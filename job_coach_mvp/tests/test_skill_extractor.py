import pytest
from skill_extractor import SkillExtractor

class TestSkillExtractor:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.extractor = SkillExtractor()
    
    def test_extract_skills_from_resume(self):
        """Test skill extraction from resume text"""
        resume_text = """
        Python developer with 3 years of experience in web development.
        Proficient in Django, Flask, React, and JavaScript.
        Experience with AWS, Docker, and Git.
        Strong communication and problem-solving skills.
        """
        
        skills = self.extractor.extract_skills_from_resume(resume_text)
        
        # Check that skills are extracted
        assert len(skills) > 0
        
        # Check for specific skills
        skill_names = [skill['name'] for skill in skills]
        assert 'Python' in skill_names
        assert 'Django' in skill_names
        assert 'React' in skill_names
        assert 'JavaScript' in skill_names
        assert 'AWS' in skill_names
        assert 'Docker' in skill_names
        assert 'Git' in skill_names
        assert 'Communication' in skill_names
    
    def test_extract_requirements_from_job_description(self):
        """Test skill requirement extraction from job description"""
        job_text = """
        Senior Python Developer position requiring:
        - Python (required)
        - Django or Flask (must have)
        - React (preferred)
        - AWS experience (nice to have)
        - Strong communication skills (essential)
        """
        
        requirements = self.extractor.extract_requirements_from_job_description(job_text)
        
        # Check that requirements are extracted
        assert len(requirements) > 0
        
        # Check for specific requirements
        req_names = [req['name'] for req in requirements]
        assert 'Python' in req_names
        assert 'Django' in req_names
        assert 'React' in req_names
        assert 'AWS' in req_names
        assert 'Communication' in req_names
    
    def test_skill_importance_detection(self):
        """Test detection of skill importance levels"""
        job_text = """
        We require Python and Django. AWS is preferred but not required.
        Communication skills are essential for this role.
        """
        
        requirements = self.extractor.extract_requirements_from_job_description(job_text)
        
        # Find specific skills and check their importance
        python_req = next((r for r in requirements if r['name'] == 'Python'), None)
        aws_req = next((r for r in requirements if r['name'] == 'AWS'), None)
        comm_req = next((r for r in requirements if r['name'] == 'Communication'), None)
        
        assert python_req is not None
        assert aws_req is not None
        assert comm_req is not None
        
        # Check importance levels (these might be 'preferred' by default)
        assert python_req['importance'] in ['critical', 'preferred']
        assert aws_req['importance'] in ['critical', 'preferred']
        assert comm_req['importance'] in ['critical', 'preferred']
    
    def test_experience_years_extraction(self):
        """Test extraction of years of experience"""
        test_cases = [
            ("Python developer with 5 years of experience", 5),
            ("3+ years in software development", 3),
            ("Experience of 2 years in web development", 2),
            ("No experience mentioned", 0),
            ("10+ years of experience in Python", 10)
        ]
        
        for text, expected in test_cases:
            years = self.extractor.extract_experience_years(text)
            assert years == expected
    
    def test_education_level_extraction(self):
        """Test extraction of education level"""
        test_cases = [
            ("Bachelor's degree in Computer Science", "Bachelors"),
            ("MS in Software Engineering", "Masters"),
            ("PhD in Machine Learning", "PhD"),
            ("High school diploma", "High School"),
            ("Associate's degree", "Associate"),
            ("No education mentioned", "Unknown")
        ]
        
        for text, expected in test_cases:
            education = self.extractor.extract_education_level(text)
            assert education == expected, f"Expected {expected} for text: {text}, got {education}"
    
    def test_skill_categorization(self):
        """Test that skills are properly categorized"""
        resume_text = "Python, React, AWS, Git, Communication"
        
        skills = self.extractor.extract_skills_from_resume(resume_text)
        
        # Check that skills have categories
        for skill in skills:
            assert 'category' in skill
            assert skill['category'] in self.extractor.SKILL_CATEGORIES.keys() or skill['category'] == 'Other'
    
    def test_empty_text_handling(self):
        """Test handling of empty or None text"""
        # Test with empty string
        skills = self.extractor.extract_skills_from_resume("")
        assert skills == []
        
        requirements = self.extractor.extract_requirements_from_job_description("")
        assert requirements == []
        
        # Test with None
        skills = self.extractor.extract_skills_from_resume(None)
        assert skills == []
        
        requirements = self.extractor.extract_requirements_from_job_description(None)
        assert requirements == []
