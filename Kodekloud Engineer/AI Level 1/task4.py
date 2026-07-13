import os
from openai import OpenAI

# Initialize OpenAI client using environment variables
client = OpenAI(
    api_key=os.environ.get
    ("Sk-kkAI-53fee547e860722d34d1cfe8bbba77dc12e45006fd2b2b025a8013967c0f387ekk_sf6ujyexieqdk3jj-kkb0f332ba"),
    base_url=os.environ.get("https://kodekey.ai.kodekloud.com/v1")
)

def compare(item1: str, item2: str) -> str:
    # Construct the prompt
    prompt = (
        f"Compare {item1} and {item2} only based on the chipset used. "
        f"Respond with one word only."
    )

    # Send request to AI model
    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5
    )

    # Extract and return response text
    result = response.choices[0].message.content.strip()
    return result


# Perform comparison
response = compare("iphone 13", "iphone 17")

# Print one-word output
print(response)