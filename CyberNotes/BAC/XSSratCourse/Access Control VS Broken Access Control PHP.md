# 📚 Access Control vs Broken Access Control (PHP Examples)
## ✅ What is Access Control?
- Access Control is **controlling what resources, objects, or functions a user can access.**
- It must be applied:    
    - ✅ On every endpoint (every URL, API call, page).        
    - ✅ On every object (files, invoices, user profiles).        
    - ✅ On every function that modifies or displays data.        

> **Challenge:** Applications may have **thousands of endpoints and objects.**  
> It's easy for developers to miss one and leave it exposed.

---
## ❌ What is Broken Access Control?
- Broken Access Control occurs when:
    - Proper security checks are **missing or not correctly implemented.**
    - Unauthorized users can **view, modify, or delete resources they shouldn’t have access to.**

---
# ⚔️ Access Control vs Broken Access Control in PHP
## ✅ Correct Example (Secure Access Control)
```php
<?php
session_start();
require 'db.php'; // Database connection

if (!isset($_SESSION['user_id'])) {
    die('You must be logged in.');
}

$invoice_id = $_GET['invoice_id'];
$user_id = $_SESSION['user_id'];

// Fetch invoice from database
$stmt = $conn->prepare("SELECT * FROM invoices WHERE id = ? AND owner_id = ?");
$stmt->bind_param("ii", $invoice_id, $user_id);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    die('Unauthorized access.');
}

$invoice = $result->fetch_assoc();
echo "Invoice: " . $invoice['details'];
?>
```

### ✅ Secure Points:
- Checks if the user is logged in.    
- Confirms the **invoice belongs to the logged-in user.**    
- Protects against unauthorized access.    

---
## ❌ Incorrect Example (Broken Access Control)
```php
<?php
session_start();
require 'db.php'; // Database connection

if (!isset($_SESSION['user_id'])) {
    die('You must be logged in.');
}

$invoice_id = $_GET['invoice_id'];

// 🚨 No ownership check!
$stmt = $conn->prepare("SELECT * FROM invoices WHERE id = ?");
$stmt->bind_param("i", $invoice_id);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    die('Invoice not found.');
}

$invoice = $result->fetch_assoc();
echo "Invoice: " . $invoice['details'];
?>
```

### 🚨 Vulnerability:
- Any logged-in user can **access invoices of other users by changing the `invoice_id` in the URL.**    
- This is a classic **IDOR (Insecure Direct Object Reference)** and broken access control issue.
---
## 🔐 Example: Role-Based Access Control in PHP
### ✅ Secure Admin Action
```php
<?php
session_start();

if (!isset($_SESSION['user_id']) || $_SESSION['role'] !== 'admin') {
    die('Access denied. Admins only.');
}

$user_to_delete = $_GET['user_id'];
require 'db.php';

// Delete user
$stmt = $conn->prepare("DELETE FROM users WHERE id = ?");
$stmt->bind_param("i", $user_to_delete);
$stmt->execute();

echo "User deleted successfully.";
?>
```

### ✅ Secure Points:
- Checks if the **user is an admin** before deleting.
- Prevents normal users from accessing admin actions.

---
### ❌ Broken Admin Control (Example)
```php
<?php
session_start();

// 🚨 No role check!
if (!isset($_SESSION['user_id'])) {
    die('You must be logged in.');
}

$user_to_delete = $_GET['user_id'];
require 'db.php';

$stmt = $conn->prepare("DELETE FROM users WHERE id = ?");
$stmt->bind_param("i", $user_to_delete);
$stmt->execute();

echo "User deleted successfully.";
?>
```

### 🚨 Vulnerability:
- Any logged-in user can **delete other users** without being an admin.---

## 🛠️ Developer’s Checklist to Avoid Broken Access Control
- ✅ Validate **session status** (is the user logged in?).    
- ✅ Validate **ownership of objects** (does this invoice belong to the user?).    
- ✅ Check **roles and permissions** (is this user an admin?).    
- ✅ Never trust user input (don’t rely on client-side controls).    
- ✅ Apply **access control on every endpoint and object.**    
- ✅ Regularly review code for forgotten access checks.    

---
## ⚡ Summary Table

|Feature|Secure Control|Broken Control|
|---|---|---|
|Authentication|Session required|May skip session checks|
|Ownership validation|Object must belong to user|No ownership check|
|Role validation|Check roles (admin, user)|Role not checked|
|URL ID access|Verified against user|Accessible by changing ID|
|Common vulnerability|Access denied if not authorized|Data leakage, IDOR possible|

---