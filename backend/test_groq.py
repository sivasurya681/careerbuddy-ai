import requests
import json

GROQ_API_KEY = ""
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def test_groq_connection():
    """Test connection to Groq API with multiple models"""
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    models = [
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "llama-3.1-8b-instant"
    ]
    
    print("🔍 Testing Groq API Connection...")
    print("=" * 50)
    
    for model in models:
        try:
            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "Say 'Hello from CareerBuddy!' in one short sentence"}
                ],
                "temperature": 0.7,
                "max_tokens": 50
            }
            
            print(f"\n📡 Testing model: {model}")
            response = requests.post(GROQ_ENDPOINT, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                message = result["choices"][0]["message"]["content"]
                print(f"✅ SUCCESS: {message}")
                return True
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n⚠️ All models failed. Using fallback responses.")
    return False

if __name__ == "__main__":
    test_groq_connection()