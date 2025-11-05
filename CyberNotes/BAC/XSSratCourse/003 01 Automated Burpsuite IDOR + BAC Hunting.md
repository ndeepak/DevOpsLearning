
# 003 01 Automated Burpsuite IDOR + BAC Hunting
## Agenda
1. Repeating the steps of manual hunting
2. Automating the steps above without tools in our head
3. Burp suite options
	1. Match and replace
	2. Authorize
	3. Auth matrix
4. Match and replace steps + example
5. Authorize steps + example
6. Auth matrix + example
7. This does not work on property level!

---

Repeating the manual steps
1. BAC
	1. Get auth header of low priv user
		1. Example, Cookie: PHPSESSID=il5u3kktv0hng3sd01ik8fsgig;
		2. Auth tokens could be:        
        - JWT            
        - PHPSESSIONID            
        - Basic Auth headers
	2. Log in as high priv user (Admin)
	3. Go make request low priv user can not do
		1. Example:
		- Delete user    
		- Change roles    
		- View sensitive dashboard
	4. **Capture This Request in Burp**
		- Right-click → Send to Repeater
	5. Replace the auth headers with Low Privilege User's Auth Header
		* Change the session ID or JWT token to the low privilege one.
	6. **Send the Modified Request and Check the Result**
	- It **should return 403 Forbidden.**
	- If it succeeds → **VULNERABLE! (BAC)**

2. IDOR
IDOR is about testing **same privilege users accessing each other's private objects.**
	1. Get auth header of same priv level user A (NOT 2 ADMINS WHO CAN SEE EVERYTHING!) (i.e. Normal User)
		1. Must be a user who has access to **their own objects only.**
	2. Log in as high priv user B (Same Privilege Level)
	3. Go make request low priv user can not do.. Perform Action on User B's Private Object
		1. GET /invoices/12345
	4. Replace the auth headers **with User A's Auth Header**
		1. You are now asking → "Can User A access User B's invoice?"
	5. **Send the Modified Request and Check the Result**
	- It **should return 403 Forbidden.**
	- If it succeeds → **VULNERABLE! (IDOR)**

---

## For BAC Setup
1. ALWAYS open burp in background
	1. Either built in browser
	2. Or point browser to burp + cert import for SSL!
2. Log in as low priv user (lowpriv/lowpriv) on [https://labs.hackxpert.com/Testing%20grounds/ratsite/index.php](https://labs.hackxpert.com/Testing%20grounds/ratsite/index.php)
3. Grab their auth header
	1. .JWT
	2. Session ID
	3. Basic auth...
4. And extract all the information you need ONLY! (Cookie: PHPSESSID=il5u3kktv0hng3sd01ik8fsgig;)
	1. Otherwise you run risk of pollution of test

Repeating the manual steps
-BAC Attacks
1. Log in in private window as admin (test/test)
2. Perform privileged action as admin
3. Replace auth header with the low priv users
4. Should return 403

-IDOR attacks
1. Similar logic, just replace with 2 users on same level who have PRIVATE objects


---

Automation the above steps in pseudo actions
1. Replace Auth Header in Each Request
- **For BAC:**
    - Replace auth header with **lower privilege user’s session**.
- **For IDOR:**
    - Replace auth header with **same privilege user’s session** (but for private objects owned by another user).	
With lower priv user for functions or same priv user for private objects

2. Check the response
	1. If responses = Same (status code + body)
		1. BAC!
	2. If Response = similar (status code 200 but different body I.E.)
		1. Is BAC? You be the judge!

### Check the Response
#### 🚩 BAC Detection:
- **If response (status code + body) is exactly the same as the original (admin’s response) → BAC confirmed!**
#### 🚩 Possible BAC:
- **If status code is 200 but body differs → Possible BAC → Manual review needed.**
#### 🚫 Not Vulnerable:
- **If response is 403 Forbidden or another denial → Proper access control enforced.**

---
## Pseudo Workflow Example
```plaintext
FOR each captured request:
    REPLACE auth header:
        IF testing BAC:
            Use lower privilege user's auth
        IF testing IDOR:
            Use same privilege user's auth (from another user)

    SEND modified request

    IF response status code == original AND response body == original:
        REPORT: "BAC VULNERABILITY DETECTED: Full Access"
    
    ELSE IF response status code == 200 AND response body differs:
        REPORT: "Possible BAC - Review manually"
    
    ELSE IF response status code == 403 or similar:
        REPORT: "Proper access control - No Issue"
    
    ELSE:
        REPORT: "Unexpected Response - Review required"
```

---
## 🚀 Quick Checklist for Automation

|Step|Purpose|Example Tool|
|---|---|---|
|Capture Requests|Intercept actions|Burp Proxy|
|Swap Auth Header|Simulate privilege escalation|Burp Repeater/Autorize|
|Send Modified Request|Trigger the action|Burp Repeater/Extension|
|Compare Status Code + Body|Confirm or deny vulnerability|Autorize / Custom Script|
|Log & Report|Track possible BAC/IDOR issues|Burp Logger|

---

## 📦 Tools You Can Use
- **Burp Suite + Autorize Extension** (for automated header swapping and response comparison)
- **Burp Suite Macros** (for session management and auto-login)    
- **Custom Python Scripts** (if you want to automate outside Burp using `requests` module)
---

### Burpsuite Options
1. Match and replace
	1. Clunky but not real setup required
	2. Works out of the box
	3. Can scan a FULL request only but an entire app like that fast
	4. You need to interpret everything!
	
2. Authorize
	1. More powerful
	2. Harder to use
	3. Faster to test with once setup
	4. Need to be able to interpret results still
	
3. Auth matrix
	1. MASSIVE setup
	2. Test entire app with 1 click after setup
	3. Repeatable
	4. Maintenance heavy

---

### Match and Replace Steps + Example