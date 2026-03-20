import os
import requests
import PyPDF2
from bs4 import BeautifulSoup
import json
import time
import re
import os
from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️ Warning: GROQ_API_KEY not found in environment variables")

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"--- Page {page_num + 1} ---\n{page_text}\n"
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text.strip()

def extract_skills_with_groq(resume_text):
    """Extract skills from resume using Groq with multiple model fallbacks"""
    if not GROQ_API_KEY:
        print("No Groq API key found, using fallback extraction")
        return extract_skills_fallback(resume_text)
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Truncate text if too long
    if len(resume_text) > 4000:
        resume_text = resume_text[:4000]
    
    prompt = f"""Extract technical and professional skills from this resume. 
Return ONLY a JSON array of skills, nothing else.
Focus on: programming languages, frameworks, tools, technologies, soft skills.

Example format: ["Python", "JavaScript", "React", "Project Management", "Team Leadership"]

Resume text:
{resume_text}
"""
    
    # List of current Groq models
    models = [
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "llama-3.1-8b-instant"
    ]
    
    for model in models:
        try:
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a resume parsing expert. Extract skills accurately and return only JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 300
            }
            
            time.sleep(0.5)  # Rate limiting
            response = requests.post(GROQ_ENDPOINT, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Try to parse JSON from response
                try:
                    # Find JSON array in the response
                    json_match = re.search(r'\[.*\]', content, re.DOTALL)
                    if json_match:
                        skills = json.loads(json_match.group())
                        if isinstance(skills, list) and skills:
                            return skills
                except:
                    # Fallback: extract skills by splitting
                    skills = re.findall(r'"([^"]*)"', content)
                    if skills:
                        return skills
            elif response.status_code == 400:
                print(f"Model {model} failed, trying next...")
                continue
            else:
                print(f"API error {response.status_code} with {model}")
                continue
                
        except Exception as e:
            print(f"Error with model {model}: {e}")
            continue
    
    print("All Groq models failed, using fallback extraction")
    return extract_skills_fallback(resume_text)

def extract_skills_fallback(resume_text):
    """Fallback method to extract skills using keyword matching"""
    common_skills = [
        "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "swift", "kotlin",
        "react", "angular", "vue", "node.js", "express", "django", "flask", "spring", "asp.net",
        "html", "css", "sass", "less", "bootstrap", "tailwind",
        "sql", "mysql", "postgresql", "mongodb", "oracle", "redis", "elasticsearch",
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "github", "gitlab",
        "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
        "data science", "data analysis", "data visualization", "tableau", "power bi",
        "project management", "agile", "scrum", "jira", "confluence",
        "leadership", "communication", "teamwork", "problem solving", "critical thinking"
    ]
    
    found_skills = []
    text_lower = resume_text.lower()
    
    for skill in common_skills:
        if skill in text_lower:
            # Capitalize properly
            if skill in ["c++", "c#", "node.js", "asp.net"]:
                found_skills.append(skill.upper())
            elif skill in ["sql", "html", "css", "aws", "gcp"]:
                found_skills.append(skill.upper())
            else:
                found_skills.append(skill.title())
    
    # Remove duplicates and return
    return list(set(found_skills))[:15]

def get_job_search_links(skill):
    """Get job search links for a skill"""
    encoded_skill = skill.replace(' ', '%20')
    return [
        f"https://www.linkedin.com/jobs/search?keywords={encoded_skill}",
        f"https://www.indeed.com/jobs?q={skill.replace(' ', '+')}",
        f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={encoded_skill}"
    ]

def parse_resume(pdf_path):
    """Main function to parse resume and find matching jobs"""
    if not os.path.exists(pdf_path):
        return {
            "error": "File not found",
            "extracted_skills": [],
            "matched_jobs": {}
        }
    
    # Extract text from PDF
    resume_text = extract_text_from_pdf(pdf_path)
    if not resume_text or len(resume_text) < 50:
        return {
            "error": "Could not extract sufficient text from PDF",
            "extracted_skills": [],
            "matched_jobs": {}
        }
    
    print(f"Extracted {len(resume_text)} characters from PDF")
    
    # Extract skills
    extracted_skills = extract_skills_with_groq(resume_text)
    
    # If no skills found, use fallback
    if not extracted_skills:
        extracted_skills = extract_skills_fallback(resume_text)
    
    print(f"Found {len(extracted_skills)} skills: {extracted_skills[:5]}")
    
    # Find jobs for each skill (limited to top 5 skills)
    matched_jobs = {}
    for skill in extracted_skills[:5]:
        job_links = get_job_search_links(skill)
        matched_jobs[skill] = job_links
    
    return {
        "extracted_skills": extracted_skills,
        "matched_jobs": matched_jobs,
        "message": "Resume parsed successfully"
    }

if __name__ == "__main__":
    # Test the parser
    test_file = "test_resume.pdf"
    if os.path.exists(test_file):
        print(f"Testing resume parser with {test_file}...")
        result = parse_resume(test_file)
        print(json.dumps(result, indent=2))
    else:
        print(f"Test file {test_file} not found")
        print("Creating a sample test_resume.pdf would be helpful for testing")