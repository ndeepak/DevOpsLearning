## **Detailed Guide on `git stash` with Advanced Use Cases**
### **1. What is `git stash`?**
`git stash` is used to temporarily save uncommitted changes in a Git working directory so you can switch branches or pull updates without committing incomplete work.
It helps in scenarios where:
- You need to quickly switch branches but don’t want to commit partial work.
- You want to apply changes later or move them between branches.
- You need a clean working directory for testing or updates.

---
### **2. Basic Usage of `git stash`**
The simplest way to stash changes:
`git stash`
This:
- Saves **unstaged and staged changes** (tracked files only).
- Reverts the working directory to the last commit.
- Allows you to switch branches without committing.

**Example:**
```
# Modify files
echo "Temporary changes" >> file.txt

# Check status
git status

# Stash changes
git stash

# Verify working directory is clean
git status  # No changes
```

---
### **3. Viewing and Applying Stashes**
#### **3.1. Listing Stashes**
To see the list of stashed changes:
`git stash list`
Example output:
```
stash@{0}: WIP on main: 4d8f2d1 Updated README
stash@{1}: WIP on feature-branch: 9c1a3b2 Added new feature
```
- `stash@{0}` → Most recent stash
- `stash@{1}` → Older stash

---

#### **3.2. Applying a Stash**
To restore the last stash without removing it from the stash list:
`git stash apply`
To apply a specific stash:
`git stash apply stash@{1}`
If conflicts occur, resolve them manually.

---
#### **3.3. Applying and Removing a Stash (`git stash pop`)**
To **apply** and **delete** the latest stash in one step:
`git stash pop`
- This applies the latest stash and removes it from the stash list.
- If there are conflicts, they must be resolved before proceeding.

---
### **4. Stashing Different Types of Changes**
#### **4.1. Stashing Untracked Files**
By default, `git stash` ignores untracked files. To stash them:
`git stash -u`
or
`git stash --include-untracked`
To stash **both untracked and ignored files**:
`git stash -a`

---
#### **4.2. Stashing Specific Files**
You can stash only certain files instead of all changes.
`git stash push -m "Stashing only file.txt" -- file.txt`
Example:
`git stash push -m "Temporary fix" -- src/main.py`

---
### **5. Removing Stashes**
#### **5.1. Dropping a Specific Stash**
`git stash drop stash@{1}`
This deletes `stash@{1}` from the stash list.
#### **5.2. Clearing All Stashes**
`git stash clear`
⚠️ **Warning:** This deletes all saved stashes permanently.

---
### **6. Advanced Use Cases of `git stash`**
#### **6.1. Switching Branches Without Losing Work**
If you need to switch branches but have uncommitted changes:
```
git stash
git checkout new-branch
git stash pop
```

---
#### **6.2. Creating Named Stashes**
Instead of the default message, add a custom stash description:
`git stash push -m "Bugfix in authentication module"`
Then list named stashes:
`git stash list`
Example output:
`stash@{0}: On main: Bugfix in authentication module 
`stash@{1}: On feature-branch: Refactored API calls`

---
#### **6.3. Moving Stashes Between Branches**
You can stash changes in one branch and apply them in another.
```
git stash
git checkout new-branch
git stash pop
```
This is useful when rebasing or switching features.

---
#### **6.4. Checking Stash Contents**
Before applying a stash, preview the changes:
`git stash show -p stash@{0}`
or
`git stash show -p stash@{1}`
For a more detailed view:
`git diff stash@{0}`

---
#### **6.5. Creating a Patch from a Stash**
To create a patch file from a stash:
`git stash show -p stash@{0} > stash_patch.diff`
This allows sharing or applying stashes later.

---
#### **6.6. Applying Stash Partially**
You can apply only a portion of a stash using interactive mode:
`git stash pop --index`
This applies only **staged changes** from the stash.

---
### **7. Summary Table of `git stash` Commands**

| Command                       | Description                                  |
| ----------------------------- | -------------------------------------------- |
| `git stash`                   | Stash tracked changes                        |
| `git stash -u`                | Stash tracked + untracked files              |
| `git stash -a`                | Stash tracked, untracked + ignored files     |
| `git stash list`              | View list of all stashes                     |
| `git stash apply`             | Apply latest stash but keep it in stash list |
| `git stash pop`               | Apply latest stash and remove it from list   |
| `git stash drop stash@{n}`    | Remove a specific stash                      |
| `git stash clear`             | Delete all stashes permanently               |
| `git stash push -m "message"` | Create a named stash                         |
| `git stash show -p stash@{n}` | View stash details                           |
| `git stash pop --index`       | Apply only staged changes from stash         |

---
### **8. Best Practices for Using `git stash`**
✅ **Use meaningful stash messages** – Helps track why you stashed changes.  
✅ **Avoid excessive stashing** – Stashes are temporary; commit frequently instead.  
✅ **Check stash contents before applying** – Use `git stash show -p` to verify.  
✅ **Use `git stash pop` cautiously** – If a stash is useful, apply it using `git stash apply` first.  
✅ **Clean up old stashes** – Avoid unnecessary clutter with `git stash drop` or `git stash clear`.

---

### **9. Conclusion**
`git stash` is a powerful tool that allows developers to manage temporary changes efficiently. Whether you need to switch branches, test new code, or move changes between branches, mastering `git stash` improves workflow and flexibility.