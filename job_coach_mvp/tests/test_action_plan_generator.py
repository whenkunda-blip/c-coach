import pytest
from action_plan_generator import ActionPlanGenerator

class TestActionPlanGenerator:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.generator = ActionPlanGenerator()
    
    def test_generate_action_plan_with_skill_gaps(self):
        """Test action plan generation with skill gaps"""
        skill_gaps = [
            {
                'skill': 'React',
                'importance': 'critical',
                'type': 'missing',
                'description': 'Missing React - critical skill'
            },
            {
                'skill': 'Python',
                'importance': 'preferred',
                'type': 'level_gap',
                'current_level': 'basic',
                'target_level': 'intermediate',
                'description': 'Improve Python from basic to intermediate'
            }
        ]
        
        action_plan = self.generator.generate_action_plan(1, skill_gaps)
        
        # Check basic structure
        assert 'tasks' in action_plan
        assert 'total_hours' in action_plan
        assert 'timeline' in action_plan
        assert 'summary' in action_plan
        
        # Check tasks
        assert len(action_plan['tasks']) == 2
        
        # Check React task (critical should come first)
        react_task = action_plan['tasks'][0]
        assert react_task['skill'] == 'React'
        assert react_task['priority'] == 'critical'
        assert 'React' in react_task['title']
        assert len(react_task['resources']) > 0
        
        # Check LinkedIn Learning priority
        linkedin_resources = [r for r in react_task['resources'] if r['platform'] == 'LinkedIn Learning']
        assert len(linkedin_resources) > 0
        assert linkedin_resources[0]['priority'] == 'primary'
    
    def test_learning_resources_prioritization(self):
        """Test that LinkedIn Learning resources are prioritized"""
        resources = self.generator._get_learning_resources('Python', 'beginner')
        
        # Should have LinkedIn Learning as primary
        linkedin_resources = [r for r in resources if r['platform'] == 'LinkedIn Learning']
        assert len(linkedin_resources) > 0
        assert linkedin_resources[0]['priority'] == 'primary'
        
        # Should have YouTube as secondary
        youtube_resources = [r for r in resources if r['platform'] == 'YouTube']
        if youtube_resources:
            assert youtube_resources[0]['priority'] == 'secondary'
        
        # Should have official documentation
        official_resources = [r for r in resources if r['platform'] == 'Official']
        assert len(official_resources) > 0
    
    def test_task_creation_for_missing_skill(self):
        """Test task creation for completely missing skills"""
        gap = {
            'skill': 'Kubernetes',
            'importance': 'critical',
            'type': 'missing'
        }
        
        task = self.generator._create_task_for_missing_skill('Kubernetes', gap)
        
        assert task is not None
        assert task['skill'] == 'Kubernetes'
        assert task['priority'] == 'critical'
        assert 'Kubernetes' in task['title']
        assert task['estimated_hours'] > 0
        assert len(task['resources']) > 0
    
    def test_task_creation_for_skill_improvement(self):
        """Test task creation for skill improvement"""
        gap = {
            'skill': 'Python',
            'importance': 'preferred',
            'type': 'level_gap',
            'current_level': 'basic',
            'target_level': 'intermediate'
        }
        
        task = self.generator._create_task_for_skill_improvement('Python', gap)
        
        assert task is not None
        assert task['skill'] == 'Python'
        assert task['current_level'] == 'basic'
        assert task['target_level'] == 'intermediate'
        assert task['estimated_hours'] > 0
    
    def test_timeline_calculation(self):
        """Test timeline calculation based on total hours"""
        # Test 1 week
        timeline = self.generator._calculate_timeline(8)
        assert timeline == "1 week"
        
        # Test multiple weeks
        timeline = self.generator._calculate_timeline(25)
        assert "weeks" in timeline
        
        # Test months
        timeline = self.generator._calculate_timeline(50)
        assert "months" in timeline
    
    def test_plan_summary_generation(self):
        """Test plan summary generation"""
        tasks = [
            {
                'skill': 'React',
                'priority': 'critical',
                'estimated_hours': 25
            },
            {
                'skill': 'Python',
                'priority': 'preferred',
                'estimated_hours': 15
            }
        ]
        
        summary = self.generator._generate_plan_summary(tasks, 40, "4 weeks")
        
        assert summary['total_tasks'] == 2
        assert summary['critical_tasks'] == 1
        assert summary['total_hours'] == 40
        assert summary['timeline'] == "4 weeks"
        assert len(summary['focus_areas']) == 2
        assert len(summary['recommendations']) > 0
    
    def test_official_documentation_mapping(self):
        """Test official documentation URL mapping"""
        docs = self.generator._get_official_documentation('Python')
        assert docs == 'https://docs.python.org/3/'
        
        docs = self.generator._get_official_documentation('React')
        assert docs == 'https://react.dev/'
        
        docs = self.generator._get_official_documentation('NonExistentSkill')
        assert docs is None
    
    def test_empty_skill_gaps(self):
        """Test action plan generation with no skill gaps"""
        action_plan = self.generator.generate_action_plan(1, [])
        
        assert action_plan['tasks'] == []
        assert action_plan['total_hours'] == 0
        assert action_plan['timeline'] == "1 week"
    
    def test_task_priority_ordering(self):
        """Test that tasks are ordered by priority (critical first)"""
        skill_gaps = [
            {
                'skill': 'Python',
                'importance': 'preferred',
                'type': 'missing'
            },
            {
                'skill': 'React',
                'importance': 'critical',
                'type': 'missing'
            }
        ]
        
        action_plan = self.generator.generate_action_plan(1, skill_gaps)
        
        # Critical task should come first
        assert action_plan['tasks'][0]['priority'] == 'critical'
        assert action_plan['tasks'][0]['skill'] == 'React'
