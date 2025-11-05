# 🔑 Authentication on API Level
---
## 📌 **How API Authentication Works**
- Users **arrange authentication beforehand.**
- They log in (often via a web portal) to get an **API Key** or credentials.

---
## 🚪 Authentication Methods
### 1. **API Keys (Most Common)**
- 📥 Provided after login or registration.
- 🔑 Sent in request headers:   
    `Authorization: Api-Key YOUR_API_KEY`
- ✅ Easy to use.    
- ✅ Most widely used.    
- ❌ If leaked, easy to abuse.
---
### 2. **JWT (JSON Web Tokens)**
- 📦 Complex structure: `Header.Payload.Signature`
- 🔗 Sent in headers or cookies:    
    `Authorization: Bearer YOUR_JWT_TOKEN`
- ✅ Used when sessions or OAuth2 are involved.
- ❌ Less common in basic APIs due to complexity.
    

---

### 3. **Basic Authentication**
- 🔐 Base64 encode: `username:password`
- Example:    
    `Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=`
- ✅ Very simple.
- ❌ Not secure without HTTPS.

---
## 🔥 Summary Table

|Method|Usage|Security|Example Header|
|---|---|---|---|
|API Key|Most common|Moderate|`Authorization: Api-Key abc123`|
|JWT|Less common|Secure (with key)|`Authorization: Bearer eyJhbGciOi...`|
|Basic Auth|Rare (nowadays)|Weak without HTTPS|`Authorization: Basic dXNlcm5hbWU6cGFz`|

---
