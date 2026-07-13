# MCP Prerequisities

## What is MCP and why is matters?
Developed by Anthropic, Claude, but designed for LLM Open Standard

Like USB for AI,
Universal Protocol to connect LLM to external systems

![](MCP/MCP%20For%20Beginners/Attachments/Pasted%20image%2020260428203613.png)

The Problem MCP Solves
1. Limited knowledge and cutoff dates
2. No access to real time data
3. No access to personal or private documents
4. No ability to interact with external systems


How MCP works
1. Key components
	1. MCP Client/Host
	2. MCP Protocol
	3. MCP Server
	4. External Services
2. The Flow
	1. Language Model
	2. Client Application
	3. External Services
---
1. Key components
Think for these like the restaurants
	1. MCP Client/Host 
	2. MCP Protocol
	3. MCP Server
	4. External Services
![](MCP/MCP%20For%20Beginners/Attachments/Pasted%20image%2020260428203936.png)

Application are:
(User, AI Chatbot, AI Assistant)
| |
MCP Client are: Messenger who Initiates Requests and Receive Response
they talk to MCP server
| |
MCP Server:  Program like accessing files, calendar, database , it is secure gateway
| |
External Data/tool: actual resource or server like, dB, file system, third party web tool, digital tool


MCP Primitives
![](MCP/MCP%20For%20Beginners/Attachments/Pasted%20image%2020260428204321.png)MCP Server:
1. Resources (Data):
	1. Content of file
	2. Information retrieve from web service
	3. Calendar Events, etc.
2. Tools (Actions):
	1. Sending an email
	2. Creating a task
	3. adding an event
	4. social media post
3. Prompts (Templates):
	1. Formatting a request


---
2. The Flow
Restaurant analogy:
Restaurant itself is host, the client is an agent which orders food, the waiter is the client which carries information and the chef is the mcp server who cook food.
	1. Language Model
	2. Client Application
	3. External Services

MCP in action: real world examples
1. File system access
2. Github integration
3. web search
4. database access


Host with an MCP Client
like
1. MCP server 01 --> LLM
2. MCP server 02 --> Database
3. MCP server 03 --> API

---
MCP - Benefits
1. Standardization
2. Separation of concerns
3. Extensibility
4. Reduced Hallucinations
5. Enhanced Capabilities



---

## What Problem does MCP solve?
The core challenge
1. Information silos
2. Integration complexity
3. Limited context
4. Development overhead
5. Scalability Barriers

MCP the universal connector
1. Standardized data exchange
2. Two-way communication
3. Secure local-first architecture
4. Developer simplicity

![](MCP/MCP%20For%20Beginners/Attachments/Pasted%20image%2020260428205557.png)
Traditional approach


![](MCP/MCP%20For%20Beginners/Attachments/Pasted%20image%2020260428205712.png)
MCP Approach


Developer Experience

| With MCP                            | Without MCP                                       |
| ----------------------------------- | ------------------------------------------------- |
| Create standardized mcp servers     | write separate code for each api integration      |
| one protocol handles authentication | custom authentication for each service            |
| unified context managment           | manage context sharing per integration            |
| consistent error handling           | implement error handling for each api and service |


Enterprise applications

| With MCP                                   | Without MCP                                  |
| ------------------------------------------ | -------------------------------------------- |
| Standard protocol for all internal tools   | Build proprietary connectors to data sources |
| Seamless access to knowledge repositiories | Limited access to internal knowledge bases   |
| Unified security model                     | Complex security integration strategies      |
| Reduced maintenance when updating systems  | High maintenance when tools change           |


MCP in action
1. Claude Desktop: using MCP to access local files and tools
2. Microsoft copilot studio: auto-discovering actions from mcp servers
3. Enterprise Assistants: connecting to internal knowledge bases
4. Data Analysis: secure connections to databases and visualization tools
5. Development environments: IDE integration with Git, databases, and documentations

Conclusion:
1. From isolated models to connected systems
2. From custom integrations to standardized protocol
3. From limited context to rich, relevant information
4. From development complexity to simplified architecture

