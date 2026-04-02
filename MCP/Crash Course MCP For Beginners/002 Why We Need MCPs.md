# Why We Need MCPs

## The Core Problem We Are Solving
LLMs (like GPT) are **stateless text prediction engines**.
They:
- Do not know how to call APIs    
- Do not know how to access databases    
- Do not know how to run scripts    
- Do not know how to make real-world decisions safely    

Yet modern AI systems are expected to:
- Book flights    
- Debug production systems    
- Inspect Kubernetes clusters    
- Analyze codebases    
- Trigger workflows    
So the real question becomes:
**How does an LLM safely interact with real systems, tools, and data without hardcoding logic or breaking security boundaries?**
This is where MCP exists.

---

## From Simple LLM to Agent-Based Systems
### Traditional LLM Interaction
`User → LLM → Text Response`
Example:
> "I want to fly to North London"

LLM replies with text suggestions only.
No execution.  
No decisions.  
No real action.

---

## Enter AI Agents
AI Agents extend LLMs by allowing them to:
- Break goals into steps    
- Call tools    
- Make decisions    
- Maintain context
- Act autonomously within limits    
Your flight example is a **goal-driven agent system**.
### Goal
Book a flight to North London.
### Constraints
- Cheap vs luxury    
- Seat preferences    
- Meal preferences    
### Actions
- Query airlines    
- Compare options    
- Make a decision    
- Execute booking
---
## How This Was Traditionally Built (Before MCP)
Let’s analyze your examples.
### 1. Automation Scripts / Python Pipelines
- Hand-written orchestration    
- Tight coupling between code and APIs    
- Hardcoded credentials    
- No standard interface for LLMs    
Problems:
- Not reusable    
- Fragile    
- Hard to scale    
- Security risks

---
What are these? how does this does this?

![](Pasted%20image%2020260210111251.png)
Automation scripts workflow
![](Pasted%20image%2020260210111323.png)
 Microsoft System Orchestrator


![](Pasted%20image%2020260210111351.png)
Modern Tool like Zapier



![](Pasted%20image%2020260210111233.png)
Series of Python scripts

![](Pasted%20image%2020260210111451.png)


---

### 2. Enterprise Orchestrators (Microsoft System Orchestrator)
- Rule-based workflows    
- Heavy configuration    
- Not LLM-native    
- Not context-aware    

Problems:
- Static logic    
- Poor natural language integration    
- High operational overhead    

---
### 3. Modern No-Code Tools (Zapier, etc.)
- Trigger-based automation    
- Predefined connectors    
- Limited reasoning    

Problems:
- No deep decision-making    
- Cannot reason over complex context    
- LLM is bolted on, not first-class

---
Sample Python :

```py
# Step 1: Read input from user
user_input = input("where do you want to fly? \n")

# Step 2: Extract flight details using LLM
prompt=
("role": "system", "content": "Extract origin, destination, and
date. "},
("role": "user", "content": user_input}
flight_query = call_Um(prompt)

# Step 3: Fetch flight options from airlines (mocked inline)
flight_options = fetch_flight_details)

# Step 4: Fetch user preferences from memory (mocked)
user_prefs = fetch_user_preferences)

# Step 5: Ask LLM to pick the best flight
decision_prompt = [
("role":
"systen",
"content": f"User preferences: {user_prefs)"},
("role": "user", "content": f"Available flights: (flight_options)"}
decision = call_lLm(decision_ prompt)

# Step 6: Book the selected flight (mocked)
def book_flight(flight): return f"Flight {flight['flight']} on
{flight['airline']} booked!"
print(book_flight({"flight": "AG303", "airline": "AeroGo"}))

# Assume LLM chsose AeroGo
```
`All code is pseudo code only. Donot try as is. Use the available in the labs.`


### 4. Series of Python Scripts (Your Example)
Your pseudo-code illustrates the **real problem perfectly**.
Let’s break it down.
#### What your code is actually doing
1. Accepts user intent    
2. Uses LLM to extract structured data    
3. Calls airline APIs    
4. Retrieves user preferences    
5. Asks LLM to decide    
6. Executes an action    

This works, but:
- Every integration is custom    
- LLM has no standardized way to request tools    
- Context passing is manual    
- Security is implicit, not enforced    
- Scaling this to 50 tools becomes chaos    

This approach does not scale.


---

## The Missing Layer: Standardized Context + Tool Access
What is missing is a **protocol** that defines:
- How an LLM requests data    
- How tools expose capabilities    
- How permissions are enforced    
- How responses are structured    
- How decisions are auditable    

That missing layer is **MCP**.
What are Tools, in using AI agents interacting with third party airlines and all.

## What MCP Actually Solves
MCP is **not**:
- A framework    
- A workflow engine    
- A replacement for APIs    
MCP **is a protocol** that standardizes how context and tools are exchanged between AI models and systems.

## MCP in the Flight Booking Example
### Without MCP
`LLM → Custom Python → Airline APIs`

Problems:
- Tight coupling    
- No standard permissions    
- LLM can accidentally access more than intended    
- No clear boundary
### With MCP
```scss
User
  ↓
LLM
  ↓
MCP Client
  ↓
MCP Server (Joyair, DracAir, AeroGo)
  ↓
Airline APIs
```

Key changes:
- LLM never touches APIs directly
- MCP Server exposes only approved tools
- Each airline is an MCP Server
- Tools are discoverable and typed    
- Context is structured


---
Use Cases: troubleshooting
"We recently noticed that a button was missing on the UI. Help me identify when and how this changed and share a plan to revert."

Agent track the Git change, check backend code, check frontend code, and then find and points out the Commit #124234 caused this change. To fix ...

---

## What Are “Tools” in AI Agents?
In MCP terminology:
### Tools are:
- Callable actions    
- Defined inputs and outputs    
- Explicit permissions    

Examples:
- `search_flights(origin, destination, date)`    
- `get_user_preferences(user_id)`    
- `book_flight(flight_id)`    

The LLM does not know **how** these work.  
It only knows:
- What tools exist    
- What inputs they accept    
- What outputs they return    

This is critical for safety and reliability.

---
## Why Client–Server Architecture Matters
### MCP Client
- Embedded in tools like Cursor, Windsurf, Claude Code    
- Acts as the LLM’s gateway    
- Sends structured requests    

### MCP Server
- Owned by system teams    
- Exposes tools and resources    
- Enforces access control    
- Connects to real systems (DBs, APIs, clusters)    
This separation ensures:
- No direct system access by the LLM    
- Clear ownership    
- Auditable actions    

---
## Troubleshooting Use Case (Very Important)
Your UI button example is a **classic MCP use case**.
### User Request
> “A button is missing on the UI. Identify when and how this changed and provide a plan to revert.”

### What the Agent Needs to Do
1. Inspect Git history    
2. Check frontend commits    
3. Check backend changes    
4. Correlate timestamps    
5. Identify breaking commit    
6. Suggest rollback or fix    

### Without MCP
- LLM hallucinating commit IDs    
- Manual copy-paste of logs    
- Risky repo access    
- No permission boundaries
### With MCP
MCP Servers expose:
- Git repository access (read-only)    
- CI/CD logs    
- Frontend build artifacts    
- Backend service configs    

Agent flow:
```scss
LLM
 → MCP tool: list_recent_commits
 → MCP tool: diff_commit
 → MCP tool: inspect_frontend_change
 → MCP tool: correlate_backend_dependency
```
 
Result:
- Commit #124234 identified    
- Exact file and change highlighted    
- Safe remediation plan suggested    

No hallucination.  
No unsafe access.  
No manual digging.

---

## Frontend Use Cases
![](Pasted%20image%2020260210112610.png)
- Trace UI regressions    
- Compare builds    
- Inspect feature flags    
- Analyze A/B test changes    

MCP Server exposes:
- Build artifacts    
- Feature flag configs    
- UI snapshots    

---
## Data Engineering Use Cases
![](Pasted%20image%2020260210112342.png)
- Inspect pipeline failures    
- Validate schema changes    
- Trace data lineage    
- Compare dataset versions    

MCP Server exposes:
- Metadata catalogs    
- Pipeline logs    
- Data quality metrics   

---

## Why MCP Is Necessary (Summarized)
Without MCP:
- AI agents are unsafe    
- Integrations are brittle    
- Scaling tools is impossible    
- Security is unclear    
- Auditing is hard    

With MCP:
- Standard tool interface    
- Safe, permissioned access    
- Reusable integrations    
- Clear system boundaries    
- Enterprise-ready AI agents    

---
## Who Builds MCP Servers?
This is critical.
MCP Servers are built by:
- Platform teams    
- DevOps teams    
- Tool vendors    
- Cloud providers    
- Internal engineering teams    
Examples:
- A company builds an MCP server for Kubernetes    
- A vendor builds one for their SaaS API    
- A team builds one for internal databases    
LLMs do **not** own MCP servers.  
**System owners do.**

---
## Key Mental Model
MCP does for AI what:
- REST did for web services    
- Kubernetes API did for infrastructure    
- OpenAPI did for integrations    
It turns AI agents from demos into **production systems**.

---


