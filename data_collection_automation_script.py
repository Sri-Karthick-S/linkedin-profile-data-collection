import requests, csv, re, time, os

API_KEY = open("API_KEY").read().strip()
SEARCH_ENGINE_ID = open("SEARCH_ENGINE_ID").read().strip()

ROLE_KEYWORDS = {
    "tech": [
        "Junior Software Engineer", "Associate Software Engineer", "Data Analyst",
        "Business Intelligence Analyst", "Cloud Support Associate", "IT Support Engineer",
        "Software Engineer", "Full Stack Developer", "Backend Developer",
        "Frontend Engineer", "Data Engineer", "Machine Learning Engineer", "DevOps Engineer",
        "Cloud Engineer", "Cloud Architect", "Product Manager", "Associate Product Manager",
        "Senior Software Engineer", "Senior Data Scientist", "AI Engineer", "NLP Engineer",
        "Computer Vision Engineer", "Solutions Architect", "Engineering Manager",
        "Senior Product Manager", "Program Manager", "Director of Engineering",
        "VP of Engineering", "CTO", "CDO", "Head of Product" # 31 roles
    ],
    "consulting": [
        "Business Analyst", "Associate Consultant", "Junior Consultant",
        "Research Analyst", "Consultant", "Strategy Consultant", "Management Consultant",
        "Advisory Consultant", "Engagement Consultant", "Senior Consultant",
        "Project Manager Consulting", "Engagement Manager", "Advisory Manager",
        "Practice Manager", "Partner", "Principal Consultant",
        "Director of Consulting", "Managing Director Consulting" # 18 roles
    ],
    "entrepreneurship": [
        "Founder", "Co-founder", "Startup Founder", "Entrepreneur-in-Residence",
        "Product Founder", "Startup CEO", "Small Business Owner", "Managing Partner",
        "Managing Director", "CEO", "COO", "CMO" # 12 roles
    ]
}

# Total roles = 61
# Total profiles = 183

CATEGORY_KEYWORDS = {
    "tech": {
        "certs": ["AWS Certified", "Azure Certified", "Google Cloud Certified",
                  "Snowflake Certified", "Databricks Certified",
                  "Certified Kubernetes Administrator", "Cisco Certified",
                  "CompTIA", "Oracle Certified", "Microsoft Certified"],
        "skills": ["Python", "SQL", "Java", "C++", "C#", "JavaScript", "TypeScript",
                   "React", "Node.js", "Django", "Flask", "Spring Boot",
                   "Machine Learning", "Deep Learning", "Artificial Intelligence",
                   "TensorFlow", "PyTorch", "NLP", "Computer Vision",
                   "Data Engineering", "ETL", "Data Warehousing", "Snowflake",
                   "Big Data", "Hadoop", "Spark", "Kafka",
                   "Cloud", "AWS", "Azure", "GCP", "DevOps", "Kubernetes", "Docker",
                   "Agile", "Scrum", "CI/CD"]
    },
    "consulting": {
        "certs": ["PMP", "PRINCE2", "Scrum Master", "Agile Certified",
                  "Lean Six Sigma", "CFA", "CPA", "CIMA", "FRM", "MBA"],
        "skills": ["Business Analysis", "Management Consulting", "Strategy",
                   "Financial Modeling", "Valuation", "Risk Analysis", "Stakeholder Engagement",
                   "Process Improvement", "Change Management", "Operations Consulting",
                   "Advisory", "Corporate Finance", "M&A", "Market Research",
                   "Excel", "PowerPoint", "Tableau", "Power BI", "SQL",
                   "Leadership", "Client Management", "Presentation Skills"]
    },
    "entrepreneurship": {
        "certs": ["MBA", "Entrepreneurship Certificate", "Y Combinator",
                  "Techstars", "Founder Institute", "Startup School", "Accelerator Program"],
        "skills": ["Entrepreneurship", "Startup", "Founder", "CEO",
                   "Business Development", "Fundraising", "Venture Capital",
                   "Seed Funding", "Series A", "Investor Relations",
                   "Growth Strategy", "Product Launch", "Go-To-Market",
                   "Marketing Strategy", "Sales Strategy", "Networking",
                   "Leadership", "Team Building", "Innovation", "Pitching"]
    }
}

def google_search(query, num=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": API_KEY, "cx": SEARCH_ENGINE_ID, "num": num}
    response = requests.get(url, params=params)
    return response.json()

def score_profile(item, category):
    score = 0
    snippet = item.get("snippet", "").lower()
    title = item.get("title", "").lower()
    certs = CATEGORY_KEYWORDS[category]["certs"]
    skills = CATEGORY_KEYWORDS[category]["skills"]

    for cert in certs:
        if cert.lower() in snippet or cert.lower() in title:
            score += 5
    for skill in skills:
        if skill.lower() in snippet or skill.lower() in title:
            score += 2
    if "500+" in snippet:
        score += 3
    if any(x in title for x in ["vp", "director", "cto", "ceo"]):
        score += 4
    return score

def extract_profiles(role, category, max_profiles=3):
    query = f'site:linkedin.com/in/ "{role}" ("United States" OR "Canada")'
    results = google_search(query, num=10)
    profiles = []
    
    if "items" not in results:
        return profiles
    
    scored_items = sorted(results["items"], key=lambda x: score_profile(x, category), reverse=True)

    for item in scored_items[:max_profiles]:
        url = item["link"]
        if "linkedin.com/in/" not in url:
            continue
        
        username_match = re.search(r"linkedin\.com/in/([^/?]+)", url)
        username = username_match.group(1) if username_match else ""
        
        name = item["title"].split("-")[0].strip()
        snippet = item.get("snippet", "")
        location_match = re.search(r"(United States|Canada|[A-Za-z ]+, [A-Z]{2})", snippet)
        location = location_match.group(0) if location_match else "US/CA"
        
        profiles.append([username, name, location, category, role, url])
    
    return profiles

def save_batch(profiles, filename="linkedin_profiles.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["username", "name", "location", "service_category", "role", "linkedin_url"])
        writer.writerows(profiles)
    print(f"Saved {len(profiles)} profiles to {filename}")

for category, roles in ROLE_KEYWORDS.items():
    for role in roles:
        print(f"\n Collecting profiles for role: {role} ({category})...")
        profiles = extract_profiles(role, category)
        if not profiles:
            print("No profiles found")
            continue
        
        for p in profiles:
            print(f"{p[1]} ({p[2]}) | {p[5]}")
        
        # Save after each role to avoid losing progress
        save_batch(profiles)
        time.sleep(1)  # Overcome API limits