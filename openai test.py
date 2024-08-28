import time
import openai

openai.api_key = "sk-...VgwA"

def call_openai_with_retry(prompt, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=50
            )
            return response.choices[0].text.strip()
        except openai.error.RateLimitError:
            print(f"Rate limit exceeded. Attempt {attempt + 1} of {retries}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

result = call_openai_with_retry("Hello, how are you?")
if result:
    print("API Response:", result)
