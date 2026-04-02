# Components Breakdown of MCP

Model Context Protocol

Model: AI = LLM (Large Language Model)
Context: Giving AI Context to third party
Protocol: A Set of standards

![](Pasted%20image%2020260210114418.png)

---
MCP is best understood by splitting the name itself and then mapping each part to real system components.

---
## 1. Model (LLM)
### What “Model” means in MCP
The **Model** is the Large Language Model (LLM):
- GPT    
- Claude    
- Any other foundation model    

Important constraints of the model:
- It only understands text (or structured tokens)    
- It cannot call APIs directly    
- It cannot access files, databases, or systems    
- It does not maintain long-term state on its own    

So in MCP:
- The model is **pure reasoning**    
- It decides _what_ needs to be done    
- It never decides _how_ to access systems    
This separation is intentional.

---
### Model’s responsibility in MCP
- Interpret user intent    
- Decide which tool or resource is needed    
- Construct a structured request    
- Reason over structured responses    
The model does **not**:
- Hold credentials    
- Execute commands    
- Access infrastructure  
---
## 2. Context
### What “Context” means in MCP
Context is **structured, controlled information** that the model needs in order to reason and make decisions.
This is the most important concept.
Context is not:
- Raw system access    
- Unlimited data dumps    
- Direct database connections    

Context **is**:
- Curated data    
- Tool outputs    
- Resource snapshots    
- Metadata    
- Observations from systems
---
### Types of Context in MCP
#### a) Tool Context
Data returned from a tool invocation.
Examples:
- List of available flights
- Git commit metadata    
- Kubernetes pod status    
- CI pipeline results    

#### b) Resource Context
Read-only information exposed to the model.
Examples:
- Log files    
- Configuration files    
- Documentation    
- Metrics    
- Schemas   
#### c) User Context
Information about user preferences or constraints.
Examples:
- Budget preferences    
- Region restrictions    
- Role-based permissions    
- Historical decisions    

---
### Why context must be controlled
Uncontrolled context leads to:
- Hallucinations    
- Security risks    
- Information overload    
- Inconsistent decisions    

MCP ensures:
- Context is structured    
- Context is scoped    
- Context is auditable    

---
## 3. Protocol
### What “Protocol” means in MCP
The protocol is a **standardized contract** for how context flows between systems.
It defines:
- How tools are described    
- How resources are exposed    
- How requests are made    
- How responses are returned    
- How errors are handled    

This is what makes MCP scalable and vendor-neutral.

---
### What the Protocol standardizes
#### Tool definitions
- Tool name    
- Input schema    
- Output schema    
- Description    
- Permissions    
#### Request format
- Tool invocation requests    
- Resource read requests    
- Context queries    

#### Response format
- Structured outputs    
- Typed data    
- Errors and warnings    

---
### Why a protocol is necessary
Without a protocol:
- Every integration is custom    
- Tools are tightly coupled    
- LLM behavior is unpredictable    
- Systems cannot trust AI agents    

With a protocol:
- Tools become discoverable    
- Integrations are reusable    
- Safety boundaries are enforced    
- AI agents become production-ready    

---
## 4. MCP Client
### What the MCP Client does
The MCP Client is the **runtime bridge** between the model and the outside world.
It:
- Lives alongside the LLM    
- Translates model intent into MCP requests    
- Sends requests to MCP servers    
- Returns structured responses to the model    

Examples:
- Cursor    
- Windsurf    
- Claude Code    
- Custom AI applications    

---
### Why the client is separate from the model
- Keeps the model stateless    
- Allows multiple models to reuse the same tools    
- Enables consistent enforcement of protocol rules    

---
## 5. MCP Server
### What the MCP Server does
The MCP Server is the **authority** that exposes tools and resources.
It:
- Defines what tools exist    
- Controls access    
- Connects to real systems    
- Enforces permissions    
- Sanitizes outputs    

Examples:
- Airline MCP server    
- Git MCP server    
- Kubernetes MCP server    
- Database MCP server    

---
### Ownership model
This is critical:
- MCP Servers are owned by **system owners**    
- Not by model providers    
- Not by end users    
This preserves security and accountability.

---

## 6. Tools
### Tools in MCP
Tools are **explicit actions** an AI agent is allowed to perform.
Each tool:
- Has a clear name    
- Has a strict input schema    
- Has a strict output schema    
- Performs a real-world operation    
Examples:
- `search_flights`    
- `get_commit_diff`    
- `list_pods`    
- `restart_service`
The model selects tools.  
The server executes them.

---
## 7. Resources
### Resources in MCP
Resources are **read-only contextual data**.
Examples:
- Logs    
- Config files    
- Metrics    
- Documentation    
Resources:
- Cannot change state    
- Are safe by default    
- Provide grounding for reasoning    

---
## Putting It All Together (Conceptual Flow)
```scss
User
  ↓
Model (LLM)
  ↓
MCP Client
  ↓
MCP Server
  ├─ Tools (actions)
  └─ Resources (context)
```
Key rule:  
**The model never directly touches tools or systems.**

---
## Why This Component Breakdown Matters
This separation:
- Prevents unsafe access    
- Enables auditing    
- Makes AI predictable    
- Allows enterprises to trust AI agents    

MCP is not about making AI more powerful.  
It is about making AI **responsible, scalable, and controllable**.