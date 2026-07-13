# Task 2 Create an AI Chatbot
The AI development team at `Nautilus` is tasked with building a role-play chatbot using OpenAI's API.

**Task Requirements:**
1. Navigate to the `/root/openaiproject/chatbot.py` directory.    
2. Create a `client` instance using `api_key` and `base_url`.    
3. Use openai model=`openai/gpt-4.1-mini`    
4. Define a variable `prompt` with the following content:   

```
You are a friendly travel guide. Greet the user and ask where they want to go.
```

5. Send this prompt to the OpenAI chat model and store the result in variable name`response`.    
6. Extract and print the generated text reply from the `response`    
7. Run the file after installing OpenAI in a virtual environment.    

  

**Notes:**
1. Ensure you are working inside `/root/openaiproject`.    
2. `api_key`&`base_url` are in `/root/.bash_profile` (typically `OPENAI_API_KEY` and `OPENAI_API_BASE_URL`).    
3. Install OpenAI inside a venv before running the script.    

```bash
python3 -m venv venv && source venv/bin/activate && pip install openai
```

4. Use `temperature=0.7`&`max_tokens=100`.    
5. Use hardcoded values for `api_key`&`base_url` when initializing the OpenAI client, or read them from environment variables via `os.environ.get('API_KEY')` and `os.environ.get('BASE_URL').`
6. You are allowed a maximum of `10` requests. After this, you may encounter a `rate limiter error`. Therefore, use your requests judiciously.

----
## Solution


```python
import os
from openai import OpenAI
  

# Create OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
) 

# Prompt for the chatbot
prompt = "You are a friendly travel guide. Greet the user and ask where they want to go."
 

# Send request to OpenAI chat model
response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.7,
    max_tokens=100
)
  

# Extract and print generated reply
reply = response.choices[0].message.content


print(reply)
```