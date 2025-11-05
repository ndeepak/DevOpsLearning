# Injection

### **Injection Techniques Checklist:**

### 1. **SQL Injection (SQLi)**:

- [ ]  **Classic SQLi**:
    - Test for unexpected SQL query behavior using characters like **`'`** or **`"`**.
    - Inject SQL payloads like **`' OR '1'='1`** to manipulate query results.
- [ ]  **Blind SQLi**:
    - Inject payloads that trigger conditional responses, e.g., using **`AND`** or **`OR`** conditions.
    - Monitor application responses to deduce database information.
- [ ]  **Time-based Blind SQLi**:
    - Inject payloads that cause delays, e.g., using **`WAITFOR DELAY`** or **`SLEEP`**.
    - Measure response times to infer database truths.
- [ ]  **Out-of-band SQLi**:
    - Inject payloads that trigger DNS lookups or HTTP requests.
    - Monitor external servers for incoming requests to confirm vulnerability.

### 2. **Operating System (OS) Command Injection**:

- [ ]  **Direct Command Injection**:
    - Inject OS commands using characters like **`;`**, **`&&`**, or **`||`**.
    - Test for unexpected system behavior or responses.
- [ ]  **Blind OS Command Injection**:
    - Inject commands that cause observable side effects, e.g., creating files.
    - Monitor system state or use out-of-band channels to confirm execution.

### 3. **LDAP Injection**:

- [ ]  **Manipulating LDAP Queries**:
    - Inject LDAP filters or characters like **`(`**, **`)`**, **`&`**, or **`|`**.
    - Test for altered LDAP query results or unexpected behaviors.
- [ ]  **Bypassing LDAP Authentication**:
    - Inject filters like **`)(uid=*)`** to manipulate authentication checks.
    - Test for unauthorized access or bypass of login mechanisms.

### 4. **XML Injection**:

- [ ]  **XML External Entity (XXE) Attack**:
    - Inject external entity references, e.g., **`<!DOCTYPE … SYSTEM "URL">`**.
    - Test for retrieval of internal files or interactions with external systems.
- [ ]  **XML Attribute Injection**:
    - Inject malicious attributes or values into XML data.
    - Monitor application behavior for signs of XML parsing vulnerabilities.

### 5. **Code Injection**:

- [ ]  **Direct Code Execution**:
    - Inject code snippets in languages like PHP, JavaScript, or Python.
    - Test for execution of injected code within the application context.
- [ ]  **Blind Code Injection**:
    - Inject code that causes side effects or out-of-band interactions.
    - Monitor system behavior or external servers for signs of code execution.

### 6. **Expression Language (EL) Injection**:

- [ ]  **Manipulating EL Expressions**:
    - Inject EL payloads, e.g., **`${8*8}`** in Java-based applications.
    - Test for evaluation of injected expressions and altered application responses.

### 7. **Server-Side Template Injection (SSTI)**:

- [ ]  **Template Engine Manipulation**:
    - Inject template expressions or syntax specific to engines like Jinja2, Twig, or Freemarker.
    - Monitor application responses for signs of template evaluation.

### 8. **Server-Side Request Forgery (SSRF)**:

- [ ]  **Forcing Server Interactions**:
    - Inject URLs or payloads that cause the server to make unintended network requests.
    - Monitor internal systems or external servers for incoming requests.

### 9. **Testing Tools and Utilities**:

- [ ]  Utilize tools like SQLMap, Burp Suite, and custom payloads.
- [ ]  Monitor logs, network traffic, and system behavior for signs of successful injections.

### 10. **Mitigation Verification**:

- [ ]  Confirm that input validation and sanitization are in place.
- [ ]  Ensure that parameterized queries, safe APIs, or ORM are used for database interactions.
- [ ]  Verify that least privilege principles are applied to database and OS operations.
