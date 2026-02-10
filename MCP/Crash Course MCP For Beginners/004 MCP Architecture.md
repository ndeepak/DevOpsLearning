# MCP Architecture

## 1. MCP Specifications: Client ↔ Server
At its core, MCP defines a **clear contract** between two entities:
- **MCP Client**: runs next to the LLM    
- **MCP Server**: exposes tools, resources, and prompts    

The specification answers four fundamental questions:
1. What can the server expose?    
2. How does the client discover those capabilities?    
3. How does the client invoke them?    
4. How is data exchanged safely and predictably?   
MCP is intentionally **client–server**, not peer-to-peer.

---

## 2. Types of Entities MCP Can Expose
An MCP Server can expose **three types of entities**. This distinction is extremely important.
### 2.1 Resources (Resources Context)
**Resources are read-only context.**
They:
- Do not change system state    
- Provide grounding data for reasoning    
- Are safe by default    
Examples:
- Log files    
- Configuration files    
- Git repository snapshots    
- Kubernetes manifests    
- Metrics    
- Documentation    
Think of resources as:
> “Here is the world as it currently looks.”

The LLM can:
- Read    
- Analyze    
- Correlate    
But cannot mutate anything through resources.

### 2.2 Tools (Tools Context)
**Tools are actions.**
They:
- Can change state    
- Perform real operations    
- Are strictly controlled    
Examples:
- Book a flight    
- Restart a service    
- Create a Kubernetes pod    
- Trigger a CI pipeline    
- Open a pull request    

Each tool has:
- A name    
- An input schema    
- An output schema    
- A description    
- Explicit permission boundaries    
Critical rule:  
The **model selects** the tool,  
the **server executes** the tool.

### 2.3 Prompts (Prompts Context)
**Prompts are reusable instruction templates.**
They:
- Standardize common reasoning patterns    
- Reduce hallucinations    
- Encode best practices    
Examples:
- “Analyze a production incident”    
- “Compare two Git commits”    
- “Summarize a Kubernetes failure”    

Prompts are not tools and not resources.  
They are **guidance artifacts** exposed by the server.

Think of prompts as:
> “Approved ways to think about this system.”

---
## 3. SDKs Available
MCP provides SDKs so you don’t implement the protocol from scratch.
Common SDKs:
- Python SDK    
- TypeScript / JavaScript SDK    

SDKs handle:
- JSON-RPC formatting    
- Transport handling   
- Tool registration    
- Schema validation    
- Error handling    
This allows you to focus on:
- Business logic    
- Tool implementation    
- Security boundaries

---

## 4. How MCP Clients and Servers Communicate
### The Protocol Used: JSON-RPC
MCP uses **JSON-RPC** as its communication protocol.
This choice is intentional.
## 5. What Is JSON-RPC?
JSON-RPC is:
- A lightweight    
- Language-agnostic    
- Request–response protocol    
- Encoded in JSON    
[JSON-RPC](https://www.google.com/search?q=JSON-RPC&sourceid=chrome&ie=UTF-8&mstk=AUtExfBbPJXSxz9vHEOIEFWPUfH0INhydQZ5c0qYxJ_lYAqfbTvmKOPi91vj_d6JtpOf5UIsR81vb3NqM7zz0YxpJmS3Hf488zEF21KbUWFHh49CwWMZJqavp1yhf3U2RAwXD1DjJrMuvP8EHooWDABX3KC1fiepDPzq1tj9hyHJCcBRqR8&csui=3&ved=2ahUKEwipyovlxM6SAxXBSmwGHVNbF-EQgK4QegQIARAB) is a lightweight, stateless Remote Procedure Call (RPC) protocol that uses [JSON](https://www.json.org/) for data serialization. It enables simple, language-independent communication between a client and server, allowing for method invocation, parameter passing, and notification support. It is widely used for API communication, supporting batch requests to reduce network overhead.

A JSON-RPC message contains:
- A method name    
- Parameters    
- An ID    
- A structured response    

Example (conceptual):
```json
{
  "jsonrpc": "2.0",
  "method": "tools.invoke",
  "params": {
    "name": "search_flights",
    "arguments": {
      "from": "NYC",
      "to": "London"
    }
  },
  "id": 1
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "flights": [...]
  },
  "id": 1
}
```


Why JSON-RPC works well for MCP:
- Explicit method calls    
- Strong structure    
- Easy to validate    
- Easy to audit    
- Transport-independent

---
## 6. How Data Is Sent and Received
Data flow always follows this pattern:
1. MCP Client sends a JSON-RPC request    
2. MCP Server validates the request    
3. MCP Server executes tool or fetches resource    
4. MCP Server returns structured JSON    
5. MCP Client passes structured context to the model    

Important:
- No free-form text between client and server    
- Everything is typed and structured   
This is how hallucinations are reduced.

---
## 7. Transport Used for JSON-RPC
JSON-RPC is **transport-agnostic**.
MCP supports multiple transports:

### Common Transports
- STDIO    
- HTTP / HTTPS    
- TCP    
- Unix Domain Sockets    
- Message queues (conceptually supported)
### Why Multiple Transports Matter
Because MCP is used in different environments:
- Local development    
- IDE integrations    
- Desktop apps    
- Remote enterprise services
- Air-gapped systems  

---
## 8. Using an MCP Server
### Relationship Between MCP Server and API Server
An MCP Server is **not a replacement for APIs**.
Instead:
- MCP Server sits **in front of APIs**    
- MCP Server wraps APIs into tools    
- MCP Server enforces policy and context boundaries    
Think of it like this:
```scss
LLM
 ↓
MCP Client
 ↓
MCP Server
 ↓
API Server
```

The API server remains unchanged.  
MCP adds an AI-safe access layer.
### Calling an MCP Server
From the client’s perspective:
- It calls the MCP server
- It never calls backend APIs directly
The MCP server:
- Translates tool calls into API calls    
- Sanitizes inputs and outputs    

---

## 9. Where Is the MCP Server Hosted?
### Option 1: Local MCP Server
Common for:
- IDE usage
- Development    
- Personal workflows    
Examples:
- File system MCP server    
- Git MCP server    
- Local database MCP server    
### Local Configuration
In tools like Cursor or Claude Code:
- MCP servers are defined in a JSON config    
- The server is started locally    
- Communication often uses STDIO    

Example concepts:
- Client spawns the MCP server process    
- STDIO is used for JSON-RPC messages
### HTTP Local Example
`MCP Client → http://localhost:3000/mcp`
Used when:
- MCP server runs as a service    
- Multiple clients connect    
- Debugging is needed    
---
## 10. MCP Server Hosted Remotely
Common for:
- SaaS platforms    
- Enterprise services    
- Shared tools    
Example:
`MCP Client → https://joyair.com/mcp`

### Remote Hosting Considerations
This is where MCP becomes enterprise-grade.
Key concerns:
- Authentication    
- Authorization    
- Data privacy    
- Trust boundaries    
- Rate limiting    
- Auditing    
The protocol allows this, but **policy enforcement is the server’s responsibility**.

---
## 11. Connecting to Applications Using SDKs
When building your own application:
- You embed an MCP Client using the SDK    
- You configure one or more MCP Servers    
- The client handles all communication    

In Python:
- SDK manages JSON-RPC    
- You focus on orchestration logic    
This is how MCP-powered agents are built into real applications.

---

## Key Architecture Takeaway
MCP Architecture enforces **clean separation**:
- Model reasons    
- Client communicates    
- Server controls    
- Systems execute   
This separation is what allows AI agents to move from demos to production systems.

