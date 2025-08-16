"""
Smart JSON Format Converter
Converts various JSON formats to the standard candidate preference format
"""

import json
import re
from typing import Dict, List, Any, Optional

def extract_skills_from_text(text: str) -> List[str]:
    """Extract skills from a text description"""
    # Common programming languages and technologies
    tech_keywords = [
        'javascript', 'python', 'java', 'react', 'angular', 'vue', 'node.js', 'nodejs',
        'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql', 'aws', 'azure', 'docker',
        'kubernetes', 'git', 'jenkins', 'django', 'flask', 'spring', 'express',
        'typescript', 'php', 'ruby', 'go', 'rust', 'c++', 'c#', 'swift', 'kotlin',
        'figma', 'sketch', 'photoshop', 'illustrator', 'tableau', 'power bi', 'excel',
        'machine learning', 'ai', 'data science', 'devops', 'agile', 'scrum'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in tech_keywords:
        if skill in text_lower:
            # Capitalize properly
            if skill == 'javascript':
                found_skills.append('JavaScript')
            elif skill == 'nodejs' or skill == 'node.js':
                found_skills.append('Node.js')
            elif skill == 'c++':
                found_skills.append('C++')
            elif skill == 'c#':
                found_skills.append('C#')
            else:
                found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates

def extract_salary_from_text(text: str) -> int:
    """Extract salary number from text"""
    # Look for numbers in various formats
    salary_patterns = [
        r'(\d+)k',  # 100k
        r'(\d+),(\d+)',  # 100,000
        r'(\d{4,})',  # 100000
    ]
    
    for pattern in salary_patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            if isinstance(matches[0], tuple):
                # Handle comma-separated numbers
                return int(''.join(matches[0]))
            else:
                num = int(matches[0])
                if 'k' in text.lower():
                    return num * 1000
                return num
    
    return 0

def detect_format_type(data: Dict) -> str:
    """Detect what type of JSON format this is"""
    # Check for job posting format
    if 'jobTitle' in data or 'company' in data:
        return 'job_posting'
    
    # Check for candidate profile format
    if 'name' in data or 'profile' in data or 'resume' in data:
        return 'candidate_profile'
    
    # Check for standard preference format
    if 'values' in data and 'skills' in data:
        return 'standard_preferences'
    
    # Check for simplified format
    if any(key in data for key in ['skills', 'experience', 'location', 'salary']):
        return 'simple_format'
    
    return 'unknown'

def convert_job_posting_to_preferences(data: Dict) -> Dict:
    """Convert job posting format to candidate preferences"""
    preferences = {
        "values": ["Learning & Growth", "Innovation & Creativity", "Team Collaboration"],
        "role_types": ["Full-Time"],
        "titles": [],
        "locations": [],
        "role_level": ["Mid-Level (3 to 5 years)"],
        "leadership_preference": "Individual Contributor",
        "company_size": ["51-200 Employees"],
        "industries": ["Technology"],
        "skills": [],
        "min_salary": 0
    }
    
    # Extract job title
    if 'jobTitle' in data:
        preferences['titles'] = [data['jobTitle']]
    elif 'title' in data:
        preferences['titles'] = [data['title']]
    
    # Extract location
    if 'company' in data and isinstance(data['company'], dict) and 'location' in data['company']:
        preferences['locations'] = [data['company']['location']]
    elif 'location' in data:
        preferences['locations'] = [data['location']]
    
    # Extract skills from requirements
    if 'requirements' in data and 'skills' in data['requirements']:
        skills_text = ' '.join(data['requirements']['skills'])
        preferences['skills'] = extract_skills_from_text(skills_text)
    
    # Extract skills from job description
    if 'jobDescription' in data:
        desc_skills = extract_skills_from_text(data['jobDescription'])
        preferences['skills'].extend(desc_skills)
    
    # Remove duplicates
    preferences['skills'] = list(set(preferences['skills']))
    
    # Extract salary
    if 'salary' in data:
        if isinstance(data['salary'], dict) and 'range' in data['salary']:
            salary_text = data['salary']['range']
            preferences['min_salary'] = extract_salary_from_text(salary_text)
    
    # Extract employment type
    if 'employmentType' in data:
        emp_type = data['employmentType']
        if 'full' in emp_type.lower():
            preferences['role_types'] = ['Full-Time']
        elif 'part' in emp_type.lower():
            preferences['role_types'] = ['Part-Time']
        elif 'contract' in emp_type.lower():
            preferences['role_types'] = ['Contract']
    
    return preferences

def convert_candidate_profile_to_preferences(data: Dict) -> Dict:
    """Convert candidate profile format to preferences"""
    preferences = {
        "values": ["Learning & Growth", "Career Development", "Work-Life Balance"],
        "role_types": ["Full-Time"],
        "titles": [],
        "locations": ["Remote"],
        "role_level": ["Mid-Level (3 to 5 years)"],
        "leadership_preference": "Individual Contributor",
        "company_size": ["51-200 Employees", "201-500 Employees"],
        "industries": ["Technology"],
        "skills": [],
        "min_salary": 0
    }
    
    # Extract from profile data
    if 'skills' in data:
        if isinstance(data['skills'], list):
            preferences['skills'] = data['skills']
        elif isinstance(data['skills'], str):
            preferences['skills'] = extract_skills_from_text(data['skills'])
    
    if 'experience' in data:
        exp_text = str(data['experience']).lower()
        if 'senior' in exp_text or '5' in exp_text:
            preferences['role_level'] = ['Senior (5 to 8 years)']
        elif 'junior' in exp_text or '1' in exp_text or '2' in exp_text:
            preferences['role_level'] = ['Entry-Level (0 to 2 years)']
    
    if 'location' in data:
        preferences['locations'] = [data['location']]
    
    if 'salary' in data or 'expectedSalary' in data:
        salary_data = data.get('salary', data.get('expectedSalary', ''))
        preferences['min_salary'] = extract_salary_from_text(str(salary_data))
    
    return preferences

def convert_simple_format_to_preferences(data: Dict) -> Dict:
    """Convert simple/flexible format to preferences"""
    preferences = {
        "values": ["Innovation & Creativity", "Learning & Growth", "Team Collaboration"],
        "role_types": ["Full-Time"],
        "titles": ["Software Engineer", "Developer"],
        "locations": ["Remote"],
        "role_level": ["Mid-Level (3 to 5 years)"],
        "leadership_preference": "Individual Contributor",
        "company_size": ["51-200 Employees"],
        "industries": ["Technology"],
        "skills": [],
        "min_salary": 0
    }
    
    # Direct mapping for common fields
    field_mappings = {
        'skills': 'skills',
        'technologies': 'skills',
        'tech_stack': 'skills',
        'location': 'locations',
        'locations': 'locations',
        'preferred_location': 'locations',
        'salary': 'min_salary',
        'min_salary': 'min_salary',
        'expected_salary': 'min_salary',
        'job_title': 'titles',
        'titles': 'titles',
        'roles': 'titles',
        'industry': 'industries',
        'industries': 'industries',
        'company_size': 'company_size',
        'values': 'values',
        'work_values': 'values'
    }
    
    for key, value in data.items():
        if key in field_mappings:
            pref_key = field_mappings[key]
            
            if pref_key in ['skills', 'locations', 'titles', 'industries', 'company_size', 'values']:
                if isinstance(value, list):
                    preferences[pref_key] = value
                elif isinstance(value, str):
                    if pref_key == 'skills':
                        preferences[pref_key] = extract_skills_from_text(value)
                    else:
                        preferences[pref_key] = [value]
            elif pref_key == 'min_salary':
                if isinstance(value, (int, float)):
                    preferences[pref_key] = int(value)
                else:
                    preferences[pref_key] = extract_salary_from_text(str(value))
    
    return preferences

def smart_convert(json_input: str) -> Dict:
    """Smart converter that handles any JSON format"""
    try:
        data = json.loads(json_input)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    
    # Detect format type
    format_type = detect_format_type(data)
    
    # Convert based on detected format
    if format_type == 'job_posting':
        return convert_job_posting_to_preferences(data)
    elif format_type == 'candidate_profile':
        return convert_candidate_profile_to_preferences(data)
    elif format_type == 'simple_format':
        return convert_simple_format_to_preferences(data)
    elif format_type == 'standard_preferences':
        return data  # Already in correct format
    else:
        # Try to extract whatever we can
        return convert_simple_format_to_preferences(data)

# Test function
if __name__ == "__main__":
    # Test with job posting format
    job_posting = '''
    {
        "jobTitle": "Software Engineer",
        "company": {
            "name": "Tech Innovators Inc.",
            "location": "Chennai, Tamil Nadu, India"
        },
        "requirements": {
            "skills": ["JavaScript", "Python", "React"]
        },
        "salary": {
            "range": "600000-1200000"
        }
    }
    '''
    
    result = smart_convert(job_posting)
    print("Converted preferences:", json.dumps(result, indent=2))