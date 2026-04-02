**Major use cases** with examples:
## **1. Compare Unstaged Changes (Working Directory vs Index)**
### **Use Case:** See what changes are made but not yet staged.
`git diff`
🔹 **Example Output:**
```
diff --git a/file.txt b/file.txt
index e69de29..d95f3ad 100644
--- a/file.txt
+++ b/file.txt
@@ -1 +1,2 @@
 Hello World
+New Line
```
🔹 **Use Case:** Useful before `git add` to verify what will be staged.

---
## **2. Compare Staged Changes (Index vs HEAD)**
### **Use Case:** See what changes are staged but not yet committed.
`git diff --cached`
🔹 **Example Output:**
```
diff --git a/file.txt b/file.txt
index e69de29..d95f3ad 100644
--- a/file.txt
+++ b/file.txt
@@ -1 +1,2 @@
 Hello World
+New Line
```
🔹 **Use Case:** Ensures that only intended changes are staged before committing.

---
## **3. Compare Working Directory with Last Commit (HEAD)**
### **Use Case:** See all modifications (both staged and unstaged).
`git diff HEAD`
🔹 **Example Output:**
```
diff --git a/file.txt b/file.txt
index e69de29..d95f3ad 100644
--- a/file.txt
+++ b/file.txt
@@ -1 +1,3 @@
 Hello World
+New Line
+Another Line
```
🔹 **Use Case:** Helps review all changes before committing.

---
## **4. Compare Two Commits**
### **Use Case:** Find differences between two commits.
`git diff commit1 commit2`
🔹 **Example:**
`git diff a1b2c3d 4e5f6g7`
🔹 **Use Case:** Track how a file/project has evolved between two points in history.

---
## **5. Compare Changes Between Two Branches**
### **Use Case:** See what’s different between two branches.
`git diff main feature-branch`
🔹 **Use Case:** Helps review a feature before merging into `main`.

---
## **6. Compare a Specific File Between Two Branches**
### **Use Case:** See how a single file differs between branches.
`git diff main feature-branch -- path/to/file.txt`
🔹 **Use Case:** Useful when debugging or reviewing a specific file.

---
## **7. Show Changes in a Specific Commit**
### **Use Case:** See what changes were introduced in a particular commit.
`git diff commit-hash^ commit-hash`
🔹 **Example:**
`git diff 4e5f6g7^ 4e5f6g7`
🔹 **Use Case:** Helps understand what was changed in a specific commit.

---
## **8. Compare Changes in a Stash**
### **Use Case:** View changes in a specific stash.
`git stash show -p stash@{0}`
🔹 **Use Case:** Helps decide whether to apply or drop a stash.

---
## **9. Compare Two Tags**
### **Use Case:** See what changed between two versions (tags).
`git diff v1.0 v2.0`
🔹 **Use Case:** Useful in software releases.

---
## **10. Generate a Patch from Differences**
### **Use Case:** Create a patch file to share with others.
`git diff > changes.patch`
🔹 **Use Case:** Patches can be applied using `git apply changes.patch`.

---
## **11. Ignore Whitespace Differences**
### **Use Case:** Compare code while ignoring whitespace changes.
`git diff -w`
🔹 **Use Case:** Helps focus on actual code changes.

---
## **12. Show Word-Level Differences**
### **Use Case:** Highlight only changed words instead of full lines.
`git diff --word-diff`
🔹 **Example Output:**
`Hello [-old-] {+new+} World`

🔹 **Use Case:** Useful for reviewing small text changes.

---
## **Summary Table of `git diff` Use Cases**

| Command                             | Use Case                             |
| ----------------------------------- | ------------------------------------ |
| `git diff`                          | Show unstaged changes                |
| `git diff --cached`                 | Show staged changes                  |
| `git diff HEAD`                     | Show all changes (staged + unstaged) |
| `git diff commit1 commit2`          | Compare two commits                  |
| `git diff branch1 branch2`          | Compare two branches                 |
| `git diff main feature -- file.txt` | Compare a file in different branches |
| `git diff commit^ commit`           | Show changes in a commit             |
| `git stash show -p`                 | View stash differences               |
| `git diff v1.0 v2.0`                | Compare two tags                     |
| `git diff > changes.patch`          | Create a patch file                  |
| `git diff -w`                       | Ignore whitespace changes            |
| `git diff --word-diff`              | Show word-level differences          |
🚀