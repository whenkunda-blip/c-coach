from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from models import db, Analysis, ActionPlan
from text_processor import TextProcessor
from gap_analyzer import GapAnalyzer
from action_plan_generator import ActionPlanGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_coach.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

# Initialize database
db.init_app(app)

# Initialize gap analyzer
gap_analyzer = GapAnalyzer()

# Initialize action plan generator
action_plan_generator = ActionPlanGenerator()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Landing page"""
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle resume and job description upload"""
    if request.method == 'POST':
        resume_text = ""
        job_description = ""
        
        # Handle resume upload
        if 'resume_file' in request.files:
            resume_file = request.files['resume_file']
            if resume_file and resume_file.filename != '':
                if allowed_file(resume_file.filename):
                    filename = secure_filename(resume_file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    resume_file.save(file_path)
                    
                    try:
                        resume_text = TextProcessor.extract_text_from_file(file_path)
                        resume_text = TextProcessor.clean_text(resume_text)
                    except Exception as e:
                        flash(f'Error processing resume: {str(e)}', 'error')
                        return redirect(request.url)
                    finally:
                        # Clean up uploaded file
                        if os.path.exists(file_path):
                            os.remove(file_path)
                else:
                    flash('Invalid file type for resume. Please upload PDF, DOCX, or TXT.', 'error')
                    return redirect(request.url)
        
        # Handle resume text input
        if not resume_text and request.form.get('resume_text'):
            resume_text = TextProcessor.clean_text(request.form.get('resume_text'))
        
        # Handle job description
        if request.form.get('job_description'):
            job_description = TextProcessor.clean_text(request.form.get('job_description'))
        
        if not resume_text or not job_description:
            flash('Please provide both resume and job description.', 'error')
            return redirect(request.url)
        
        # Perform skill analysis
        analysis_result = gap_analyzer.analyze_skills(resume_text, job_description)
        
        # Create analysis record
        analysis = Analysis(
            resume_text=resume_text,
            job_description=job_description,
            extracted_skills=analysis_result['extracted_skills'],
            required_skills=analysis_result['required_skills'],
            skill_gaps=analysis_result['skill_gaps'],
            readiness_score=analysis_result['readiness_score']
        )
        db.session.add(analysis)
        db.session.commit()
        
        return redirect(url_for('analysis', analysis_id=analysis.id))
    
    return render_template('upload.html')

@app.route('/analysis/<int:analysis_id>')
def analysis(analysis_id):
    """Display skill gap analysis"""
    analysis = Analysis.query.get_or_404(analysis_id)
    return render_template('analysis.html', analysis=analysis)

@app.route('/action-plan/<int:analysis_id>')
def action_plan(analysis_id):
    """Display personalized action plan"""
    analysis = Analysis.query.get_or_404(analysis_id)
    action_plan = ActionPlan.query.filter_by(analysis_id=analysis_id).first()
    
    # Generate action plan if it doesn't exist
    if not action_plan and analysis.skill_gaps:
        action_plan_data = action_plan_generator.generate_action_plan(analysis_id, analysis.skill_gaps)
        action_plan = ActionPlan(
            analysis_id=analysis_id,
            tasks=action_plan_data['tasks'],
            completed_tasks=action_plan_data['completed_tasks'],
            updated_readiness_score=action_plan_data['updated_readiness_score']
        )
        db.session.add(action_plan)
        db.session.commit()
    
    return render_template('action_plan.html', analysis=analysis, action_plan=action_plan)

@app.route('/generate-action-plan/<int:analysis_id>')
def generate_action_plan(analysis_id):
    """Generate a new action plan"""
    analysis = Analysis.query.get_or_404(analysis_id)
    
    if not analysis.skill_gaps:
        flash('No skill gaps found to generate action plan.', 'error')
        return redirect(url_for('analysis', analysis_id=analysis_id))
    
    # Generate action plan
    action_plan_data = action_plan_generator.generate_action_plan(analysis_id, analysis.skill_gaps)
    
    # Check if action plan already exists
    existing_plan = ActionPlan.query.filter_by(analysis_id=analysis_id).first()
    if existing_plan:
        # Update existing plan
        existing_plan.tasks = action_plan_data['tasks']
        existing_plan.completed_tasks = action_plan_data['completed_tasks']
        existing_plan.updated_readiness_score = action_plan_data['updated_readiness_score']
    else:
        # Create new plan
        action_plan = ActionPlan(
            analysis_id=analysis_id,
            tasks=action_plan_data['tasks'],
            completed_tasks=action_plan_data['completed_tasks'],
            updated_readiness_score=action_plan_data['updated_readiness_score']
        )
        db.session.add(action_plan)
    
    db.session.commit()
    flash('Action plan generated successfully!', 'success')
    return redirect(url_for('action_plan', analysis_id=analysis_id))

@app.route('/complete-task/<int:analysis_id>/<task_id>', methods=['POST'])
def complete_task(analysis_id, task_id):
    """Mark a task as complete and update progress"""
    action_plan = ActionPlan.query.filter_by(analysis_id=analysis_id).first()
    
    if not action_plan:
        flash('Action plan not found.', 'error')
        return redirect(url_for('action_plan', analysis_id=analysis_id))
    
    # Initialize completed_tasks if None
    if action_plan.completed_tasks is None:
        action_plan.completed_tasks = []
    
    # Toggle task completion
    if task_id in action_plan.completed_tasks:
        action_plan.completed_tasks.remove(task_id)
        flash('Task marked as incomplete.', 'info')
    else:
        action_plan.completed_tasks.append(task_id)
        flash('Task marked as complete!', 'success')
    
    # Update readiness score based on completed tasks
    if action_plan.completed_tasks:
        # Calculate new readiness score
        total_tasks = len(action_plan.tasks) if action_plan.tasks else 1
        completed_count = len(action_plan.completed_tasks)
        progress_percentage = (completed_count / total_tasks) * 100
        
        # Get original analysis
        analysis = Analysis.query.get(analysis_id)
        if analysis:
            # Increase readiness score based on progress
            original_score = analysis.readiness_score or 0
            max_improvement = 100 - original_score
            improvement = (progress_percentage / 100) * max_improvement
            action_plan.updated_readiness_score = min(100, original_score + improvement)
    
    db.session.commit()
    return redirect(url_for('action_plan', analysis_id=analysis_id))

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
