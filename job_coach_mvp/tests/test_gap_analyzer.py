import pytest
from gap_analyzer import GapAnalyzer

class TestGapAnalyzer:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analyzer = GapAnalyzer()
    
    def test_analyze_skills_complete_analysis(self):
        """Test complete skill analysis"""
        resume_text = """
        Python developer with 3 years of experience.
        Proficient in Django, Flask, and JavaScript.
        Experience with Git and basic AWS.
        Strong communication skills.
        """
        
        job_text = """
        Senior Python Developer position requiring:
        - Python (required)
        - Django (must have)
        - React (preferred)
        - AWS (essential)
        - Communication skills (required)
        """
        
        result = self.analyzer.analyze_skills(resume_text, job_text)
        
        # Check that all expected keys are present
        expected_keys = ['extracted_skills', 'required_skills', 'skill_gaps', 
                        'readiness_score', 'experience_years', 'education_level', 'summary']
        for key in expected_keys:
            assert key in result
        
        # Check that skills are extracted
        assert len(result['extracted_skills']) > 0
        assert len(result['required_skills']) > 0
        
        # Check readiness score is between 0 and 100
        assert 0 <= result['readiness_score'] <= 100
        
        # Check that gaps are identified
        assert len(result['skill_gaps']) > 0
    
    def test_readiness_score_calculation(self):
        """Test readiness score calculation"""
        # Perfect match
        resume_skills = [
            {'name': 'Python', 'level': 'advanced', 'category': 'Programming'},
            {'name': 'Django', 'level': 'intermediate', 'category': 'Web Development'}
        ]
        
        required_skills = [
            {'name': 'Python', 'importance': 'critical', 'category': 'Programming'},
            {'name': 'Django', 'importance': 'critical', 'category': 'Web Development'}
        ]
        
        score = self.analyzer._calculate_readiness_score(resume_skills, required_skills)
        assert score == 80.0  # Both skills are critical, so 100% * 0.8 = 80%
        
        # Partial match
        required_skills_mixed = [
            {'name': 'Python', 'importance': 'critical', 'category': 'Programming'},
            {'name': 'React', 'importance': 'preferred', 'category': 'Web Development'}
        ]
        
        score = self.analyzer._calculate_readiness_score(resume_skills, required_skills_mixed)
        assert 0 < score < 100
        
        # No requirements
        score = self.analyzer._calculate_readiness_score(resume_skills, [])
        assert score == 100.0
    
    def test_skill_gap_calculation(self):
        """Test skill gap calculation"""
        resume_skills = [
            {'name': 'Python', 'level': 'intermediate', 'category': 'Programming'},
            {'name': 'JavaScript', 'level': 'basic', 'category': 'Programming'}
        ]
        
        required_skills = [
            {'name': 'Python', 'importance': 'critical', 'category': 'Programming'},
            {'name': 'React', 'importance': 'critical', 'category': 'Web Development'},
            {'name': 'JavaScript', 'importance': 'preferred', 'category': 'Programming'}
        ]
        
        gaps = self.analyzer._calculate_skill_gaps(resume_skills, required_skills)
        
        # Should find React as missing
        missing_skills = [gap for gap in gaps if gap['type'] == 'missing']
        assert len(missing_skills) > 0
        
        react_gap = next((gap for gap in missing_skills if gap['skill'] == 'React'), None)
        assert react_gap is not None
        assert react_gap['importance'] == 'critical'
    
    def test_level_gap_assessment(self):
        """Test level gap assessment"""
        # No gap
        result = self.analyzer._assess_level_gap('advanced', 'basic')
        assert result is None
        
        # Gap exists
        result = self.analyzer._assess_level_gap('basic', 'advanced')
        assert result is not None
        assert result['target_level'] == 'advanced'
        assert result['gap_size'] == 2
    
    def test_summary_generation(self):
        """Test summary generation"""
        resume_skills = [
            {'name': 'Python', 'level': 'intermediate', 'category': 'Programming'},
            {'name': 'Django', 'level': 'basic', 'category': 'Web Development'}
        ]
        
        required_skills = [
            {'name': 'Python', 'importance': 'critical', 'category': 'Programming'},
            {'name': 'React', 'importance': 'critical', 'category': 'Web Development'}
        ]
        
        summary = self.analyzer._generate_summary(resume_skills, required_skills, 50.0)
        
        # Check summary structure
        assert 'readiness_level' in summary
        assert 'strongest_areas' in summary
        assert 'weakest_areas' in summary
        assert 'recommendations' in summary
        assert 'skill_coverage' in summary
        
        # Check readiness level
        assert summary['readiness_level'] in ['Excellent', 'Strong', 'Good', 'Fair', 'Needs Improvement']
        
        # Check skill coverage
        coverage = summary['skill_coverage']
        assert coverage['resume_skills'] == 2
        assert coverage['required_skills'] == 2
        assert coverage['matching_skills'] == 1
    
    def test_readiness_level_determination(self):
        """Test readiness level determination"""
        assert self.analyzer._get_readiness_level(95) == "Excellent"
        assert self.analyzer._get_readiness_level(85) == "Strong"
        assert self.analyzer._get_readiness_level(75) == "Good"
        assert self.analyzer._get_readiness_level(65) == "Fair"
        assert self.analyzer._get_readiness_level(45) == "Needs Improvement"
    
    def test_empty_input_handling(self):
        """Test handling of empty inputs"""
        result = self.analyzer.analyze_skills("", "")
        
        assert result['extracted_skills'] == []
        assert result['required_skills'] == []
        assert result['skill_gaps'] == []
        assert result['readiness_score'] == 100.0  # No requirements = perfect score
        assert result['experience_years'] == 0
        assert result['education_level'] == 'Unknown'
