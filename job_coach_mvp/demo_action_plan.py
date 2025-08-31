#!/usr/bin/env python3
"""
Demo script for Action Plan Generator
Shows the personalized action plan generation with LinkedIn Learning resources
"""

from action_plan_generator import ActionPlanGenerator

def main():
    print("🎯 Action Plan Generator Demo")
    print("=" * 50)
    
    # Sample skill gaps from our previous analysis
    skill_gaps = [
        {
            'skill': 'Kubernetes',
            'importance': 'critical',
            'type': 'missing',
            'description': 'Missing Kubernetes - critical skill'
        },
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
    
    print("\n📊 Sample Skill Gaps:")
    print("-" * 30)
    for gap in skill_gaps:
        print(f"  - {gap['skill']} ({gap['importance']}): {gap['description']}")
    
    # Initialize action plan generator
    generator = ActionPlanGenerator()
    
    print("\n🔧 Generating Action Plan...")
    print("-" * 30)
    
    # Generate action plan
    action_plan = generator.generate_action_plan(1, skill_gaps)
    
    print(f"✅ Action Plan Generated!")
    print(f"📅 Timeline: {action_plan['timeline']}")
    print(f"⏱ Total Hours: {action_plan['total_hours']}")
    print(f"📋 Total Tasks: {len(action_plan['tasks'])}")
    
    print("\n📋 Generated Tasks:")
    print("-" * 30)
    
    for i, task in enumerate(action_plan['tasks'], 1):
        print(f"\n{i}. {task['title']}")
        print(f"   Skill: {task['skill']}")
        print(f"   Priority: {task['priority']}")
        print(f"   Timeline: {task['timeline']}")
        print(f"   Hours: {task['estimated_hours']}")
        print(f"   Description: {task['description']}")
        
        if task['resources']:
            print("   📚 Learning Resources:")
            for resource in task['resources']:
                platform_icon = "🔵" if resource['platform'] == 'LinkedIn Learning' else "🔴" if resource['platform'] == 'YouTube' else "📖"
                print(f"      {platform_icon} {resource['name']}")
                if resource.get('duration'):
                    print(f"         Duration: {resource['duration']}")
                if resource.get('instructor'):
                    print(f"         Instructor: {resource['instructor']}")
    
    print("\n📈 Plan Summary:")
    print("-" * 30)
    summary = action_plan['summary']
    print(f"  • Total Tasks: {summary['total_tasks']}")
    print(f"  • Critical Tasks: {summary['critical_tasks']}")
    print(f"  • High Priority Tasks: {summary['high_priority_tasks']}")
    print(f"  • Focus Areas: {', '.join(summary['focus_areas'])}")
    print(f"  • Timeline: {summary['timeline']}")
    print(f"  • Total Hours: {summary['total_hours']}")
    
    print("\n💡 Recommendations:")
    print("-" * 30)
    for rec in summary['recommendations']:
        print(f"  • {rec}")
    
    print("\n🎯 Key Features Demonstrated:")
    print("-" * 30)
    print("  ✅ LinkedIn Learning prioritization")
    print("  ✅ YouTube as backup resources")
    print("  ✅ Official documentation links")
    print("  ✅ Priority-based task ordering")
    print("  ✅ Realistic time estimates")
    print("  ✅ Skill level progression")
    print("  ✅ Comprehensive learning paths")
    
    print("\n✅ Action Plan Generator Demo Completed!")
    print("\nTo test the full web application:")
    print("  python3 app.py")
    print("  Then visit: http://localhost:5000")

if __name__ == "__main__":
    main()
