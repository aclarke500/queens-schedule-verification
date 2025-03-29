import requests
import logging

# Use localhost for dev
url = "http://localhost:5000/api/chatbot"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(response):
    logging.error(f"Request to {response.url} failed with status code {response.status_code}")
    logging.error(f"Response content: {response.text}")

def test_chatbot():
    """Test the /api/chatbot endpoint with valid message and history."""
    payload = {
        "message": "What second year CS courses do I need?",
        "history": [
            { "role": "user", "content": "Here are my courses: CISC 121, CISC 124, CISC 235" },
            { "role": "assistant", "content": "You’re missing CISC 203 and CISC 204." }
        ]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        log_error(response)
        return

    data = response.json()
    assert "llm_response" in data, "Response missing 'llm_response' key"
    assert isinstance(data["llm_response"], str), "'llm_response' should be a string"

    logging.info("Test passed! Response:")
    print(data["llm_response"])

if __name__ == "__main__":
    test_chatbot()
