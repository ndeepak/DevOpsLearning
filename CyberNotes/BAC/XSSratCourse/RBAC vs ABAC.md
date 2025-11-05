# 📚 RBAC vs ABAC (with PHP Examples)
## 🔐 **RBAC: Role-Based Access Control**
### ✅ Key Concepts:
- **Every user is assigned a role.**
- **Roles have predefined permissions** (rights) tied to:
    - Specific objects (files, records)        
    - Specific functions (delete, edit)        
    - Specific properties of an object (view name, hide salary)
### ✅ Example Roles:
- `admin` → can create, read, update, delete (CRUD)    
- `editor` → can create, read, update    
- `viewer` → can only read

---
### ✅ RBAC Flow:
`User → Role → Rights → Object/Action`

---

### ✅ PHP Example of RBAC
```php
<?php
session_start();

$user_role = $_SESSION['role']; // Example: 'admin', 'editor', 'viewer'

// RBAC Permission Table
$permissions = [
    'admin' => ['delete', 'edit', 'view'],
    'editor' => ['edit', 'view'],
    'viewer' => ['view']
];

$requested_action = $_GET['action']; // Example: 'delete'

if (in_array($requested_action, $permissions[$user_role])) {
    echo "Action allowed: $requested_action";
    // Perform the action...
} else {
    echo "Access Denied: You are not authorized to perform this action.";
}
?>
```

### ✅ Secure Points:
- **Role assignment controls what users can do.**
- Simple and easy to manage in small/medium systems.

---
## 🚫 Limitation of RBAC
- RBAC is **static**.
- It does not consider **dynamic factors** like:
    - Device type        
    - IP address        
    - Time of access        
    - User location        

---
# 🧩 **ABAC: Attribute-Based Access Control**
### ✅ Key Concepts:
- Access is **granted based on user attributes.**    
- Attributes can include:    
    - ✅ User properties (role, department, subscription level)        
    - ✅ Environment properties (IP address, location, browser)        
    - ✅ Object properties (sensitivity level, owner)        

### ✅ Example Attributes:
- Allow access **only if user is on a corporate network.**    
- Allow streaming **only if user is in permitted countries (Netflix).**
- Allow admin actions **only during working hours.**

---
### ✅ ABAC Flow:
`User + Attributes + Environment → Policy → Access Decision`

---

### ✅ PHP Example of ABAC
```php
<?php
session_start();

$user_role = $_SESSION['role'];
$user_ip = $_SERVER['REMOTE_ADDR'];
$allowed_ip_range = '192.168.1.'; // Example internal network

$action = $_GET['action'];

// ABAC policy example
if ($user_role == 'admin' && strpos($user_ip, $allowed_ip_range) === 0 && date('H') >= 9 && date('H') <= 17) {
    echo "Action allowed: $action (within allowed IP and working hours)";
    // Perform the action...
} else {
    echo "Access Denied: Outside allowed attributes.";
}
?>
```
### ✅ Secure Points:
- Checks **multiple dynamic factors.**
- Highly flexible and fine-grained control.

---
## 🚫 Limitation of ABAC
- ABAC is **complex to manage and implement.**
- Can be hard to audit.    
- Policies can conflict if not carefully designed.
---
# 🔥 RBAC vs ABAC Comparison

|Feature|RBAC|ABAC|
|---|---|---|
|Based On|User Roles|Attributes (user, object, environment)|
|Flexibility|Low (static roles)|High (dynamic policies)|
|Example|Admin can delete all users|Admin can delete only during office hours and from office network|
|Complexity|Simple|Complex|
|Scalability|Less scalable for large systems|Highly scalable|
|Management|Easy role assignment|Requires policy management|

---

# ✅ Summary:
- **RBAC** is best for **static, role-driven systems** like intranet portals, small web apps, basic CRUD apps.
- **ABAC** is best for **dynamic, complex, scalable systems** like cloud services, streaming platforms (Netflix), or multi-tenant apps with location/device-based security.
---