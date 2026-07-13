# Task 1 Clarify Bugs with AI


Question:
The `datacenter` AI Engineering team is developing tools to improve the clarity of developer-reported bugs. Developers often report issues informally, which makes them difficult to understand or reproduce.

You are tasked to build a Python-based **AI Bug Description Clarifier** that transforms such informal bug reports into clear, structured, and professional issue summaries.

Inside `/root/openaiproject/bug_clarifier.py`:
1. Initialize the `OpenAI` client using environment values (`api_key` and `base_url`).    
2. Define a function `clarify_bug(description: str) -> str` that builds a **parameterized prompt** to rewrite the raw bug description.    
3. Send this prompt to the **OpenAI Chat Completion API**.    
4. Use the following configuration for the API call:    
    - **model**: `openai/gpt-4.1-mini`
    - **messages**: user → the constructed prompt
    - **max_tokens**: `100`
    - **temperature**: `0.0`
5. Use the input bug report:
```text
  App keeps crashing when I click save.
```
6. Store the AI response in a variable named `response` and print the clarified bug summary to the console.

  

**Notes:**
1. Function must use the developer's input description dynamically in the prompt.    
2. Ensure you are working inside `/root/openaiproject`.    
3. OpenAI credentials are available in `/root/.bash_profile`.    
4. Use hardcoded values for `api_key` and `base_url` when initializing the `OpenAI client` or read them from environment variables via `os.environ.get('API_KEY')` and `os.environ.get('BASE_URL')`.    
5. Before running `bug_clarifier.py`, set up a virtual environment:   

```bash
python3 -m venv venv && source venv/bin/activate && pip install openai
```

5. Maximum of **10 API requests** allowed before rate limiting.

---


# Solution: 

1. Go to the project directory and set up the virtual environment:

```
cd /root/openaiproject && python3 -m venv venv && source venv/bin/activate && pip install openai
```

2. Create `bug_clarifier.py` with the following content:

```python
import os
from openai import OpenAI

# Initialize OpenAI client using environment variables
client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url=os.environ.get("BASE_URL")
)

def clarify_bug(description: str) -> str:
    prompt = f"""
Rewrite the following informal bug report into a clear, professional, and structured bug summary.

Bug Report:
{description}

Provide a concise and professional issue description.
"""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=100,
        temperature=0.0
    )

    return response.choices[0].message.content.strip()


# Input bug report
bug_description = "App keeps crashing when I click save."

# Store AI response in variable named response
response = clarify_bug(bug_description)

# Print clarified bug summary
print(response)
```

3. Make sure the environment variables are loaded:

```
source /root/.bash_profile
```

4. Run the script:

```
python bug_clarifier.py
```

Example output:

```
The application crashes consistently when the user clicks the Save button. This issue prevents data from being saved and disrupts normal application functionality.
```


References:
https://developers.openai.com/api/reference/python

