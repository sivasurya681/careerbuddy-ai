import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_all_endpoints():
    """Test all API endpoints"""
    
    print("🚀 Testing CareerBuddy API")
    print("="*60)
    
    # Test 1: Root endpoint
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)
    
    # Test 2: Health check
    response = requests.get(f"{BASE_URL}/api/health")
    print_response("Health Check", response)
    
    # Test 3: Prediction
    response = requests.post(
        f"{BASE_URL}/api/predict",
        json={"skills": "python, machine learning, sql", "role": "data scientist"}
    )
    print_response("Job Prediction", response)
    
    # Test 4: Chatbot
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={"query": "What is the average salary for a Full Stack developer in India?"}
    )
    print_response("Chatbot", response)
    
    # Test 5: LinkedIn jobs
    response = requests.post(
        f"{BASE_URL}/api/linkedin-jobs",
        json={"job_title": "Data Scientist", "num_links": 3}
    )
    print_response("LinkedIn Jobs", response)

if __name__ == "__main__":
    # Wait for server to start
    time.sleep(2)
    test_all_endpoints()