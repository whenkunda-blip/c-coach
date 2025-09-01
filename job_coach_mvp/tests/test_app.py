import pytest
from app import app, db
from models import Analysis

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.drop_all()

@pytest.fixture
def app_context():
    """Create an application context"""
    with app.app_context():
        yield

class TestApp:
    
    def test_home_page(self, client):
        """Test that home page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Career Copilot' in response.data
        assert b'Start Your Free Analysis' in response.data
    
    def test_upload_page_get(self, client):
        """Test that upload page loads correctly"""
        response = client.get('/upload')
        assert response.status_code == 200
        assert b'Upload Your Resume' in response.data
        assert b'Job Description' in response.data
    
    def test_upload_with_file(self, client, app_context):
        """Test upload with file input"""
        # Create a test file
        from io import BytesIO
        
        data = {
            'resume_file': (BytesIO(b'Python developer with 3 years experience'), 'test_resume.pdf'),
            'job_description': 'Senior Python Developer position requiring Python, Django, and AWS'
        }
        
        response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        
        # Check that analysis was created
        analysis = Analysis.query.first()
        assert analysis is not None
        assert 'Python developer' in analysis.resume_text
        assert 'Senior Python Developer' in analysis.job_description
    
    def test_upload_missing_data(self, client):
        """Test upload with missing required data"""
        # Test with missing resume file
        data = {'job_description': 'Test job description'}
        response = client.post('/upload', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Please upload a resume file' in response.data
    
    def test_analysis_page_not_found(self, client):
        """Test analysis page with non-existent ID"""
        response = client.get('/analysis/999')
        assert response.status_code == 404
    
    def test_action_plan_page_not_found(self, client):
        """Test action plan page with non-existent ID"""
        response = client.get('/action-plan/999')
        assert response.status_code == 404
    
    def test_upload_with_docx_file(self, client, app_context):
        """Test upload with DOCX file input"""
        # Create a test DOCX file
        from io import BytesIO
        
        data = {
            'resume_file': (BytesIO(b'Python developer with 3 years experience'), 'test_resume.docx'),
            'job_description': 'Senior Python Developer position requiring Python, Django, and AWS'
        }
        
        response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        
        # Check that analysis was created
        analysis = Analysis.query.first()
        assert analysis is not None
        assert 'Python developer' in analysis.resume_text
        assert 'Senior Python Developer' in analysis.job_description
