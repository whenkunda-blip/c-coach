from typing import List, Dict, Any, Tuple, Optional, Union
from skill_extractor import SkillExtractor

class GapAnalyzer:
    """Analyze skill gaps between resume and job requirements"""
    
    def __init__(self):
        self.skill_extractor = SkillExtractor()
    
    def analyze_skills(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Perform complete skill gap analysis"""
        
        # Extract skills from resume and job description
        resume_skills = self.skill_extractor.extract_skills_from_resume(resume_text)
        required_skills = self.skill_extractor.extract_requirements_from_job_description(job_description)
        
        # Calculate skill gaps
        skill_gaps = self._calculate_skill_gaps(resume_skills, required_skills)
        
        # Calculate readiness score
        readiness_score = self._calculate_readiness_score(resume_skills, required_skills)
        
        # Extract additional information
        experience_years = self.skill_extractor.extract_experience_years(resume_text)
        education_level = self.skill_extractor.extract_education_level(resume_text)
        
        return {
            'extracted_skills': resume_skills,
            'required_skills': required_skills,
            'skill_gaps': skill_gaps,
            'readiness_score': readiness_score,
            'experience_years': experience_years,
            'education_level': education_level,
            'summary': self._generate_summary(resume_skills, required_skills, readiness_score)
        }
    
    def _calculate_skill_gaps(self, resume_skills: List[Dict], required_skills: List[Dict]) -> List[Dict]:
        """Calculate gaps between resume skills and job requirements"""
        gaps = []
        
        # Create sets of skill names for easy comparison
        resume_skill_names = {skill['name'].lower() for skill in resume_skills}
        
        for required_skill in required_skills:
            skill_name = required_skill['name'].lower()
            
            if skill_name not in resume_skill_names:
                # Missing skill
                gaps.append({
                    'skill': required_skill['name'],
                    'importance': required_skill['importance'],
                    'category': required_skill['category'],
                    'type': 'missing',
                    'description': f"Missing {required_skill['name']} - {required_skill['importance']} skill"
                })
            else:
                # Skill exists, check if level is sufficient
                resume_skill = next(s for s in resume_skills if s['name'].lower() == skill_name)
                level_gap = self._assess_level_gap(resume_skill['level'], required_skill.get('level', 'basic'))
                
                if level_gap:
                    gaps.append({
                        'skill': required_skill['name'],
                        'importance': required_skill['importance'],
                        'category': required_skill['category'],
                        'type': 'level_gap',
                        'description': f"Improve {required_skill['name']} from {resume_skill['level']} to {level_gap['target_level']}",
                        'current_level': resume_skill['level'],
                        'target_level': level_gap['target_level']
                    })
        
        # Sort gaps by importance (critical first)
        importance_order = {'critical': 0, 'high': 1, 'preferred': 2}
        gaps.sort(key=lambda x: importance_order.get(x['importance'], 3))
        
        return gaps
    
    def _assess_level_gap(self, current_level: str, required_level: str) -> Optional[Dict[str, str]]:
        """Assess if there's a level gap between current and required skill level"""
        level_hierarchy = {'basic': 1, 'intermediate': 2, 'advanced': 3}
        
        current_score = level_hierarchy.get(current_level, 1)
        required_score = level_hierarchy.get(required_level, 1)
        
        if current_score < required_score:
            return {
                'target_level': required_level,
                'gap_size': required_score - current_score
            }
        
        return None
    
    def _calculate_readiness_score(self, resume_skills: List[Dict], required_skills: List[Dict]) -> float:
        """Calculate overall job readiness score (0-100)"""
        if not required_skills:
            return 100.0
        
        # Separate critical and preferred skills
        critical_skills = [s for s in required_skills if s.get('importance') == 'critical']
        preferred_skills = [s for s in required_skills if s.get('importance') != 'critical']
        
        resume_skill_names = {skill['name'].lower() for skill in resume_skills}
        
        # Calculate critical skills match (weighted 80%)
        critical_match = 0
        if critical_skills:
            critical_matches = sum(1 for skill in critical_skills if skill['name'].lower() in resume_skill_names)
            critical_match = (critical_matches / len(critical_skills)) * 0.8
        
        # Calculate preferred skills match (weighted 20%)
        preferred_match = 0
        if preferred_skills:
            preferred_matches = sum(1 for skill in preferred_skills if skill['name'].lower() in resume_skill_names)
            preferred_match = (preferred_matches / len(preferred_skills)) * 0.2
        
        total_score = (critical_match + preferred_match) * 100
        
        return round(total_score, 1)
    
    def _generate_summary(self, resume_skills: List[Dict], required_skills: List[Dict], readiness_score: float) -> Dict[str, Any]:
        """Generate a summary of the analysis"""
        
        # Count skills by category
        resume_by_category = {}
        for skill in resume_skills:
            category = skill['category']
            if category not in resume_by_category:
                resume_by_category[category] = []
            resume_by_category[category].append(skill)
        
        required_by_category = {}
        for skill in required_skills:
            category = skill['category']
            if category not in required_by_category:
                required_by_category[category] = []
            required_by_category[category].append(skill)
        
        # Find strongest and weakest areas
        strongest_areas = []
        weakest_areas = []
        
        for category in required_by_category:
            resume_count = len(resume_by_category.get(category, []))
            required_count = len(required_by_category[category])
            
            if resume_count >= required_count:
                strongest_areas.append(category)
            elif resume_count == 0:
                weakest_areas.append(category)
        
        # Generate recommendations
        recommendations = []
        if readiness_score < 60:
            recommendations.append("Focus on developing critical missing skills first")
        elif readiness_score < 80:
            recommendations.append("Strengthen your application by improving key skills")
        else:
            recommendations.append("You're well-positioned for this role")
        
        if len(weakest_areas) > 0:
            recommendations.append(f"Consider focusing on: {', '.join(weakest_areas[:3])}")
        
        return {
            'readiness_level': self._get_readiness_level(readiness_score),
            'strongest_areas': strongest_areas[:3],
            'weakest_areas': weakest_areas[:3],
            'recommendations': recommendations,
            'skill_coverage': {
                'resume_skills': len(resume_skills),
                'required_skills': len(required_skills),
                'matching_skills': len([s for s in required_skills if s['name'].lower() in {rs['name'].lower() for rs in resume_skills}])
            }
        }
    
    def _get_readiness_level(self, score: float) -> str:
        """Get readiness level based on score"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Strong"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        else:
            return "Needs Improvement"
