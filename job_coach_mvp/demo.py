#!/usr/bin/env python3
"""
Demo script for Career Copilot MVP
Shows the skill extraction and gap analysis functionality
"""

from skill_extractor import SkillExtractor
from gap_analyzer import GapAnalyzer

def main():
    print("🎯 Job-Ready Career Coach MVP Demo")
    print("=" * 50)
    
    # Sample resume text
    resume_text = """
    John Doe
    Python Developer
    
    EXPERIENCE:
    Software Developer at TechCorp (2021-2023)
    - Developed web applications using Python, Django, and React
    - Worked with AWS services including EC2 and S3
    - Used Git for version control and collaborated with team using Jira
    - Implemented CI/CD pipelines with Jenkins
    
    SKILLS:
    - Python (3 years experience)
    - Django, Flask
    - JavaScript, React
    - AWS, Docker
    - Git, Jira
    - Communication, Problem Solving
    
    EDUCATION:
    Bachelor's degree in Computer Science
    """
    
    # Sample job description
    job_description = """
    Senior Python Developer
    
    We are looking for a Senior Python Developer to join our team.
    
    REQUIREMENTS:
    - Python (required, 5+ years experience)
    - Django or Flask (must have)
    - React (preferred)
    - AWS experience (essential)
    - Docker and Kubernetes (nice to have)
    - Strong communication skills (required)
    - Experience with CI/CD (preferred)
    
    RESPONSIBILITIES:
    - Develop and maintain web applications
    - Work with cloud infrastructure
    - Collaborate with cross-functional teams
    """
    
    print("\n📄 Sample Resume:")
    print("-" * 30)
    print(resume_text[:200] + "...")
    
    print("\n💼 Sample Job Description:")
    print("-" * 30)
    print(job_description[:200] + "...")
    
    # Initialize analyzers
    extractor = SkillExtractor()
    analyzer = GapAnalyzer()
    
    print("\n🔍 Analyzing Skills...")
    print("-" * 30)
    
    # Extract skills from resume
    resume_skills = extractor.extract_skills_from_resume(resume_text)
    print(f"Skills found in resume: {len(resume_skills)}")
    for skill in resume_skills:
        print(f"  - {skill['name']} ({skill['level']}) - {skill['category']}")
    
    # Extract requirements from job
    required_skills = extractor.extract_requirements_from_job_description(job_description)
    print(f"\nSkills required for job: {len(required_skills)}")
    for skill in required_skills:
        print(f"  - {skill['name']} ({skill['importance']}) - {skill['category']}")
    
    # Perform gap analysis
    print("\n📊 Gap Analysis Results:")
    print("-" * 30)
    
    analysis = analyzer.analyze_skills(resume_text, job_description)
    
    print(f"Job Readiness Score: {analysis['readiness_score']}%")
    print(f"Experience Years: {analysis['experience_years']}")
    print(f"Education Level: {analysis['education_level']}")
    
    print(f"\nSkill Gaps Found: {len(analysis['skill_gaps'])}")
    for gap in analysis['skill_gaps']:
        print(f"  - {gap['skill']} ({gap['importance']}): {gap['description']}")
    
    print(f"\nSummary:")
    print(f"  - Readiness Level: {analysis['summary']['readiness_level']}")
    print(f"  - Strongest Areas: {', '.join(analysis['summary']['strongest_areas'])}")
    print(f"  - Weakest Areas: {', '.join(analysis['summary']['weakest_areas'])}")
    
    for rec in analysis['summary']['recommendations']:
        print(f"  - Recommendation: {rec}")
    
    print("\n✅ Demo completed successfully!")
    print("\nTo run the full web application:")
    print("  python3 app.py")
    print("  Then visit: http://localhost:5000")

if __name__ == "__main__":
    main()
