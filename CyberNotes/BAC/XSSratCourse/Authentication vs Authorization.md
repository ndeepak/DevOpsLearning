## 🔐 Authentication vs Authorization
- **Authentication:**  
    👉 Proves **who you are** (login with username & password).
- **Authorization:**  
    👉 Decides **what you can do or access** (permissions).
    

---
### 🗝️ Quick Process:
1. You **log in** → (Authentication)
2. You get a **token** → (Like your ID card)
3. Token is used to **authorize** your actions (no need to log in every time)
4. When testing **BAC (Broken Access Control)**, you reuse this token to check if you can access what you shouldn't.
---
> 💡 **Remember:**  
> Authentication = Identity ✅  
> Authorization = Permissions 🔓

---