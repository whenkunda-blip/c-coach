from typing import List, Dict, Any, Optional
from gap_analyzer import GapAnalyzer
import re

class ActionPlanGenerator:
    """Generate personalized action plans with learning resources"""
    
    # LinkedIn Learning course mappings
    LINKEDIN_LEARNING_COURSES = {
        'Python': {
            'beginner': {
                'title': 'Python Essential Training',
                'url': 'https://www.linkedin.com/learning/python-essential-training-2',
                'duration': '4h 30m',
                'instructor': 'Bill Weinman'
            },
            'intermediate': {
                'title': 'Advanced Python',
                'url': 'https://www.linkedin.com/learning/advanced-python',
                'duration': '3h 45m',
                'instructor': 'Joe Marini'
            },
            'advanced': {
                'title': 'Python Design Patterns',
                'url': 'https://www.linkedin.com/learning/python-design-patterns',
                'duration': '2h 15m',
                'instructor': 'Jungwoo Ryoo'
            }
        },
        'JavaScript': {
            'beginner': {
                'title': 'JavaScript Essential Training',
                'url': 'https://www.linkedin.com/learning/javascript-essential-training-3',
                'duration': '5h 15m',
                'instructor': 'Morten Rand-Hendriksen'
            },
            'intermediate': {
                'title': 'JavaScript: Advanced Concepts',
                'url': 'https://www.linkedin.com/learning/javascript-advanced-concepts',
                'duration': '4h 20m',
                'instructor': 'Sasha Vodnik'
            }
        },
        'React': {
            'beginner': {
                'title': 'React.js Essential Training',
                'url': 'https://www.linkedin.com/learning/react-js-essential-training',
                'duration': '4h 45m',
                'instructor': 'Eve Porcello'
            },
            'intermediate': {
                'title': 'React: Advanced Patterns',
                'url': 'https://www.linkedin.com/learning/react-advanced-patterns',
                'duration': '3h 30m',
                'instructor': 'Shaun Wassell'
            }
        },
        'Django': {
            'beginner': {
                'title': 'Django Essential Training',
                'url': 'https://www.linkedin.com/learning/django-essential-training',
                'duration': '4h 10m',
                'instructor': 'Justin Mitchel'
            },
            'intermediate': {
                'title': 'Django: Advanced Concepts',
                'url': 'https://www.linkedin.com/learning/django-advanced-concepts',
                'duration': '3h 55m',
                'instructor': 'Justin Mitchel'
            }
        },
        'AWS': {
            'beginner': {
                'title': 'AWS Essential Training for Developers',
                'url': 'https://www.linkedin.com/learning/aws-essential-training-for-developers',
                'duration': '5h 30m',
                'instructor': 'Jeremy Villeneuve'
            },
            'intermediate': {
                'title': 'AWS for Developers: Deploying Applications',
                'url': 'https://www.linkedin.com/learning/aws-for-developers-deploying-applications',
                'duration': '4h 15m',
                'instructor': 'Jeremy Villeneuve'
            }
        },
        'Docker': {
            'beginner': {
                'title': 'Docker Essential Training',
                'url': 'https://www.linkedin.com/learning/docker-essential-training',
                'duration': '3h 45m',
                'instructor': 'James Williams'
            },
            'intermediate': {
                'title': 'Docker: Advanced Concepts',
                'url': 'https://www.linkedin.com/learning/docker-advanced-concepts',
                'duration': '3h 20m',
                'instructor': 'James Williams'
            }
        },
        'Kubernetes': {
            'beginner': {
                'title': 'Kubernetes Essential Training',
                'url': 'https://www.linkedin.com/learning/kubernetes-essential-training',
                'duration': '4h 25m',
                'instructor': 'James Williams'
            }
        },
        'Git': {
            'beginner': {
                'title': 'Git Essential Training',
                'url': 'https://www.linkedin.com/learning/git-essential-training-the-basics',
                'duration': '3h 15m',
                'instructor': 'Kevin Skoglund'
            },
            'intermediate': {
                'title': 'Git: Advanced Techniques',
                'url': 'https://www.linkedin.com/learning/git-advanced-techniques',
                'duration': '2h 45m',
                'instructor': 'Kevin Skoglund'
            }
        },
        'SQL': {
            'beginner': {
                'title': 'SQL Essential Training',
                'url': 'https://www.linkedin.com/learning/sql-essential-training-2',
                'duration': '4h 20m',
                'instructor': 'Bill Weinman'
            },
            'intermediate': {
                'title': 'SQL: Advanced Querying',
                'url': 'https://www.linkedin.com/learning/sql-advanced-querying',
                'duration': '3h 30m',
                'instructor': 'Bill Weinman'
            }
        },
        'Machine Learning': {
            'beginner': {
                'title': 'Machine Learning with Python',
                'url': 'https://www.linkedin.com/learning/machine-learning-with-python',
                'duration': '5h 45m',
                'instructor': 'Frederic Ngen'
            }
        }
    }
    
    # YouTube fallback resources
    YOUTUBE_RESOURCES = {
        'Python': {
            'beginner': {
                'title': 'Python for Beginners - Full Course',
                'url': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc',
                'channel': 'Programming with Mosh',
                'duration': '6h 14m'
            },
            'intermediate': {
                'title': 'Python Intermediate Tutorial',
                'url': 'https://www.youtube.com/watch?v=HGOBQPFzWKo',
                'channel': 'Corey Schafer',
                'duration': '4h 30m'
            }
        },
        'React': {
            'beginner': {
                'title': 'React Tutorial for Beginners',
                'url': 'https://www.youtube.com/watch?v=Ke90Tje7VS0',
                'channel': 'Programming with Mosh',
                'duration': '5h 20m'
            }
        },
        'AWS': {
            'beginner': {
                'title': 'AWS Tutorial for Beginners',
                'url': 'https://www.youtube.com/watch?v=ulprqHHWlng',
                'channel': 'Simplilearn',
                'duration': '4h 15m'
            }
        }
    }
    
    # Task templates with time estimates
    TASK_TEMPLATES = {
        'Python': {
            'beginner': {
                'title': 'Complete Python Fundamentals Course',
                'description': 'Learn Python basics including syntax, data structures, and control flow',
                'estimated_hours': 20,
                'timeline': 'Week 1-2',
                'priority': 'high'
            },
            'intermediate': {
                'title': 'Build 2-3 Python Projects for Portfolio',
                'description': 'Create practical projects to demonstrate Python skills',
                'estimated_hours': 30,
                'timeline': 'Week 2-4',
                'priority': 'high'
            },
            'advanced': {
                'title': 'Master Advanced Python Concepts',
                'description': 'Learn decorators, generators, context managers, and design patterns',
                'estimated_hours': 25,
                'timeline': 'Week 3-5',
                'priority': 'medium'
            }
        },
        'React': {
            'beginner': {
                'title': 'Complete React Basics Tutorial',
                'description': 'Learn React fundamentals including components, state, and props',
                'estimated_hours': 25,
                'timeline': 'Week 1-3',
                'priority': 'high'
            },
            'intermediate': {
                'title': 'Build Full-Stack React Application',
                'description': 'Create a complete web application with React frontend and API backend',
                'estimated_hours': 35,
                'timeline': 'Week 3-6',
                'priority': 'high'
            }
        },
        'AWS': {
            'beginner': {
                'title': 'Get AWS Cloud Practitioner Certification',
                'description': 'Study and pass the AWS Cloud Practitioner exam',
                'estimated_hours': 15,
                'timeline': 'Week 1-2',
                'priority': 'high'
            },
            'intermediate': {
                'title': 'Deploy Application Using AWS Services',
                'description': 'Deploy a real application using EC2, S3, and other AWS services',
                'estimated_hours': 20,
                'timeline': 'Week 2-4',
                'priority': 'high'
            }
        },
        'Docker': {
            'beginner': {
                'title': 'Learn Docker Fundamentals',
                'description': 'Understand containers, images, and basic Docker commands',
                'estimated_hours': 15,
                'timeline': 'Week 1-2',
                'priority': 'medium'
            },
            'intermediate': {
                'title': 'Containerize Your Applications',
                'description': 'Dockerize existing applications and create multi-container setups',
                'estimated_hours': 20,
                'timeline': 'Week 2-4',
                'priority': 'medium'
            }
        },
        'Kubernetes': {
            'beginner': {
                'title': 'Learn Kubernetes Basics',
                'description': 'Understand pods, services, deployments, and basic kubectl commands',
                'estimated_hours': 20,
                'timeline': 'Week 2-4',
                'priority': 'medium'
            }
        },
        'Git': {
            'beginner': {
                'title': 'Master Git Fundamentals',
                'description': 'Learn version control, branching, merging, and collaboration',
                'estimated_hours': 10,
                'timeline': 'Week 1',
                'priority': 'medium'
            },
            'intermediate': {
                'title': 'Advanced Git Workflows',
                'description': 'Learn Git hooks, rebasing, and advanced collaboration techniques',
                'estimated_hours': 15,
                'timeline': 'Week 1-2',
                'priority': 'low'
            }
        }
    }
    
    def __init__(self):
        self.gap_analyzer = GapAnalyzer()
    
    def generate_action_plan(self, analysis_id: int, skill_gaps: List[Dict]) -> Dict[str, Any]:
        """Generate a comprehensive action plan from skill gaps"""
        
        tasks = []
        total_hours = 0
        
        # Sort gaps by importance (critical first)
        importance_order = {'critical': 0, 'high': 1, 'preferred': 2}
        sorted_gaps = sorted(skill_gaps, key=lambda x: importance_order.get(x.get('importance', 'preferred'), 3))
        
        for gap in sorted_gaps:
            skill_name = gap['skill']
            gap_type = gap.get('type', 'missing')
            
            if gap_type == 'missing':
                # Generate task for missing skill
                task = self._create_task_for_missing_skill(skill_name, gap)
            elif gap_type == 'level_gap':
                # Generate task for skill improvement
                task = self._create_task_for_skill_improvement(skill_name, gap)
            else:
                continue
            
            if task:
                tasks.append(task)
                total_hours += task['estimated_hours']
        
        # Calculate timeline
        timeline = self._calculate_timeline(total_hours)
        
        # Generate summary
        summary = self._generate_plan_summary(tasks, total_hours, timeline)
        
        return {
            'analysis_id': analysis_id,
            'tasks': tasks,
            'total_hours': total_hours,
            'timeline': timeline,
            'summary': summary,
            'completed_tasks': [],
            'updated_readiness_score': None
        }
    
    def _create_task_for_missing_skill(self, skill_name: str, gap: Dict) -> Optional[Dict]:
        """Create a task for a completely missing skill"""
        
        # Determine target level based on job requirements
        target_level = self._determine_target_level(gap)
        
        # Get task template
        task_template = self.TASK_TEMPLATES.get(skill_name, {}).get(target_level)
        if not task_template:
            # Create generic task if no template exists
            task_template = {
                'title': f'Learn {skill_name}',
                'description': f'Study and practice {skill_name} to meet job requirements',
                'estimated_hours': 20,
                'timeline': 'Week 1-3',
                'priority': gap.get('importance', 'preferred')
            }
        
        # Get learning resources
        resources = self._get_learning_resources(skill_name, target_level)
        
        return {
            'id': f"task_{skill_name.lower().replace(' ', '_')}_{target_level}",
            'skill': skill_name,
            'title': task_template['title'],
            'description': task_template['description'],
            'estimated_hours': task_template['estimated_hours'],
            'timeline': task_template['timeline'],
            'priority': gap.get('importance', 'preferred'),
            'target_level': target_level,
            'resources': resources,
            'completed': False
        }
    
    def _create_task_for_skill_improvement(self, skill_name: str, gap: Dict) -> Optional[Dict]:
        """Create a task for improving an existing skill"""
        
        current_level = gap.get('current_level', 'basic')
        target_level = gap.get('target_level', 'intermediate')
        
        # Get task template for improvement
        task_template = self.TASK_TEMPLATES.get(skill_name, {}).get(target_level)
        if not task_template:
            task_template = {
                'title': f'Improve {skill_name} from {current_level} to {target_level}',
                'description': f'Enhance your {skill_name} skills to reach {target_level} level',
                'estimated_hours': 15,
                'timeline': 'Week 1-2',
                'priority': gap.get('importance', 'preferred')
            }
        
        # Get learning resources
        resources = self._get_learning_resources(skill_name, target_level)
        
        return {
            'id': f"task_{skill_name.lower().replace(' ', '_')}_{target_level}",
            'skill': skill_name,
            'title': task_template['title'],
            'description': task_template['description'],
            'estimated_hours': task_template['estimated_hours'],
            'timeline': task_template['timeline'],
            'priority': gap.get('importance', 'preferred'),
            'current_level': current_level,
            'target_level': target_level,
            'resources': resources,
            'completed': False
        }
    
    def _determine_target_level(self, gap: Dict) -> str:
        """Determine the target skill level based on job requirements"""
        # Default to intermediate for most skills
        return 'intermediate'
    
    def _get_learning_resources(self, skill_name: str, target_level: str) -> List[Dict]:
        """Get learning resources prioritizing LinkedIn Learning and official docs"""
        resources = []
        
        # Add official documentation first (always available)
        official_docs = self._get_official_documentation(skill_name)
        if official_docs:
            resources.append({
                'name': f"Official Documentation: {skill_name}",
                'url': official_docs,
                'type': 'documentation',
                'platform': 'Official',
                'priority': 'reference'
            })
        
        # Try LinkedIn Learning second (premium structured learning)
        linkedin_course = self.LINKEDIN_LEARNING_COURSES.get(skill_name, {}).get(target_level)
        if linkedin_course:
            resources.append({
                'name': f"LinkedIn Learning: {linkedin_course['title']}",
                'url': linkedin_course['url'],
                'type': 'course',
                'platform': 'LinkedIn Learning',
                'duration': linkedin_course['duration'],
                'instructor': linkedin_course['instructor'],
                'priority': 'primary'
            })
        
        # Add YouTube as backup (free alternative)
        youtube_resource = self.YOUTUBE_RESOURCES.get(skill_name, {}).get(target_level)
        if youtube_resource:
            resources.append({
                'name': f"YouTube: {youtube_resource['title']}",
                'url': youtube_resource['url'],
                'type': 'video',
                'platform': 'YouTube',
                'channel': youtube_resource['channel'],
                'duration': youtube_resource['duration'],
                'priority': 'secondary'
            })
        
        return resources
    
    def _get_official_documentation(self, skill_name: str) -> Optional[str]:
        """Get official documentation URLs for skills"""
        docs_mapping = {
            'Python': 'https://docs.python.org/3/',
            'React': 'https://react.dev/',
            'Django': 'https://docs.djangoproject.com/',
            'AWS': 'https://docs.aws.amazon.com/',
            'Docker': 'https://docs.docker.com/',
            'Kubernetes': 'https://kubernetes.io/docs/',
            'Git': 'https://git-scm.com/doc',
            'JavaScript': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
            'SQL': 'https://www.w3schools.com/sql/'
        }
        return docs_mapping.get(skill_name)
    
    def _calculate_timeline(self, total_hours: int) -> str:
        """Calculate realistic timeline based on total hours"""
        # Assume 10 hours per week for learning
        weeks = max(1, round(total_hours / 10))
        
        if weeks == 1:
            return "1 week"
        elif weeks <= 4:
            return f"{weeks} weeks"
        else:
            months = round(weeks / 4, 1)
            return f"{months} months"
    
    def _generate_plan_summary(self, tasks: List[Dict], total_hours: int, timeline: str) -> Dict[str, Any]:
        """Generate a summary of the action plan"""
        
        critical_tasks = [t for t in tasks if t['priority'] == 'critical']
        high_priority_tasks = [t for t in tasks if t['priority'] == 'high']
        
        return {
            'total_tasks': len(tasks),
            'critical_tasks': len(critical_tasks),
            'high_priority_tasks': len(high_priority_tasks),
            'total_hours': total_hours,
            'timeline': timeline,
            'focus_areas': list(set([t['skill'] for t in tasks])),
            'recommendations': [
                f"Complete {len(critical_tasks)} critical tasks first",
                f"Allocate {total_hours} hours over {timeline}",
                "Use LinkedIn Learning courses for structured learning",
                "Practice with real projects to reinforce skills"
            ]
        }
