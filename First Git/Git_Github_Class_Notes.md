## Version Control Systems (VCS)

### What is SCM/VCS/RCS?

- **SCM**: Source Code Management
- **VCS**: Version Control System
- **RCS**: Revision Control System

### Why Do We Need VCS?

- **Track Changes**: Maintain a history of modifications to the codebase.
- **Collaboration**: Allow multiple developers to work on the same project simultaneously.
- **Backup**: Keep a backup of the code.
- **Branching and Merging**: Work on different features or fixes in parallel without affecting the main codebase.
- **Revert Changes**: Undo changes and revert to previous versions if needed.

### VCS Features

- **Branching and Merging**: Create branches for new features or bug fixes and merge them back into the main branch.
- **Commit History**: Track the history of changes with commit messages.
- **Diff and Merge Tools**: Compare changes and resolve conflicts.
- **Access Control**: Restrict who can make changes to the codebase.
- **Tagging**: Mark specific points in history as important.

### Official Documentation

- Refer to the **ProGit** book for detailed documentation and advanced topics.

---

## GIT Installation on Ubuntu

### Install Git

`$ sudo apt-get update $ sudo apt-get install git`

### Verify Installation

`$ which git `
`$ git version`

### Uninstall Git

`$ sudo apt-get remove git`

---
## Git Architecture

### End-to-End Git Workflow

1. **Clone Repository**:
         `git clone <repository_url>`
    
2. **Create Branch**:
 
    `git checkout -b <branch_name>`
    
3. **Make Changes**: Modify files as needed.
4. **Stage Changes**:
    `git add <file>`
    
5. **Commit Changes**:
    `git commit -m "commit message"`    
6. **Push Changes**:
        `git push origin <branch_name>`
    
7. **Create Pull Request**: Merge changes into the main branch through a pull request.

---

### Creating a Remote Repository in GitHub

1. **Create an Account on GitHub**:
        - Visit [GitHub](https://github.com) and sign up for an account.
2. **Login to GitHub**:
        - Use your credentials to log in.
3. **Create a New Repository**:
        - Click on "New" and provide a name (e.g., "ecommerce").
    - Click "Create repository".
4. **Copy the Repository URL**:
        - For example: `https://github.com/username/ecommerce.git`
5. **Clone the Repository**:
     `git clone https://github.com/username/ecommerce.git`
    
6. **Navigate to the Cloned Repository**:
    - Change directory to the cloned repository:   
        `cd ecommerce`
            - Observe the `.git` folder, which is your local repository.
7. **Create and Submit Code to the Remote Repository**:
        - Create a sample file:
               `touch Login.java`
            - Stage the file:
            `git add Login.java`
        
    - Commit the changes:
            `git commit -m "login module code"`
        
    - Push the changes (refer to GitHub documentation to generate a token if needed for authentication):   
        `git push`
        
    - View the commit log:
            `git log Login.java`

--------------------------------------------------------------------------
## Setting up Token/Password to Access GitHub

### Steps to Generate and Use a GitHub Token

1. **Visit GitHub**:
    - Go to [GitHub](https://github.com).
2. **Generate Token from GitHub**:
    - Click on the user profile icon (top right).
    - Click on 'Settings'.
    - Click on 'Developer settings'.
    - Click on 'Personal access tokens'.
    - Click on 'Generate new token'.
    - Provide a name under 'Note' (e.g., "class").
    - Select 'No expiration' from the 'Expiration' drop-down box.
    - Click on the 'repo' checkbox under 'Select scopes'.
    - Click on the 'Generate token' button.
3. **Store the Token on Your Machine**:
    `git remote set-url origin <github-link>`
    - Note: In the above command:
        - `username` is your GitHub username.
        - `sdsddfsdfsdfsdf` is your token generated from GitHub.
        - `github.com/user/repo` is your repository path (omit 'https').

---

## Staging Index/Stage
### Skip Staging
- **Commit All Pending Changes**:
    `git commit -am "submit all pending changes"`
    - Note: If you want to skip the staging step, you need to commit all pending changes. For new files, you must go through the 'stage' process.

---

## Show All Files Modified in a Commit (with Content)

`git show <commit_id> git show b85a6e123`

---
## Git Commit Structure
- **SHA Value / Commit ID**
- **User & Email**
- **Date & Timestamp**
- **Commit Message**
--------------------------------------------------------------------------
## Setting up Mandatory Configurations

### Configure Git with Your Information

`$ git config --global user.name "Your Name"` 
`$ git config --global user.email "your Email"`

### Verify Configurations
`$ git config --list`

- Git stores all configurations in the following file:
    - `$USER_HOME/.gitconfig`

---

## Understand Git Jargon

### Key Terms

- **Remote Repository**: The version of your project that is hosted on a server, such as GitHub or GitLab.
- **Working Directory**: The local directory where you are currently working and making changes.
- **Local Repository**: The version of your project stored on your local machine.
- **Stage/"Staging Index"**: The area where you can format and prepare your changes before committing them.
- **SHA**: A unique identifier for each commit, used to keep track of changes.

---
## History

### View Commit History for a Specific File
`$ git log Login.java`

### View Complete Commit History
`$ git log`

## GIT Commands

### Show all commits made by user "Ram" with a commit message containing "math function"
`$ git log --author="Ram" --grep="math function"`
### Viewing File Changes
1. **See the content change of a file in the 'source' area:**
`$ git diff Login.java`
2. **See the content change of a file in the 'stage' area:**
`$ git diff --staged Login.java`
3. **See the content change of a file after a commit:**
`$ git show 123abc456`

---
### Deleting a File
1. **Delete the file and add it to the staged area:**
`git rm OMS.java`
2. **Commit and push the changes:**
`git commit OMS.java -m "comment" git push`

---
### Renaming a File/Folder

1. **Rename a file:**
`git mv Login.java Login1.java`

2. **Commit and push the changes:**
`git commit -m "rename Login" git push`

**Note:** Git will carry the history of the old file to the new file. To check the complete history:
`$ git log $ git log --follow Login1.java`

---
### Undoing Changes

1. **Undo/revert local changes from the source area:**
`$ git restore LoginWeb.java`

2. **Unstage the changes from the STAGE area:**
`$ git restore --staged LoginWeb.java`

3. **Add all changes and check the status:**
`$ git add . $ git status`

4. **Reset the HEAD for a specific file:**
`$ git reset HEAD filename`

---
## Branching

### A. What is a Branch?

- A branch in Git is a lightweight movable pointer to a commit. It allows you to isolate your work from other changes in the project.

### B. Why and When Do We Create a Branch?

- **Why:** To work on new features, bug fixes, or experiments in isolation.
- **When:** Before starting any new task that could impact the main codebase, to keep the main branch stable and clean.

### C. Branching Strategies

- **Feature Branching:** Create a new branch for each feature.
- **Release Branching:** Create branches to prepare for production releases.
- **Hotfix Branching:** Create branches for urgent fixes to production code.

---

### Git Commands for Branching

#### List All Active Branches in the Local Repository
`$ git branch -a`

#### Creating a New Branch
`$ git branch dev_1.2.3`

#### Push New Branch to Remote Repository
`$ git push origin dev_1.2.3`

#### Switching from One Branch to Another
`$ git checkout dev_1.2.3`

#### Creating and Switching to a Newly Created Branch
`$ git checkout -b dev_1.2.4`

#### Clone a Remote Repository with a Particular Branch as Default
`$ git clone -b dev_1.2.4 https://github.com/nageshvkn/flipkart899.git`

#### List All Remote Branches
`$ git branch -r`

#### Deleting a Branch
`$ git branch -d dev_1.2.3 `
`$ git push -d origin dev_1.2.3`

---
## Merging

### List All Branches
`$ git branch`

### Create a New Branch
`$ git branch dev_1.2.3`

### Merge Workflow Example

#### 1. Modify the Same File in Different Branches to Create a Conflict

**Common File: `Login.java`**

- **In `master` Branch:**
    `int a = 100;`
    
- **In `dev_1.2.3` Branch:**
    `int a = 200;`
    

#### 2. Switch to the Target Branch (`master`)
`$ git checkout master`

#### 3. Merge the Source Branch (`dev_1.2.3`) into the Target Branch (`master`)
`$ git merge dev_1.2.3`

#### 4. Handle Merge Conflicts

- Run `git status` to see the conflicted files.
- Open the conflicted file (`Login.java`), resolve the conflict manually, and save the changes.

**Example Conflict Resolution:**

`// Resolve the conflict by choosing one of the following or combining them:` 
`int a = 100; // or int a = 200;
`
#### 5. Add the Resolved File
`$ git add Login.java`

#### 6. Commit the Merge
`$ git commit -m "Resolved merge conflict between master and dev_1.2.3"`

#### 7. Push the Changes to the Remote Repository
` $ git push`

---

## What is a Conflict?

A conflict occurs when two users modify the same file in different branches and the same line has different content. Git can't automatically decide which changes to keep. This situation is called a conflict.

## Example of Creating and Resolving a Conflict

### Step 1: Setup

1. **Create a new branch:**
        `$ git branch dev_1.2.3 $ git checkout dev_1.2.3`
    
2. **Modify the file in the new branch (`dev_1.2.3`):**
    `// Login.java in dev_1.2.3 branch int a = 200;`
        `$ git add Login.java $ git commit -m "Modified a in dev_1.2.3" $ git push origin dev_1.2.3`
    
3. **Switch back to the master branch and modify the same file:**
    `$ git checkout master`
        `// Login.java in master branch int a = 100;`
    
    `$ git add Login.java $ git commit -m "Modified a in master" $ git push origin master`
    

### Step 2: Create the Conflict

1. **Merge the `dev_1.2.3` branch into `master`:**
    `$ git checkout master $ git merge dev_1.2.3`
    
    Git will detect a conflict:
        `Auto-merging Login.java CONFLICT (content): Merge conflict in Login.java Automatic merge failed; fix conflicts and then commit the result.`
    

### Step 3: Resolve the Conflict

1. **Open the conflicted file (`Login.java`):**
    `<<<<<<< HEAD int a = 100; ======= int a = 200; >>>>>>> dev_1.2.3`
    
2. **Resolve the conflict:**
    
    - Remove conflict markers `<<<<<<<`, `=======`, `>>>>>>>`.
    - Choose the correct content based on the discussion with developers.
   
    `int a = 100; // or int a = 200; or any other resolution.`
    
3. **Add the resolved file:**
        `$ git add Login.java`
    
4. **Commit the merge:**
        `$ git commit -m "Resolved merge conflict between master and dev_1.2.3"`
    
5. **Push the changes to the remote repository:**
        `$ git push origin master`
    

### Finding the Owner of the Conflict

Use the `git blame` command to find the user who modified/added the conflicted code:
`$ git blame Login.java`

---

## Git Remote Operations

### PULL

Fetches and integrates changes from the remote repository into the current branch:

`$ git pull origin <branch_name>`

### FETCH

Downloads changes from the remote repository but does not integrate them into the current branch:
`$ git fetch origin`

### PUSH

Uploads changes from the local repository to the remote repository:
`$ git push origin <branch_name>`

### CLONE

Creates a copy of an existing remote repository:
`$ git clone <repository_url>`