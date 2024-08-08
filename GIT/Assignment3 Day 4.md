### Git Commands Learning Assignment
---
#### **1. Introduction to Version Control and Git**
- **Objective:** Understand version control and Git's role in software development.
- **Tasks:**
    1. **Research:** Learn what version control is and why it’s crucial in software development.
    2. **Types of VCS:** Identify the differences between centralized and distributed version control systems.
    3. **Understand Git:** Learn about Git’s architecture and how it works as a distributed version control system.
    4. **Explore Git Features:** Identify key features of Git such as branching, merging, and offline work.
- **Resources:**
    - [Learn Git Branching](https://learngitbranching.js.org/)
    - [Git Documentation](https://git-scm.com/doc)

#### **2. Basic Git Setup**
- **Objective:** Set up Git on your machine and understand the basic Git workflow.
- **Tasks:**
    
    1. **Install Git:** Follow instructions to install Git on your operating system.
    2. **Configure Git:** Set up your name and email to be used in commits.
```
git config --global user.name "Your Name" 
git config --global user.email "your.email@example.com"

OR For Local Repo setting only,
git config --local user.name "Your Name" 
git config --local user.email "your.email@example.com"
```

	3. **Understand Git Workflow:** Learn about the working directory, staging area, and repository. Understand how changes move between these states.
- **Resources:**
    
    - [Git Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
    - [Git Configuration](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)

#### **3. Repository Management**
- **Objective:** Learn how to create, clone, and manage repositories.
- **Tasks:**
    
    1. **Initialize a Repository:**        
        `git init`
        
    2. **Clone a Repository:** Clone an existing repository to your local machine.
        `git clone <repository-url>`
        
    3. **Understand Repository Structure:** Explore the `.git` folder in a repository and understand its purpose.
- **Resources:**
    - [Git Init and Clone](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)

#### **4. Tracking and Staging Changes**
- **Objective:** Learn how to track and stage changes in Git.
- **Tasks:**
    1. **Track New Files and Changes:** Use the `git add` command to track files.
        `git add <file>  git add .`
        
    2. **Check Status:** Understand the state of your working directory.
        `git status`
        
    3. **View Changes:** Use `git diff` to see changes between your working directory and the staging area.       
        `git diff`
        
- **Resources:**
    - [Git Add and Status](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)

#### **5. Committing Changes**
- **Objective:** Learn how to commit changes to your repository.
- **Tasks:**
    1. **Commit Changes:** Write meaningful commit messages and commit staged changes.
        `git commit -m "Commit message"`
        
    2. **Amend a Commit:** Modify the most recent commit if needed.
        `git commit --amend`
        
- **Resources:**
    - [Git Commit](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)

#### **6. Working with Branches**
- **Objective:** Understand how to create, switch, and manage branches in Git.
- **Tasks:**
    1. **List Branches:**
        `git branch`
        
    2. **Create a New Branch:**
        `git branch <branch-name>`
        
    3. **Switch to a Branch:**        
        `git checkout <branch-name>`
        
    4. **Create and Switch to a New Branch:**
        `git checkout -b <branch-name>`
        
- **Resources:**    
    - [Git Branching](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)

#### **7. Merging and Resolving Conflicts**
- **Objective:** Learn how to merge branches and resolve conflicts in Git.
- **Tasks:**
    1. **Merge a Branch:** Merge changes from one branch into another.
        `git merge <branch-name>`
        
    2. **Resolve Conflicts:** Handle merge conflicts and commit the resolution.       
```
git add <file>
git commit -m "Resolved merge conflicts"
```
        
- **Resources:**
    - [Merging in Git](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)

#### **8. Synchronizing with Remote Repositories**
- **Objective:** Learn how to work with remote repositories.
- **Tasks:**
    1. **List Remote Repositories:**
        `git remote -v`
        
    2. **Add a New Remote Repository:**
        `git remote add <remote-name> <repository-url>`
        
    3. **Fetch Changes:** Fetch updates from a remote repository.
        `git fetch <remote-name>`
        
    4. **Pull and Push Changes:** Synchronize your local repository with the remote.
```
git pull <remote-name> <branch-name>
git push <remote-name> <branch-name>
```
        
- **Resources:**
    - [Git Remote](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)

#### **9. Additional Git Commands**
- **Objective:** Explore additional Git commands and features.
- **Tasks:**
    1. **Create a Tag:**
        `git tag <tag-name>`
        
    2. **View Commit History:**
	   `git log`
	   `git log --graph --oneline

	3. **Revert a Commit:**
        `git revert <commit-hash>`
        
    4. **Reset to a Previous Commit:**
        `git reset --hard <commit-hash>`
        
    5. **Stash Changes:**
```
git stash
git stash apply
```
        
- **Resources:**
    - [Advanced Git Commands](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning)

### **Practical Exercises**
1. **Interactive Git Learning:** Use [Learn Git Branching](https://learngitbranching.js.org/) to practice branching, merging, and other Git operations in an interactive environment.
    
2. **Scenario-Based Tasks:**
    - Scenario 1: Initialize a new repository, create branches, make commits, and push changes to a remote repository.
    - Scenario 2: Simulate a merge conflict by creating conflicting changes in two branches, then resolve the conflict.
    - Scenario 3: Revert a commit that introduced a bug, then use reset to undo local changes.

### **Assessment**
- Successfully complete the interactive Git exercises.
- Demonstrate proficiency by managing a small project repository, including initializing, committing, branching, merging, and pushing to a remote repository.
- Explain the differences between `git revert` and `git reset` and when to use each.

### **Additional Resources**
- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Learning Lab](https://lab.github.com/)

This assignment will guide you through the essential Git commands and concepts, helping you develop a strong foundation in version control. By the end of these exercises, you should be comfortable with managing Git repositories, resolving conflicts, and collaborating on projects.