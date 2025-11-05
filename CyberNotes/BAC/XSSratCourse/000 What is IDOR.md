## 📚 IDOR (Insecure Direct Object Reference) Explained
### ✅ What is IDOR?
- **IDOR** stands for **Insecure Direct Object Reference**.
- It happens when **an application exposes direct access to objects** like files, records, invoices, or user profiles **without proper authorization checks**.
- Example: Accessing `https://site.com/invoice?id=1` to see Invoice #1. If you change the ID to `id=2` and can access Invoice #2 (which doesn’t belong to you), that’s an IDOR.

---
## 🔑 Key Concepts
### 📌 Direct Object Reference:
- **Direct access** to objects via something like `id=1` in:
    - URLs (GET requests)        
    - POST request bodies        
    - Headers (including cookies)        
    - File uploads/imports        

### 📌 Insecure Part:
- The system **fails to properly check** whether you are allowed to access that object.    

---
## 🔒 Authentication vs Authorization

|Concept|Meaning|
|---|---|
|Authentication|Verifying _who_ you are (login, biometrics)|
|Authorization|Verifying _what_ you are allowed to access|
- **IDOR is always a failure of _authorization_, not authentication.**    
---

## 🚨 Common IDOR Attack Scenarios
1. **Unauthenticated IDOR:**    
    - Accessing objects without logging in.        
    - Example: `GET /invoices?id=432` without any session.        
2. **Authenticated IDOR:**    
    - Logged in as a user but accessing objects you shouldn’t.        
    - Example: Logged in as User A, but accessing User B’s invoice.        
3. **Multi-Tenant IDOR (B2B Applications):**    
    - **IDOR between employees** of the same company.        
    - **IDOR between two different companies.**        
    - Example: An employee from Company A accessing sensitive data of Company B.
---
## 📥 Where Can IDs Be Hidden?
- URL parameters (GET): `?id=432`    
- POST body parameters    
- Cookies (Session IDs, object IDs)    
- HTTP Headers (Custom headers might carry IDs)    
- File imports (hidden ID fields in CSV/JSON/XML files)    

### 🔍 Pro Tip:
> **Always test IDOR in:**  
> ✅ GET requests  
> ✅ POST requests  
> ✅ Headers (especially cookies)  
> ✅ File upload/import parameters

---

## ⚙️ Object ID vs User ID Reference
- **Object ID Example:** `/invoice?id=10`    
- **User ID Example:** `/invoice?owner=123`    
- Both can be vulnerable to IDOR.    
- Know whether you’re **directly referencing an object or indirectly via the user**.    

---

## 🥈 Primary vs Secondary IDOR
- **Primary IDOR:** Happens immediately during object request.    
- **Secondary IDOR (Second-Order):**    
    - Happens when one system passes a request to another without re-checking authorization.   
    - Example: If System A authorizes you but passes your request to System B, which doesn’t validate your permissions.
        

---

## 🏢 Multi-Tenancy and IDOR
- **Multi-Tenant Applications:** Multiple companies or clients share the same system/server.    
- Risk: A user from Company A may access Company B’s sensitive data if proper separation is not enforced.    
- Very dangerous in B2B applications (HR, invoicing, etc.).    

---

## ✅ Summary Checklist for Finding IDOR
✔️ Check object references in GET, POST, headers, cookies, and file uploads.  
✔️ Test both unauthenticated and authenticated scenarios.  
✔️ Investigate multi-tenant risks.  
✔️ Understand both user-based and object-based ID references.  
✔️ Look for primary and secondary (second-order) IDOR vulnerabilities.

---

