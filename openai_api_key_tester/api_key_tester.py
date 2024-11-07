import sys
import os
from typing import Tuple, List, Dict
from openai import OpenAI, APIError, APIConnectionError
from datetime import datetime, timezone
import base64
import requests
import json

# Available models to test
OPENAI_MODELS = [
    "gpt-4",
    "gpt-4-turbo-preview",
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-1106",
    "dall-e-3",
    "text-embedding-ada-002"
]

# Example Ollama models to test
OLLAMA_MODELS = [
    "llama2",
    "mistral",
    "codellama",
    "phi"
]

def validate_key_format(api_key: str) -> bool:
    """
    Perform basic validation of API key format.
    OpenAI keys typically start with 'sk-' and have a specific length.
    """
    if not api_key.startswith('sk-'):
        return False
    if len(api_key) < 40:  # OpenAI keys are typically longer than 40 chars
        return False
    return True

def validate_ollama_url(url: str) -> bool:
    """
    Validate Ollama API URL format.
    """
    if not url:
        return False
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    return True

def test_ollama_model(base_url: str, model: str) -> Tuple[bool, str]:
    """
    Test a specific Ollama model.
    Returns a tuple of (success: bool, message: str)
    """
    try:
        print(f"Testing Ollama model: {model}...")
        # First check if model exists
        response = requests.get(f"{base_url}/api/tags")
        if response.status_code != 200:
            return False, f"❌ Failed to get model list: HTTP {response.status_code}"
            
        available_models = response.json().get("models", [])
        if not any(m.get("name") == model for m in available_models):
            return False, f"❌ Model {model} is not available in Ollama"

        # Test the model with a simple generation request
        headers = {'Content-Type': 'application/json'}
        data = {
            'model': model,
            'prompt': 'Hello',
            'stream': False
        }
        response = requests.post(f"{base_url}/api/generate", headers=headers, json=data)
        
        if response.status_code == 200:
            return True, f"✅ Model {model} is accessible"
        else:
            return False, f"❌ Error testing {model}: HTTP {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return False, f"❌ Connection error with {model}: {str(e)}"
    except Exception as e:
        return False, f"❌ Unexpected error with {model}: {str(e)}"

def get_ollama_status(base_url: str) -> Dict:
    """
    Get Ollama API status.
    Returns a dictionary containing status information.
    """
    try:
        print("📊 Checking Ollama API status...")
        
        # Get current timestamp
        now = datetime.now(timezone.utc)
        
        # Test API connection
        response = requests.get(f"{base_url}/api/tags")
        if response.status_code == 200:
            status = "✅ API is responsive"
            available_models = len(response.json().get("models", []))
        else:
            status = f"❌ API error: HTTP {response.status_code}"
            available_models = 0

        return {
            "status": "success",
            "data": {
                "checked_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "api_status": status,
                "available_models": available_models
            }
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"Connection error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

def get_usage_stats(client: OpenAI) -> Dict:
    """
    Retrieve usage statistics for the API key.
    Returns a dictionary containing usage information.
    """
    try:
        print("📊 Retrieving usage statistics...")
        
        # Get current timestamp in ISO format
        now = datetime.now(timezone.utc)
        start_date = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        end_date = now
        
        # Test a simple API call to check quota
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            quota_status = "✅ API quota available"
        except APIError as e:
            if "exceeded your current quota" in str(e):
                quota_status = "❌ API quota exceeded"
            else:
                quota_status = f"⚠️ API status unknown: {str(e)}"

        return {
            "status": "success",
            "data": {
                "checked_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "quota_status": quota_status,
                "api_status": "✅ API is responsive" if quota_status != "❌ API quota exceeded" else "❌ API quota exceeded"
            }
        }
    except APIError as e:
        return {
            "status": "error",
            "error": f"API Error while checking status: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unexpected error while checking status: {str(e)}"
        }

def test_model(client: OpenAI, model: str) -> Tuple[bool, str]:
    """
    Test a specific OpenAI model with the API key.
    Returns a tuple of (success: bool, message: str)
    """
    try:
        print(f"Testing model: {model}...")
        
        if model == "dall-e-3":
            # Test DALL-E 3 model
            response = client.images.generate(
                model=model,
                prompt="A simple test image of a blue dot",
                n=1,
                size="1024x1024"
            )
            return True, f"✅ Model {model} is accessible"
            
        elif model == "text-embedding-ada-002":
            # Test embedding model
            response = client.embeddings.create(
                model=model,
                input="test"
            )
            return True, f"✅ Model {model} is accessible"
            
        elif model == "gpt-4-vision-preview":
            # Test vision model with a simple base64 image
            # Create a 1x1 transparent pixel
            base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=1
            )
            return True, f"✅ Model {model} is accessible"
            
        else:
            # Test chat completion models
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return True, f"✅ Model {model} is accessible"
            
    except APIError as e:
        if "model not found" in str(e).lower():
            return False, f"❌ Model {model} is not available with this API key"
        return False, f"❌ Error testing {model}: {str(e)}"
    except Exception as e:
        return False, f"❌ Unexpected error with {model}: {str(e)}"

def format_usage_stats(stats: Dict) -> str:
    """
    Format usage statistics into a readable string.
    """
    if stats["status"] == "success":
        data = stats["data"]
        return "\n".join([
            "📊 API Status Check:",
            f"- Checked at: {data['checked_at']}",
            f"- API Status: {data['api_status']}",
            f"- Quota Status: {data.get('quota_status', 'N/A')}",
            f"- Available Models: {data.get('available_models', 'N/A')}"
        ])
    else:
        return f"❌ Failed to retrieve API status:\n{stats['error']}"

def main():
    """
    Main function to handle the API key testing process.
    """
    print("\n=== API Key Tester ===\n")
    
    # Test OpenAI API
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("Testing OpenAI API...")
        if not validate_key_format(api_key):
            print("❌ Error: Invalid API key format. OpenAI API keys should start with 'sk-'")
        else:
            try:
                client = OpenAI(api_key=api_key)
                print("✅ OpenAI API client initialized successfully\n")
                
                # Get and display usage statistics
                usage_stats = get_usage_stats(client)
                print("\n" + format_usage_stats(usage_stats) + "\n")
                
                # If quota is exceeded, skip model testing
                if usage_stats["status"] == "success" and "❌ API quota exceeded" in usage_stats["data"]["quota_status"]:
                    print("\n❌ Skipping OpenAI model testing due to exceeded quota.")
                else:
                    # Test models
                    print("\nTesting OpenAI model access:")
                    for model in OPENAI_MODELS:
                        success, message = test_model(client, model)
                        print(message)
                    
            except APIError as e:
                print(f"\n❌ OpenAI API Error: {str(e)}")
            except APIConnectionError:
                print("\n❌ Connection error. Please check your internet connection.")
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
    else:
        print("ℹ️ OpenAI API key not provided, skipping OpenAI tests.")

    # Test Ollama API
    ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    if validate_ollama_url(ollama_url):
        print("\nTesting Ollama API...")
        try:
            # Get and display Ollama status
            ollama_stats = get_ollama_status(ollama_url)
            print("\n" + format_usage_stats(ollama_stats) + "\n")
            
            if ollama_stats["status"] == "success":
                # Test models
                print("\nTesting Ollama model access:")
                for model in OLLAMA_MODELS:
                    success, message = test_ollama_model(ollama_url, model)
                    print(message)
        except Exception as e:
            print(f"\n❌ Ollama API Error: {str(e)}")
    else:
        print("\nℹ️ Invalid or missing Ollama API URL, skipping Ollama tests.")

    print("\n✅ Test completed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ An unexpected error occurred: {str(e)}")
        sys.exit(1)
