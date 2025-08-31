# Job-Ready Career Coach MVP
## Resume + Job Description → Action Plan

**Core Value:** Upload your resume and a job description, get a personalized action plan to become job-ready.

**Tech Stack:** Flask + SQLAlchemy + Modern CSS/JS + File Upload + Text Processing  
**Design:** Modern, minimal, mobile-first interface

## User Journey (2-3 minute flow)

1. **Upload Resume** (PDF/text) or paste resume text
2. **Add Job Description** (paste or upload job posting)  
3. **Get Skill Gap Analysis** (visual comparison of resume vs job requirements)
4. **Receive Action Plan** (specific tasks to complete before applying)
5. **Track Progress** (mark tasks complete, see readiness score)

## MVP Tasks (4 Core Features)

### Task 1: Modern Flask Setup + File Upload ✅
**Goal:** Clean, modern web app that can handle file uploads

**Features to Build:**
- [x] Flask app with modern, minimal UI (using Tailwind CSS via CDN)
- [x] File upload functionality for PDFs and text files
- [x] Text area inputs for pasting content
- [x] Responsive, mobile-first design
- [x] Basic database setup with SQLAlchemy
- [x] Drag-and-drop file upload with visual feedback
- [x] Modern templates with Inter font and clean design
- [x] Comprehensive test suite

**Key Files:**
```
job_coach_mvp/
├── app.py                    # Main Flask app
├── models.py                 # Database models  
├── text_processor.py         # Resume/job description parsing
├── gap_analyzer.py           # Skill gap analysis logic
├── requirements.txt          # Dependencies
├── uploads/                  # User uploaded files
├── templates/
│   ├── base.html            # Modern base template
│   ├── home.html            # Landing page
│   ├── upload.html          # Upload resume + job description
│   ├── analysis.html        # Gap analysis results
│   └── action_plan.html     # Generated action plan
└── static/
    ├── css/style.css        # Custom modern styles
    └── js/main.js           # Interactive elements
```

**Modern UI Requirements:**
- Clean typography (Inter font)
- Subtle shadows and rounded corners
- Drag-and-drop file upload areas
- Progress indicators
- Smooth transitions
- Mobile-responsive grid

**Dependencies:**
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
PyPDF2==3.0.1              # PDF text extraction
python-docx==0.8.11        # Word document support
nltk==3.8                  # Text processing
textstat==0.7.3            # Text analysis
```

**Acceptance Criteria:**
- Modern, professional-looking interface
- Drag-and-drop file upload works
- Can extract text from PDF resumes
- Responsive design works on mobile
- Clean, minimal aesthetic

### Task 2: Text Processing & Skill Extraction ✅
**Goal:** Extract skills and requirements from resumes and job descriptions

**Core Logic:**
- [x] Parse uploaded resume (PDF/DOCX/text) to extract skills, experience
- [x] Parse job description to identify required skills and qualifications
- [x] Create skill taxonomy (technical skills, soft skills, tools, certifications)
- [x] Match extracted skills to standardized skill database
- [x] Store parsed data in database
- [x] Comprehensive skill extraction with 8 categories
- [x] Experience level and education extraction
- [x] Skill importance detection (critical vs preferred)
- [x] Robust text processing with word boundary matching

**Skill Categories:**
```python
SKILL_CATEGORIES = {
    'Programming': ['Python', 'JavaScript', 'Java', 'C++', 'React', 'Node.js', 'Django', 'Flask'],
    'Data': ['SQL', 'PostgreSQL', 'MongoDB', 'Excel', 'Tableau', 'Power BI', 'Data Analysis'],
    'Cloud': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'CI/CD'],
    'Design': ['Figma', 'Photoshop', 'UI/UX', 'Wireframing', 'Prototyping'],
    'Soft Skills': ['Communication', 'Leadership', 'Project Management', 'Problem Solving'],
    'Tools': ['Git', 'Jira', 'Slack', 'VS Code', 'Linux']
}
```

**Text Processing Pipeline:**
1. Extract text from uploaded files
2. Normalize and clean text (remove formatting, standardize terms)
3. Identify skills using keyword matching and NLP
4. Extract experience levels, years of experience, education
5. Parse job requirements, must-haves vs nice-to-haves

**Database Models:**
```python
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_text = db.Column(db.Text)
    job_description = db.Column(db.Text)
    extracted_skills = db.Column(db.JSON)  # User's current skills
    required_skills = db.Column(db.JSON)   # Job requirements
    skill_gaps = db.Column(db.JSON)        # Calculated gaps
    readiness_score = db.Column(db.Float)  # Overall match percentage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ActionPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
    tasks = db.Column(db.JSON)             # Generated tasks
    completed_tasks = db.Column(db.JSON, default=list)
    updated_readiness_score = db.Column(db.Float)
```

**Acceptance Criteria:**
- Accurately extracts skills from resume text
- Identifies required skills from job descriptions
- Handles multiple file formats (PDF, DOCX, plain text)
- Creates structured data from unstructured text
- Matches skills to standardized taxonomy

### Task 3: Skill Gap Analysis Engine ✅
**Goal:** Visual comparison of resume skills vs job requirements with actionable insights

**Analysis Features:**
- [x] Calculate skill match percentage for the job
- [x] Identify missing critical skills (must-haves)
- [x] Highlight nice-to-have skills that would strengthen application
- [x] Show experience level gaps (junior vs senior requirements)
- [x] Generate overall job readiness score
- [x] Comprehensive gap analysis with skill level assessment
- [x] Readiness score calculation with critical/preferred weighting
- [x] Summary generation with recommendations
- [x] Strongest and weakest areas identification

**Visual Gap Analysis:**
```
Job Readiness Score: 73% 🟡

✅ SKILLS YOU HAVE:
Python ████████████ Expert
Communication ████████ Strong
Problem Solving ██████████ Expert

❌ MISSING CRITICAL SKILLS:
React ░░░░░░░░░░░░ Required for role
AWS ░░░░░░░░░░░░ Required for role

🔄 SKILLS TO IMPROVE:
JavaScript ████░░░░░░░░ Basic → Intermediate needed
SQL ██████░░░░░░ Intermediate → Advanced preferred
```

**Readiness Score Calculation:**
```python
def calculate_readiness_score(user_skills, required_skills):
    critical_skills = [s for s in required_skills if s.get('importance') == 'critical']
    nice_to_have = [s for s in required_skills if s.get('importance') == 'preferred']
    
    critical_match = sum(1 for skill in critical_skills if skill['name'] in user_skills) / len(critical_skills)
    nice_match = sum(1 for skill in nice_to_have if skill['name'] in user_skills) / len(nice_to_have)
    
    return (critical_match * 0.8 + nice_match * 0.2) * 100
```

**Gap Categories:**
- **Green (80%+):** Ready to apply! Minor improvements suggested
- **Yellow (60-79%):** Good foundation, key skills missing
- **Red (<60%):** Significant skill development needed

**Acceptance Criteria:**
- Clear visual representation of skill gaps
- Accurate readiness score calculation  
- Distinguishes between critical and nice-to-have skills
- Easy to understand what needs improvement
- Mobile-friendly analysis display

### Task 4: Personalized Action Plan Generator ⏳
**Goal:** Convert skill gaps into specific, actionable tasks with timeline

**Action Plan Components:**
- [ ] Generate specific tasks for each missing skill
- [ ] Prioritize tasks by impact on job readiness
- [ ] Provide learning resources and time estimates
- [ ] Create study timeline leading up to application
- [ ] Track task completion and update readiness score

**Task Generation Logic:**
```python
TASK_TEMPLATES = {
    'Python': {
        'beginner': "Complete Python fundamentals course (Est: 20 hours)",
        'intermediate': "Build 2-3 Python projects for portfolio (Est: 30 hours)",
        'advanced': "Contribute to open source Python project (Est: 40 hours)"
    },
    'React': {
        'beginner': "Complete React basics tutorial + build todo app (Est: 25 hours)",  
        'intermediate': "Build full-stack React application (Est: 35 hours)"
    },
    'AWS': {
        'beginner': "Get AWS Cloud Practitioner certification (Est: 15 hours)",
        'intermediate': "Deploy application using AWS services (Est: 20 hours)"
    }
}
```

**Action Plan Format:**
```
🎯 ACTION PLAN TO BECOME JOB-READY

PRIORITY 1: CRITICAL SKILLS (Complete first)
□ Learn React fundamentals (25 hours) - Week 1-2
□ Get AWS Cloud Practitioner cert (15 hours) - Week 2

PRIORITY 2: SKILL IMPROVEMENTS (Strengthen application)  
□ Build advanced JavaScript project (20 hours) - Week 3
□ Practice SQL queries and database design (10 hours) - Week 3

📅 TIMELINE: 3 weeks to job-ready (70 hours total)
📈 COMPLETION: 0/4 tasks (Current readiness: 73% → Target: 90%+)

RESOURCES:
• React: freeCodeCamp React course, React documentation
• AWS: AWS free tier, A Cloud Guru certification course
• JavaScript: JavaScript30 challenge, Mozilla MDN docs
```

**Task Tracking Features:**
- [ ] Mark individual tasks as complete
- [ ] Update readiness score as tasks are finished
- [ ] Show progress toward job-ready status
- [ ] Estimated completion timeline
- [ ] Resource links for each skill

**Acceptance Criteria:**
- Tasks are specific and actionable
- Realistic time estimates for each task
- Clear priority ordering (critical first)
- Progress tracking updates readiness score
- Includes helpful learning resources

## Modern UI/UX Specifications

### Design System
```css
/* Color Palette */
:root {
  --primary: #3B82F6;      /* Blue */
  --success: #10B981;      /* Green */  
  --warning: #F59E0B;      /* Yellow */
  --danger: #EF4444;       /* Red */
  --gray-50: #F9FAFB;
  --gray-900: #111827;
  --shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Typography */
body {
  font-family: 'Inter', system-ui, sans-serif;
  line-height: 1.6;
  color: var(--gray-900);
}
```

### Component Patterns
- **Cards:** Subtle shadows, rounded corners (8px), clean borders
- **Buttons:** Solid colors, hover states, loading spinners  
- **File Upload:** Drag-and-drop zones with visual feedback
- **Progress Bars:** Animated, color-coded by readiness level
- **Task Lists:** Clean checkboxes, completion animations

### Responsive Breakpoints
- **Mobile:** Single column, stack elements vertically
- **Tablet:** 2-column layout for analysis/action plan
- **Desktop:** Full 3-column layout with sidebar navigation

## Demo Flow (2 minutes)

**"Here's how Job Coach makes you job-ready:"**

1. **Upload Resume** (15 sec): "Drag your resume PDF here"
2. **Paste Job Description** (15 sec): "Copy job posting from LinkedIn"  
3. **See Skill Analysis** (30 sec): "73% ready - missing React and AWS"
4. **Get Action Plan** (30 sec): "Complete these 4 tasks in 3 weeks"
5. **Track Progress** (30 sec): "Mark tasks done, watch readiness improve"

**Value Proposition:** "Know exactly what skills to learn before applying for any job."

## Success Metrics

**Core Functionality:**
- [ ] Upload and analyze resume/job description in under 2 minutes
- [ ] Readiness score feels accurate to users
- [ ] Action plans contain relevant, specific tasks
- [ ] Progress tracking motivates completion

**User Experience:**  
- [ ] Interface feels modern and professional
- [ ] Works seamlessly on mobile devices
- [ ] No confusing steps or technical errors
- [ ] Fast performance (<3 second analysis)

**LinkedIn Pitch Ready:**
- [ ] Clear differentiation from existing tools
- [ ] Demonstrates immediate, practical value
- [ ] Professional appearance suitable for B2B demo
- [ ] Scalable concept for integration with LinkedIn's job platform

This MVP laser-focuses on the core problem: "What do I need to learn to get this specific job?" Perfect for validation and LinkedIn pitch!