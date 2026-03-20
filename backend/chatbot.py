import requests
import json
import time
import re
import os
from dotenv import load_dotenv

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("⚠️ Warning: GROQ_API_KEY not found in environment variables")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

ALLOWED_TOPICS = {
    "career", "job", "role", "certificate", "certification", "resume", "cv",
    "interview", "salary", "skills", "learning", "learn", "language", "coding", 
    "code", "courses", "education", "hiring", "recruitment", "linkedin", "udemy", 
    "coursera", "promotion", "offer letter", "internship", "training", 
    "professional growth", "remote job", "on-site job", "work-life balance", 
    "career advice", "networking", "job portal", "freelancing", "project management", 
    "personal branding", "career switch", "mock interview", "job fair", "career goals", 
    "career planning", "career growth", "self improvement", "technical skills", 
    "soft skills", "leadership", "team management", "communication skills", 
    "negotiation skills", "online courses", "job search", "employee benefits", 
    "job responsibilities", "career mentoring", "industry trends", "job descriptions", 
    "performance review", "appraisal", "job openings", "career change", "headhunting", 
    "job satisfaction", "career counseling", "employment opportunities", "career achievements", 
    "job vacancies", "career objectives", "cover letter", "professional resume", 
    "career advancement", "industry certification", "career seminars", "career workshops", 
    "career webinars", "career conferences", "resume writing", "career breaks", 
    "career tips", "career coaching", "skill enhancement", "portfolio building", 
    "professional branding", "job relocation", "career transition", "online learning", 
    "career consultation", "company culture", "personal development", "employer expectations", 
    "career exposure", "salary negotiation", "career evaluation", "career challenges", 
    "industry networking", "career pathways", "career flexibility", "career roadmap", 
    "career decisions", "career resources", "career forums", "career blogs", 
    "career opportunities", "career fairs", "career partnerships", "career references", 
    "career highlights", "job offers"
}

# Fallback responses for when API is unavailable
FALLBACK_RESPONSES = {
    "salary": {
        "india": "In India, average salaries:\n• Entry Level: ₹3-6 LPA\n• Mid Level: ₹6-15 LPA\n• Senior Level: ₹15-30 LPA\n• Full Stack Developer: ₹6-18 LPA depending on experience",
        "us": "In the US, average salaries:\n• Entry Level: $60,000-80,000\n• Mid Level: $80,000-120,000\n• Senior Level: $120,000-160,000+",
        "uk": "In the UK, average salaries:\n• Entry Level: £25,000-35,000\n• Mid Level: £35,000-55,000\n• Senior Level: £55,000-80,000+"
    },
    "skills": {
        "web_dev": "Essential web development skills:\n• Frontend: HTML, CSS, JavaScript, React/Vue/Angular\n• Backend: Python/Java/Node.js, SQL, APIs\n• Tools: Git, Docker, AWS",
        "data_science": "Essential data science skills:\n• Programming: Python, SQL\n• Libraries: Pandas, NumPy, Scikit-learn\n• ML/DL: TensorFlow, PyTorch\n• Statistics & Mathematics",
        "devops": "Essential DevOps skills:\n• Tools: Docker, Kubernetes, Jenkins\n• Cloud: AWS/Azure/GCP\n• IaC: Terraform, Ansible"
    },
    "interview": "Interview preparation tips:\n1. Research the company\n2. Practice common questions\n3. Prepare your own questions\n4. Review fundamentals\n5. Do mock interviews",
    "resume": "Resume tips:\n• Keep it to 1-2 pages\n• Use action verbs\n• Quantify achievements\n• Tailor to each job\n• Include relevant skills\n• Proofread carefully",
    "default": "I'm your career assistant! I can help with:\n• Salary information\n• Skills required\n• Interview preparation\n• Resume tips\n• Career advice\n\nWhat would you like to know?"
}

def is_valid_query(user_input):
    """Check if the query is career-related"""
    user_input_lower = user_input.lower()
    return any(topic in user_input_lower for topic in ALLOWED_TOPICS)

def get_fallback_response(query):
    """Get fallback response based on query keywords"""
    query_lower = query.lower()
    
    # Check for location
    location = "global"
    if "india" in query_lower or "inr" in query_lower or "lpa" in query_lower:
        location = "india"
    elif "uk" in query_lower or "london" in query_lower or "pound" in query_lower:
        location = "uk"
    elif "us" in query_lower or "usa" in query_lower or "dollar" in query_lower:
        location = "us"
    
    # Check for salary questions
    if "salary" in query_lower or "pay" in query_lower or "compensation" in query_lower:
        if "full stack" in query_lower or "full-stack" in query_lower:
            if location == "india":
                return "Average Full Stack Developer salary in India:\n• Fresher: ₹4-7 LPA\n• 2-4 years: ₹8-15 LPA\n• 5+ years: ₹18-30 LPA\n\nTop companies pay 20-30% higher."
        return FALLBACK_RESPONSES["salary"].get(location, FALLBACK_RESPONSES["salary"]["us"])
    
    # Check for skills questions
    if "skill" in query_lower or "learn" in query_lower or "need to know" in query_lower:
        if "web" in query_lower or "frontend" in query_lower or "backend" in query_lower:
            return FALLBACK_RESPONSES["skills"]["web_dev"]
        elif "data" in query_lower or "machine learning" in query_lower or "ai" in query_lower:
            return FALLBACK_RESPONSES["skills"]["data_science"]
        elif "devops" in query_lower or "cloud" in query_lower:
            return FALLBACK_RESPONSES["skills"]["devops"]
    
    # Check for interview questions
    if "interview" in query_lower:
        return FALLBACK_RESPONSES["interview"]
    
    # Check for resume questions
    if "resume" in query_lower or "cv" in query_lower:
        return FALLBACK_RESPONSES["resume"]
    
    return FALLBACK_RESPONSES["default"]

def get_groq_response(prompt):
    """Get response from Groq's model with multiple model fallbacks"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # List of current Groq models in order of preference
    models = [
        "llama-3.3-70b-versatile",  # Current Llama 3.3 70B (recommended)
        "mixtral-8x7b-32768",       # Mixtral
        "gemma2-9b-it",              # Google's Gemma 2
        "llama-3.1-8b-instant"       # Llama 3.1 8B (fast)
    ]
    
    system_message = """You are CareerBuddy AI, a helpful career assistant. 
    Provide concise, practical advice about careers, jobs, and professional development.
    Keep responses under 150 words. Be friendly and encouraging.
    Focus on accurate, up-to-date career information."""
    
    for model in models:
        try:
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300,
                "top_p": 0.9
            }
            
            time.sleep(0.5)  # Rate limiting
            response = requests.post(GROQ_ENDPOINT, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            elif response.status_code == 400:
                # Model might be deprecated, try next
                print(f"Model {model} failed, trying next...")
                continue
            else:
                print(f"Groq API error {response.status_code} with {model}")
                continue
                
        except requests.exceptions.Timeout:
            print(f"Timeout with model {model}")
            continue
        except requests.exceptions.ConnectionError:
            print(f"Connection error with model {model}")
            continue
        except Exception as e:
            print(f"Error with model {model}: {e}")
            continue
    
    # If all models fail, use fallback
    print("All Groq models failed, using fallback response")
    return get_fallback_response(prompt)

def get_chatbot_response(query):
    """Main function to get chatbot response"""
    if not query or not query.strip():
        return [{"type": "text", "content": "Please enter a question about careers, jobs, or skills."}]
    
    # Check if query is career-related
    if not is_valid_query(query):
        return [{
            "type": "text", 
            "content": "I specialize in career-related questions. Feel free to ask about:\n• Job salaries\n• Required skills\n• Interview tips\n• Resume advice\n• Career paths\n• Professional development"
        }]
    
    # Get response from Groq or fallback
    answer = get_groq_response(query)
    
    # Parse response into structured format
    responses = []
    lines = answer.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for bullet points
        if line.startswith("- ") or line.startswith("•") or line.startswith("* "):
            content = line[2:].strip()
            if content:
                responses.append({
                    "type": "bullet",
                    "content": content
                })
        # Check for numbered lists
        elif re.match(r'^\d+\.', line):
            content = re.sub(r'^\d+\.\s*', '', line)
            if content:
                responses.append({
                    "type": "bullet",
                    "content": content
                })
        # Check for headings (ends with colon)
        elif line.endswith(":"):
            responses.append({
                "type": "heading",
                "content": line
            })
        # Regular text
        else:
            # Split long text into sentences for better display
            sentences = re.split(r'(?<=[.!?])\s+', line)
            for sentence in sentences:
                if sentence.strip():
                    responses.append({
                        "type": "text",
                        "content": sentence.strip()
                    })
    
    # If no structured responses, return the whole answer as text
    if not responses:
        responses = [{"type": "text", "content": answer}]
    
    return responses

if __name__ == "__main__":
    print("Career Chatbot (Type 'exit' to quit)")
    print("Testing connection to Groq API...")
    
    # Test API connection
    test_response = get_groq_response("Say 'Hello' in one word")
    print(f"API Test: {test_response[:50]}...\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting Chatbot. Goodbye!")
            break
        responses = get_chatbot_response(user_input)
        print("\nCareerBuddy:")
        for r in responses:
            print(f"  {r['content']}")
        print()