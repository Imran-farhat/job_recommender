from difflib import SequenceMatcher

WEIGHTS = {
    "skills": 0.25,
    "title_role": 0.25,
    "location": 0.15,
    "industry": 0.10,
    "company_size": 0.10,
    "values": 0.10,
    "salary": 0.05,
}

# Helpers
def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

def fuzzy_match_list(target_list, candidate_list, threshold=0.6):
    """Find fuzzy matches between two lists"""
    matches = 0
    total_possible = len(target_list)
    
    if total_possible == 0:
        return 0
    
    for target in target_list:
        best_match = 0
        for candidate in candidate_list:
            match_score = similarity(target, candidate)
            if match_score > best_match:
                best_match = match_score
        
        if best_match >= threshold:
            matches += best_match
    
    return matches / total_possible

def score_skills(prefs, job):
    """Score based on skill matches with fuzzy matching"""
    pref_skills = [s.lower().strip() for s in prefs.get("skills", [])]
    job_skills = [s.lower().strip() for s in job.get("required_skills", [])]
    
    if not pref_skills or not job_skills:
        return 0
    
    # Find exact matches first
    exact_matches = len(set(pref_skills) & set(job_skills))
    
    # Find fuzzy matches for remaining skills
    fuzzy_score = fuzzy_match_list(pref_skills, job_skills, threshold=0.7)
    
    # Combine scores (favor exact matches)
    return min(1.0, (exact_matches / len(pref_skills)) * 0.7 + fuzzy_score * 0.3)

def score_title_role(prefs, job):
    """Score based on job title and role type matches"""
    titles = prefs.get("titles", [])
    role_types = prefs.get("role_types", [])
    score = 0
    
    # Check employment type match
    job_employment = job.get("employment_type", "")
    role_match = 0
    for role_type in role_types:
        if similarity(role_type, job_employment) > 0.8:
            role_match = 1
            break
    score += 0.3 * role_match
    
    # Check title similarity
    job_title = job.get("title", "")
    best_title_match = 0
    for title in titles:
        title_sim = similarity(title, job_title)
        if title_sim > best_title_match:
            best_title_match = title_sim
    
    score += 0.7 * best_title_match
    return min(1.0, score)

def score_location(prefs, job):
    """Score based on location preferences"""
    locations = prefs.get("locations", [])
    job_loc = job.get("location", "")
    
    if not locations:
        return 0
    
    # Handle remote work specifically
    remote_prefs = [loc for loc in locations if "remote" in loc.lower()]
    remote_job = "remote" in job_loc.lower()
    
    if remote_prefs and remote_job:
        return 1.0
    
    # Check city/location matches
    best_match = 0
    for location in locations:
        loc_similarity = similarity(location, job_loc)
        if loc_similarity > best_match:
            best_match = loc_similarity
    
    return best_match

def score_industry(prefs, job):
    """Score based on industry match with fuzzy matching"""
    pref_industries = prefs.get("industries", [])
    job_industry = job.get("industry", "")
    
    if not pref_industries or not job_industry:
        return 0
    
    # Check for exact or fuzzy matches
    for industry in pref_industries:
        if similarity(industry, job_industry) > 0.7:
            return 1.0
    
    return 0

def score_company_size(prefs, job):
    """Score based on company size preference"""
    pref_sizes = prefs.get("company_size", [])
    job_size = job.get("company_size", "")
    
    if not pref_sizes or not job_size:
        return 0
    
    # Check for exact or similar matches
    for size in pref_sizes:
        if similarity(size, job_size) > 0.8:
            return 1.0
    
    return 0

def score_values(prefs, job):
    """Score based on values alignment with fuzzy matching"""
    pref_values = prefs.get("values", [])
    job_values = job.get("values_promoted", [])
    
    if not pref_values or not job_values:
        return 0
    
    matches = 0
    for pref_val in pref_values:
        best_match = 0
        for job_val in job_values:
            val_similarity = similarity(pref_val, job_val)
            if val_similarity > best_match:
                best_match = val_similarity
        
        if best_match > 0.6:  # Lower threshold for values
            matches += best_match
    
    return min(1.0, matches / len(pref_values))

def score_salary(prefs, job):
    """Score based on salary requirements"""
    min_salary = prefs.get("min_salary", 0)
    job_range = job.get("salary_range", [0, 0])
    
    if min_salary == 0:
        return 1.0  # No salary requirement
    
    if len(job_range) >= 2 and min_salary <= job_range[1]:
        # Bonus points if min salary is within the range
        if min_salary >= job_range[0]:
            return 1.0
        else:
            return 0.8  # Meets minimum but below range
    
    return 0

def match_jobs(prefs, jobs):
    """Main matching function"""
    scored = []
    for job in jobs:
        breakdown = {}
        breakdown["skills"] = score_skills(prefs, job)
        breakdown["title_role"] = score_title_role(prefs, job)
        breakdown["location"] = score_location(prefs, job)
        breakdown["industry"] = score_industry(prefs, job)
        breakdown["company_size"] = score_company_size(prefs, job)
        breakdown["values"] = score_values(prefs, job)
        breakdown["salary"] = score_salary(prefs, job)

        # Calculate weighted total score
        total = sum(breakdown[k] * WEIGHTS[k] for k in WEIGHTS)
        
        scored.append({
            "job_id": job["job_id"],
            "job_title": job["title"],
            "company": job["company"],
            "match_score": round(total * 100, 2),
            "breakdown": {k: round(v * 100, 2) for k, v in breakdown.items()}
        })
    
    # Sort by match score (highest first) and limit to top 20
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:20]
