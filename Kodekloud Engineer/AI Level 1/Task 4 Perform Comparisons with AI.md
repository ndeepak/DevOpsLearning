# Task 4 Perform Comparisons with AI
The devops AI Development Team is now exploring how artificial intelligence can assist in making smarter, data-driven decisions for cloud optimization. Continuing this journey, you are tasked to build a Python-based AI module that compares `chipset` used between two major iPhone models.

Inside `compare.py`, create an `OpenAI` client using the provided `api_key` and `base_url` under `/root/.bash_profile`. Then, define a function named `compare(item1: str, item2: str) -> str` that constructs a parameterized prompt asking the AI to compare the two given iPhone models (item1 and item2) **in terms of only the chip used**, ensuring the response is given **in one word only**.

Use the following items for comparison:

`iphone 13`  
`iphone 17`

After defining the function, send the constructed `prompt` to the OpenAI chat model using:

- model: `openai/gpt-4.1-mini`
- messages: user → `prompt`
- max_tokens: `100`
- temperature: `0.5`

Store the result in a variable named `response`, and print the **one-word comparison output** to the console.

Finally, run your `compare.py` file to perform the chip comparison.

  

**Notes:**

1. Function should accept two parameters: `item1` and `item2`.
    
2. Use the provided `OpenAI api_key` and `base_url` under `/root/.bash_profile`.
    
3. File `compare.py` must be inside `/root/openaiproject`.
    
4. Use hardcoded values for `api_key` and `base_url` when initializing the `OpenAI client` or read them from environment variables via `os.environ.get('OPENAI_API_KEY')` and `os.environ.get('OPENAI_BASE_URL')`.
    
5. Before running the script run the following commands:
    

```bash
python3 -m venv venv && source venv/bin/activate && pip install openai
```

6. You are allowed a maximum of `10` requests. After this, you may encounter a `rate limiter error`, so use your calls wisely.

----
## Solution:

```python
from openai import OpenAI

# Initialize OpenAI client using environment variables
client = OpenAI(
    OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY"),
    OPENAI_API_BASE=os.environ.get("OPENAI_BASE_URL")
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
```

```bash
cd /root/openaiproject
python3 -m venv venv && source venv/bin/activate && pip install openai
python3 compare.py
```

References:

https://developers.openai.com/api/reference/python


