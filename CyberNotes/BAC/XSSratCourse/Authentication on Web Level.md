# 🌐 Authentication on Web Level
## 🗂️ Sessions (Old Method)
- ✅ **Used in early web applications**
- ❌ **Rarely used now** due to security flaws
- ⚠️ **Common issues:**
    - **Session Fixation:** Attacker forces a user to use a known session ID.
    - **Session Hijacking:** Stealing a session ID to impersonate a user.
    - Sessions can be easily mismanaged or forced.

---
## 🔐 JWT Tokens (Modern Method)
- ✅ **Commonly used today**
- 🔗 Stored in **HTTP headers** or **cookies** (cookies are also part of headers)
- 🛠️ Typically obtained via **OAuth 2.0 authentication** or similar flows
- 📦 JWT Structure:
    `Header.Payload.Signature`
- 📜 JWTs can **always be decoded** to read the payload (never store sensitive data without encryption!)
- 🔐 Requires a **secret key to encode** and verify the token.
- 🌍 Test and view at [https://jwt.io](https://jwt.io)

---

### 💡 Key Differences:

|Feature|Sessions|JWT Tokens|
|---|---|---|
|Storage|Server-side|Client-side (Header/Cookie)|
|Scalability|Low|High|
|Common Attack|Session Fixation|Token Leakage|
|Usage|Old|Modern|