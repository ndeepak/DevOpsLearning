### Git Merge, Rebase, and Squash: Concepts, Use Cases, and Examples
#### 1. **Git Merge**
---
**Git Merge** is a way to combine the changes from one branch into another. It creates a new merge commit that represents the integration of two or more branches.
##### **Use Case:**
- **Scenario**: When you have been working on a feature branch and are ready to merge it into the main branch.
- **Best for**: Preserving the full history of development, especially in team projects where visibility of the entire branch history is essential.

##### **Example:**
Suppose you're working on a feature branch called `feature-branch` and want to merge it into `main`.
```
# Switch to the main branch
git checkout main

# Merge the feature branch into main
git merge feature-branch
```
After merging, a new merge commit is created that contains the combined work of both branches.

##### **Advantages:**
- Retains the entire history of both branches.
- Easy to track which branches were merged and when.

##### **Disadvantages:**
- Can create extra merge commits that clutter the commit history, especially if multiple small branches are frequently merged.

#### 2. **Git Rebase**
---
**Git Rebase** is a powerful tool that moves or "rebases" the commits from one branch on top of another, effectively rewriting history to create a linear commit timeline.

##### **Use Case:**
- **Scenario**: You have a feature branch and want to integrate it with the latest changes from the main branch without creating merge commits.
- **Best for**: Keeping a clean, linear project history, often used in solo projects or feature branches before merging.

##### **Example:**
If you have been working on `feature-branch` and `main` has been updated by others, you can rebase your changes on top of the latest `main`.
```
# Switch to your feature branch
git checkout feature-branch

# Rebase your feature branch on top of the main branch
git rebase main
```
During the rebase, Git applies each commit from your feature branch on top of the `main` branch. This creates a clean, linear history.

If there are conflicts, Git will pause the process and allow you to manually resolve them.
```
# Resolve conflicts, then add the resolved files
git add <file>

# Continue the rebase process
git rebase --continue
```
##### **Advantages:**
- Creates a clean and linear history.
- Avoids unnecessary merge commits.

##### **Disadvantages:**
- Can be risky if done incorrectly, as it rewrites commit history. It’s not recommended for shared or public branches.

##### **Golden Rule**: Never rebase commits that have been pushed to a shared repository, as it can confuse collaborators.

#### 3. **Git Squash**
---
**Git Squash** combines multiple commits into one. It is typically used when you want to clean up your commit history before merging a feature branch into the main branch.

##### **Use Case:**
- **Scenario**: You have made multiple small commits while working on a feature and want to combine them into a single, clean commit before merging.
- **Best for**: Reducing clutter in commit history, especially when a series of small commits doesn't provide meaningful context individually.

##### **Example:**
Let's say you have three commits on your `feature-branch` that you want to squash into one.
1. **Interactive Rebase**:
```
# Start an interactive rebase for the last 3 commits
git rebase -i HEAD~3
```

This command opens up your editor, where you can decide how to handle each commit. To squash all commits into one, modify the lines to say `squash` (or `s`):
```
pick 1a2b3c4 Commit 1
squash 2b3c4d5 Commit 2
squash 3c4d5e6 Commit 3
```

2. After saving and closing the editor, Git will squash the commits into one. You’ll then be asked to combine the commit messages:

`# Commit message for the combined commit`

3. **Force Push (If Required)**:
```
# Push the changes to the remote repository
git push --force-with-lease
```

##### **Advantages:**
- Clean, easy-to-read commit history.
- Makes feature branches more manageable and easier to review.

##### **Disadvantages:**
- Like rebase, it rewrites history, so avoid squashing commits that have already been shared with others.

---

### Summary: When to Use Merge, Rebase, and Squash

|Command|Best Use Case|Pros|Cons|
|---|---|---|---|
|**git merge**|Combining branches while keeping full history|Keeps the history intact and shows full context of changes|Can clutter history with merge commits|
|**git rebase**|Integrating feature branches into mainline history|Creates a clean, linear history with no extra merge commits|Rewrites history, risky for public branches|
|**git squash**|Cleaning up commits before merging|Combines multiple commits into one for a clean history|Rewrites history, should only be done locally|

---

### Workflow Example:
1. **Develop Feature Branch**:
```
git checkout -b feature-branch
# Make changes, commit as needed
git commit -m "Add new feature"
```
2. **Rebase Before Merge**:
```
git checkout feature-branch
git rebase main
```
3. **Squash Commits**:
    `git rebase -i HEAD~3`
    
4. **Merge into Main**:  
    `git checkout main git merge feature-branch`
    
5. **Push Changes**:
    `git push origin main`
    

By understanding these commands, you can make more informed decisions about how to manage your Git history in different development scenarios.