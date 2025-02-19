In Git, the `git diff` command is used to show the differences between various states of your files. The options you provided modify how `git diff` behaves. Let's break each one down with examples.

---
## 1. `git diff filename`
### **What It Does:**
- Compares the working directory version of the file with the index (staged version).
- Shows changes that **haven't been staged yet**.
### **Example:**
#### Step 1: Create a Git repository and a file
```
mkdir git-diff-demo
cd git-diff-demo
git init
echo "Hello World" > file.txt
git add file.txt
git commit -m "Initial commit"
```
#### Step 2: Modify the file **without staging**
`echo "New Line" >> file.txt`
#### Step 3: Run `git diff`
`git diff file.txt`
#### **Output (Example):**
```
diff --git a/file.txt b/file.txt
index e69de29..d95f3ad 100644
--- a/file.txt
+++ b/file.txt
@@ -1 +1,2 @@
 Hello World
+New Line
```
This shows that a new line `"New Line"` has been added but **not yet staged**.

---
## 2. `git diff -r HEAD filename`
### **What It Does:**
- Compares the working directory version of the file **with the latest commit (HEAD)**.
- Shows **all unstaged and staged changes**.
### **Example:**
#### Step 1: Stage the changes
`git add file.txt`
#### Step 2: Run `git diff -r HEAD file.txt`
`git diff -r HEAD file.txt`
#### **Output (Example):**
```
diff --git a/file.txt b/file.txt
index e69de29..d95f3ad 100644
--- a/file.txt
+++ b/file.txt
@@ -1 +1,2 @@
 Hello World
+New Line
```
Even though the file is staged, the changes are still visible because `-r HEAD` compares **working directory** vs **HEAD**.

---
## 3. `git diff -r HEAD`
### **What It Does:**
- Compares the entire **working directory** (all files) with the latest commit (`HEAD`).
- Shows unstaged and staged changes across all files.
### **Example:**
#### Step 1: Modify another file
`echo "Another Change" > another.txt 
`git add another.txt`
#### Step 2: Run `git diff -r HEAD`
`git diff -r HEAD`
#### **Output (Example):**
```
diff --git a/file.txt b/file.txt
index e69de29..d95f3ad 100644
--- a/file.txt
+++ b/file.txt
@@ -1 +1,2 @@
 Hello World
+New Line

diff --git a/another.txt b/another.txt
new file mode 100644
index 0000000..d95f3ad
--- /dev/null
+++ b/another.txt
@@ -0,0 +1 @@
+Another Change
```
This shows **changes across all files** compared to `HEAD`.

---
## **Summary Table:**

|Command|Compares|Shows|
|---|---|---|
|`git diff filename`|Working Directory vs. Index|Unstaged changes in `filename`|
|`git diff -r HEAD filename`|Working Directory vs. Last Commit (HEAD)|Unstaged + Staged changes in `filename`|
|`git diff -r HEAD`|Working Directory vs. Last Commit (HEAD)|Unstaged + Staged changes in all files|

🚀