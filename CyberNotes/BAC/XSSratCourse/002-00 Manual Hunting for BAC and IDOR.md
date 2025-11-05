#  002-00 Manual Hunting for BAC and IDOR

Agenda
* Why Manual Hunting?
* What is manual hunting
* BAC
	* Listing functions
	* Listing Users
	* CRUD actions
	* Any other functions
	* GET calls
	* POST + PUT + DELETE calls
* IDOR
	* Listing objecsts
	* Listing users
	* RUD actions
	* Any other functions
	* GET calls
	* POST + PUT + DELETE calls

### Why Manual hunting?
Manual hunting is a **critical skill in security testing**, especially for **Broken Access Control (BAC)** vulnerabilities.
* Its easy, You can do it with just a browser and common tools.
* Its efficient,It directly focuses on endpoints and parameters.
* You can spot more details
* It does take more time
* You can individually judge parameters, identifiers easier
	* For example, 4 IDs in 1 request body
* No tools required, You can test with:
	- Browser developer tools
	- Burp Suite (optional but helpful)
- **Time-consuming**: It requires patience and thoroughness.

---
### What is Manual Hunting?
Manual hunting means **manually testing requests and endpoints to verify access control.**
### How it's done:
- **Switch users manually:** Log in as Admin and Low Privilege (Lowpriv) in separate browsers or incognito tabs.    
- **Copy requests:** Test admin URLs and try to access them as Lowpriv users.    
- **Use MITM proxies (like Burp Suite):** To intercept and modify:    
    - **Auth tokens**        
    - **Cookies**        
    - **Request bodies**        
- **Browser developer tools:** Even without Burp, you can manually test using the **Network tab in Firefox/Chrome.**
* No tools but some do help
* Manually either repeat call as other user
* Or replace auth headers in calls via MITM proxy
* Theoretically, you can do this in FIREFOX dev tools
* Manually and individually verify each request
---

BAC - listing functions + users
https://labs.hackxpert.com/Testing%20grounds/ratsite/index.php
Users: lowpriv; lowpriv and test;test (admin)
![[{ACD6C1F2-0A84-4964-9E4E-1C894BD00976}.png]]

---
## BAC Manual Testing Workflow (Example Table)
This is how you can **plan your manual tests:**

| TC  | Role    | Request            | Expect         |
| --- | ------- | ------------------ | -------------- |
| U-1 | Admin   | GET /users         | 200 OK         |
| U-2 | Lowpriv | GET /users         | 403 Forbidden  |
| U-3 | Admin   | POST /users        | 201 Created    |
| U-4 | Lowpriv | POST /users        | 403 Forbidden  |
| U-5 | Admin   | PUT /users/{id}    | 200 OK         |
| U-6 | Lowpriv | PUT /users/{id}    | 403 Forbidden  |
| U-7 | Admin   | DELETE /users/{id} | 204 No Content |
| U-8 | Lowpriv | DELETE /users/{id} | 403 Forbidden  |
### Notes:
- 📄 Prepare a **matrix for all functions and user roles.**
- 🕵️ Check all CRUD (Create, Read, Update, Delete) actions
----
### BAC - CRUD Actions
When logged in as **Lowpriv**, try the following:
* POST /contacts - lowpriv tries to create a con
* PUT /contacts/{id} - lowpriv tries to update any contact
* DELETE /contacts/{id} - lowpriv tries to delete any contact
* GET /invoices - lowpriv tries to view the invoices listing
* POST /invoices - lowpriv tries to create a new invoice
* GET /orders - lowpriv  tries to view the orders listing
* POST /orders - lowpriv tries to create a new order
* GET /user-settings?userID={otherUser} - lowpriv tries to view another user's settings
* PUT /user-settings?userID={otherUser} - lowpriv tries to update another user's settings
* GET /users - lowpriv tries to list all users 
* POST /users - lowpriv tries to create a new user 
* PUT /users/{id) - lowpriv tries to update any user 
* DELETE /users/{id) - lowpriv tries to delete any user


---
#### BAC - GET calls
* You log in to the browser as administrator 
* You log in to a different browser (Firefox vs chrome) or in private mode as low privilege 
* You copy the link from the admin window 
* You paste it into the low-privilege user 
* We can clearly see the user should not have access to this in the next screenshot in the right
### Steps:
1. ✅ Log in as **Admin** in **Chrome.**
2. ✅ Log in as **Lowpriv** in **Firefox or Incognito.**    
3. 📋 Copy a sensitive **GET request link** from the Admin session.    
4. 📥 Paste it into the Lowpriv browser and check:    
    - Should they be allowed to access this?        
    - Does the system block or return the data?
### Visual:
In real-world tests, this is **quick and powerful for catching GET-based BAC.**

---
#### BAC - POST/PUT/DELETE Calls (Manual Testing via MITM Proxy)
* Easiest way: MITM proxy 
* These HTTP methods **change data** (create, update, delete).
- BAC issues are often hidden in these methods because:
    - They are **less visible** to normal users.
    - Many developers only focus on GET restrictions but forget to lock down modification endpoints.
* Open burp 
* Open browser 
* Log in as **low privilege** user in incognito (for isolation).
* Log in as **admin** in normal browser 
* Make a request (click around) as the low privilege user 
* Capture their auth headers 
	* Extract the authentication token/session ID.
	* In Ratsite: PHPSESSIONID 
* Save it somewhere 
* Make a request (click on something high privilege user can not do) 
	* ### Find a High-Privilege Action
	- In your **admin session:**
	    - Perform an action that low privilege users shouldn’t be able to do. Example:
	        - Create a new user (POST)
	        - Update sensitive settings (PUT)
	        - Delete a record (DELETE)
	            
- Capture this request in Burp Suite.
* Send the request to repeater
	* This allows you to modify and replay the request safely.
* Replace the auth header (Swap Authentication Headers)
	* Replace the admin’s `PHPSESSID` (or other auth tokens) with the **low privilege user’s session ID.**
* ### Replay the Request
	- Click **Send** in Burp’s Repeater.
	- Observe the response:
	    - ✅ If the system properly checks access, it should return **403 Forbidden** or similar.
	    - ❌ If the system is vulnerable, the action will succeed (e.g., a lowpriv user can create, update, or delete high-privilege resources.)
## Why This Works:
- Many systems **only protect the UI** (buttons, menus) but forget to lock down **backend endpoints.**
- Manually swapping the session lets you test the **backend security directly, bypassing the UI.**
- This method uncovers serious issues like:
    - Unrestricted POST/PUT/DELETE access.        
    - Missing backend access validation.


## Quick Example Flow:

|Step|Action|Tool|
|---|---|---|
|1|Login as lowpriv in Incognito|Browser|
|2|Capture lowpriv session (PHPSESSID)|Burp Proxy|
|3|Login as admin in normal browser|Browser|
|4|Perform restricted admin action|Burp Proxy|
|5|Send request to Repeater|Burp|
|6|Swap session ID with lowpriv’s|Burp|
|7|Replay request|Burp|
|8|Analyze result|Burp|

---

## Key Takeaways:
- **Backend access control must always be enforced.**
- POST/PUT/DELETE calls are where the most dangerous BAC bugs often hide.
- MITM proxy tools like **Burp Suite** are perfect for manual BAC hunting.
- This method helps uncover **Privilege Escalation** and **IDOR** bugs as well.
---
#### IDOR - Listing Objects
* Instead of focusing on **functions** (like GET, POST), you focus on **private objects**.
* Public objects we do not care about
### Example: In RatSite

|Object|Access Type|
|---|---|
|Invoices|Private|
|Orders|Private|
|Contacts|Private|
|Users|Private|
* Do not forget: Users
- 👉 One of these **might be public** (test carefully).
---
IDOR - Listing Users
* User A (admin)
* User B (admin)
* Both **should only access their own objects.** Even if they have the same role, **cross-access is forbidden.**

---
##### IDOR - RUD Actions(Read, Update, Delete)
### Test Scenario: Can User A access B's objects?

| Action | API Endpoint          | Expected Response |
| ------ | --------------------- | ----------------- |
| READ   | GET /invoices/B_id    | 403 Forbidden     |
| UPDATE | PUT /invoices/B_id    | 403 Forbidden     |
| DELETE | DELETE /invoices/B_id | 403 Forbidden     |
| READ   | GET /orders/B_id      | 403 Forbidden     |
| UPDATE | PUT /orders/B_id      | 403 Forbidden     |
| DELETE | DELETE /orders/B_id   | 403 Forbidden     |
| READ   | GET /contacts/B_id    | 403 Forbidden     |
| UPDATE | PUT /contacts/B_id    | 403 Forbidden     |
| DELETE | DELETE /contacts/B_id | 403 Forbidden     |
**If it returns 200 OK → It’s an IDOR vulnerability!**

![[{8FD3D94E-4374-4F5C-BEDD-8FFD9DDD9085}.png]]

IDOR - GET Calls AKA READ
* Just do the same method of 
	* Logging into two browsers 
		* One user A 
		* One user B in another browser (or incognito).
	* In User B’s browser, copy a private object’s URL (example: `GET /invoices/B_id`).
	* Paste it into User A’s browser.
	* Should return 403 
	* Do this for ALL resources that should be PRIVATE. Do this for **ALL private objects.**
---
IDOR - POST + PUT + DELETE CALLS (WRITE Testing)
* Easiest way: MiTM proxy 
* Open burp 
* Open browser 
* Log in as A user in incognito 
* Log in as B in normal browser 
* Make a request (click around) as the A 
* Capture their auth headers 
	* In ratsite: PHPSESSIONID 
	* Save it somewhere 
* Make a request as B on a PRIVATE object (Update/Delete) 
* Send the request to repeater 
* For DELETE calls 
* MAKE SURE YOU INTERCEPT AND REPLACE AS YOU CAN NOT DELETE TWICE! - DELETE calls can only work once → **Intercept and replace carefully before it actually deletes.**
* Replace the auth header
## Summary:

|Step|Description|
|---|---|
|Identify Objects|Focus on private objects.|
|Test READ Access|Copy URLs between users.|
|Test WRITE Access|Use Burp, swap sessions.|
|Expected Result|403 Forbidden if secured.|