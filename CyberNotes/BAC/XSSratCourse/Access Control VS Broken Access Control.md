# 📚 Access Control vs Broken Access Control
## ✅ What is Access Control?
- **Access Control** is the mechanism that **ensures users can only access resources, data, or functions they are authorized to use.**    
- It is critical for enforcing security boundaries in applications.    

### ✔️ Developer's Responsibility:
- Apply **correct access control**:    
    - ✅ On **every endpoint** (API URLs, web pages, page, etc.)        
    - ✅ On **every object** (data entries, files, user profiles, etc.)        
    - ✅ On **every function** that can manipulate or read objects i.e. displays data.
        
- This is difficult because:    
    - Applications can have **thousands of endpoints and objects.**        
    - It’s easy to **miss one or apply access control incorrectly.**        

---
## ❌ What is Broken Access Control?
- **Broken Access Control** happens when:    
    - Access control is **not properly enforced**.        
    - Users can **perform actions or access data they shouldn’t.**        

### 🔍 Common Reasons:
- Missing checks.    
- Incorrect role validation.    
- Relying on client-side enforcement.    
- Hardcoded access patterns that are easy to bypass.    

---
## 🔐 Types of Access Control Models

|Model|Description|
|---|---|
|Role-Based Access Control (RBAC)|Access based on user roles (Admin, User, Guest).|
|Attribute-Based Access Control (ABAC)|Access based on user attributes (department, location, etc.).|
|Discretionary Access Control (DAC)|User controls access to their own objects.|

---
## ⚔️ Access Control vs Broken Access Control Example
### ✅ Secure Access Control Example:
```python
# Flask-based API example with proper access control
@app.route('/invoices/<int:invoice_id>')
@login_required
def view_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if invoice.owner_id != current_user.id:
        return "Unauthorized", 403
    return render_template('invoice.html', invoice=invoice)
```
- ✅ Checks if the logged-in user **owns the invoice**.
- ✅ Denies access with HTTP 403 if not authorized.
    

---

### ❌ Broken Access Control Example:
```python
# Flask-based API example with broken access control
@app.route('/invoices/<int:invoice_id>')
@login_required
def view_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    return render_template('invoice.html', invoice=invoice)
```

- 🚨 No ownership check!    
- A logged-in user can access **any invoice just by changing the URL ID**.    

---
## 🔓 Another Example: API Endpoint
### ✅ Secure API (Role-Based)
```python
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    delete_user_from_db(user_id)
    return jsonify({'message': 'User deleted successfully'})
```
### ❌ Broken API
```python
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    delete_user_from_db(user_id)
    return jsonify({'message': 'User deleted successfully'})
```

- 🚨 Any logged-in user can delete other users without restriction.
---
## ⚙️ Real-World Scenarios

|Scenario|Secure|Broken|
|---|---|---|
|User accessing their profile|Checks if profile belongs to user|No check; users can view/edit other profiles|
|Admin deleting a user|Role check: Only admins allowed|No role check; any user can delete others|
|Company employee accessing another company’s data|Multi-tenant ID check per request|No isolation between tenants|

---
## 🛠️ Developer’s Best Practices
- ✅ **Enforce access control on the server side.**
- ✅ **Check user identity and permissions for each resource.**    
- ✅ Validate **both the request and the object being accessed.**    
- ✅ Apply **principle of least privilege.**    
- ✅ Use well-tested access control libraries/frameworks.    
- ✅ Regularly **review and test** all endpoints and functions.    
- ✅ Never trust user input (don’t rely on client-side validation).
---

## ⚡ Summary

|Topic|Key Point|
|---|---|
|Access Control|Proper permission enforcement|
|Broken Access Control|Missing or incorrect permission check|
|Developer’s Role|Must secure every endpoint & object|
|Why It's Hard|Many endpoints, easy to miss|
|How to Secure|Check roles, ownership, server-side|

---

[[Access Control VS Broken Access Control PHP]]