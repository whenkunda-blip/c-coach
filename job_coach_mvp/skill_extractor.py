import re
import nltk
from typing import List, Dict, Any
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class SkillExtractor:
    """Extract skills from resume and job description text"""
    
    # Comprehensive skill taxonomy
    SKILL_CATEGORIES = {
        'Programming': [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Go', 'Rust', 'Swift', 'Kotlin',
            'TypeScript', 'Scala', 'R', 'MATLAB', 'Perl', 'Shell', 'Bash', 'PowerShell'
        ],
        'Web Development': [
            'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Express.js',
            'Laravel', 'Spring', 'ASP.NET', 'Ruby on Rails', 'jQuery', 'Bootstrap', 'Tailwind CSS',
            'Sass', 'Less', 'Webpack', 'Babel', 'npm', 'yarn'
        ],
        'Data & Analytics': [
            'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Cassandra',
            'Excel', 'Tableau', 'Power BI', 'Looker', 'Data Analysis', 'Data Visualization',
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn',
            'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Jupyter', 'Apache Spark', 'Hadoop'
        ],
        'Cloud & DevOps': [
            'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI',
            'GitHub Actions', 'Terraform', 'Ansible', 'Chef', 'Puppet', 'Linux', 'Ubuntu',
            'CentOS', 'Red Hat', 'CI/CD', 'Microservices', 'Serverless', 'Lambda'
        ],
        'Design & UX': [
            'Figma', 'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'InVision', 'UI/UX',
            'Wireframing', 'Prototyping', 'User Research', 'Design Systems', 'Responsive Design',
            'Accessibility', 'WCAG', 'Adobe XD', 'Framer'
        ],
        'Soft Skills': [
            'Communication', 'Leadership', 'Project Management', 'Problem Solving', 'Teamwork',
            'Collaboration', 'Time Management', 'Critical Thinking', 'Creativity', 'Adaptability',
            'Customer Service', 'Presentation Skills', 'Negotiation', 'Mentoring'
        ],
        'Tools & Platforms': [
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jira', 'Confluence', 'Slack', 'Microsoft Teams',
            'VS Code', 'IntelliJ', 'Eclipse', 'Sublime Text', 'Vim', 'Emacs', 'Postman',
            'Swagger', 'Figma', 'Notion', 'Trello', 'Asana', 'Monday.com'
        ],
        'Methodologies': [
            'Agile', 'Scrum', 'Kanban', 'Waterfall', 'DevOps', 'Lean', 'Six Sigma',
            'Design Thinking', 'User-Centered Design', 'Test-Driven Development', 'BDD'
        ]
    }
    
    # Experience level indicators
    EXPERIENCE_INDICATORS = {
        'entry': ['entry level', 'junior', '0-1 years', '1-2 years', 'recent graduate', 'new grad'],
        'mid': ['mid level', 'intermediate', '2-3 years', '3-5 years', 'experienced'],
        'senior': ['senior', 'lead', '5+ years', '7+ years', '10+ years', 'expert', 'principal']
    }
    
    def __init__(self):
        self.all_skills = self._flatten_skills()
    
    def _flatten_skills(self) -> List[str]:
        """Flatten all skills into a single list for easier matching"""
        skills = []
        for category_skills in self.SKILL_CATEGORIES.values():
            skills.extend(category_skills)
        return skills
    
    def extract_skills_from_resume(self, resume_text: str) -> List[Dict[str, Any]]:
        """Extract skills from resume text"""
        if not resume_text:
            return []
        
        # Normalize text
        text = resume_text.lower()
        
        # Find skills in the text
        found_skills = []
        for skill in self.all_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text):
                # Determine skill level based on context
                level = self._determine_skill_level(text, skill.lower())
                found_skills.append({
                    'name': skill,
                    'level': level,
                    'category': self._get_skill_category(skill)
                })
        
        return found_skills
    
    def extract_requirements_from_job_description(self, job_text: str) -> List[Dict[str, Any]]:
        """Extract required skills from job description"""
        if not job_text:
            return []
        
        # Normalize text
        text = job_text.lower()
        
        # Find skills in the text
        required_skills = []
        for skill in self.all_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text):
                # Determine importance based on context
                importance = self._determine_skill_importance(text, skill.lower())
                required_skills.append({
                    'name': skill,
                    'importance': importance,
                    'category': self._get_skill_category(skill)
                })
        
        return required_skills
    
    def _determine_skill_level(self, text: str, skill: str) -> str:
        """Determine skill level based on context"""
        # Look for experience indicators near the skill
        skill_index = text.find(skill)
        if skill_index == -1:
            return 'basic'
        
        # Check context around the skill
        context_start = max(0, skill_index - 100)
        context_end = min(len(text), skill_index + 100)
        context = text[context_start:context_end]
        
        # Check for experience level indicators
        for level, indicators in self.EXPERIENCE_INDICATORS.items():
            for indicator in indicators:
                if indicator in context:
                    if level == 'entry':
                        return 'basic'
                    elif level == 'mid':
                        return 'intermediate'
                    elif level == 'senior':
                        return 'advanced'
        
        return 'basic'
    
    def _determine_skill_importance(self, text: str, skill: str) -> str:
        """Determine skill importance based on context"""
        skill_index = text.find(skill)
        if skill_index == -1:
            return 'preferred'
        
        # Check context around the skill
        context_start = max(0, skill_index - 100)
        context_end = min(len(text), skill_index + 100)
        context = text[context_start:context_end]
        
        # Look for importance indicators
        critical_indicators = ['required', 'must have', 'essential', 'mandatory', 'necessary']
        preferred_indicators = ['preferred', 'nice to have', 'bonus', 'plus', 'advantage']
        
        for indicator in critical_indicators:
            if indicator in context:
                return 'critical'
        
        for indicator in preferred_indicators:
            if indicator in context:
                return 'preferred'
        
        return 'preferred'
    
    def _get_skill_category(self, skill: str) -> str:
        """Get the category for a given skill"""
        for category, skills in self.SKILL_CATEGORIES.items():
            if skill in skills:
                return category
        return 'Other'
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        if not text:
            return 0
        
        # Look for patterns like "X years", "X+ years", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s*of?\s*experience',
            r'experience\s*of?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in',
            r'in\s*(\d+)\+?\s*years?'
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return int(match.group(1))
        
        return 0
    
    def extract_education_level(self, text: str) -> str:
        """Extract education level from text"""
        if not text:
            return 'Unknown'
        
        text_lower = text.lower()
        
        # Use word boundaries to avoid partial matches
        if re.search(r'\bphd\b', text_lower) or re.search(r'\bdoctorate\b', text_lower):
            return 'PhD'
        elif re.search(r'\bmasters?\b', text_lower) or re.search(r'\bms\b', text_lower) or re.search(r'\bma\b', text_lower) or re.search(r'\bmba\b', text_lower):
            return 'Masters'
        elif re.search(r'\bbachelors?\b', text_lower) or re.search(r'\bbs\b', text_lower) or re.search(r'\bba\b', text_lower):
            return 'Bachelors'
        elif re.search(r'\bassociate\b', text_lower) or re.search(r'\baa\b', text_lower) or re.search(r'\bas\b', text_lower):
            return 'Associate'
        elif re.search(r'\bhigh school\b', text_lower) or re.search(r'\bhs diploma\b', text_lower) or re.search(r'\bged\b', text_lower):
            return 'High School'
        
        return 'Unknown'
