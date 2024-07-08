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

---

## Git Configuration Example

### Setting Up Mandatory Configurations



`$ git config --global user.name "Nageswara Rao P" $ git config --global user.email "nageshvkn@gmail.com"`

### Checking Configurations


`$ git config --list`

### Configuration Storage

Git stores all configurations in the file:


`$USER_HOME/.gitconfig`

---

## Git Jargon

- **Remote Repository**: The version of your project hosted on a server, like GitHub.
- **Working Directory**: The files that you see in your computer's file system.
- **Local Repository**: The version of your project that you have saved on your local machine.
- **Stage/"Staging Index"**: The area where git tracks changes to files before you commit them.
- **SHA**: A unique identifier for each commit.

### Git History



`$ git log Login.java $ git log`

---

## Git Commands

### Show All Commits by User "Ram" with "math function" in the Message



`$ git log --author="Ram" --grep="math function"`

### See Content Changes

1. **See the content change of a file in the 'source' area:**
    
    
    `$ git diff Login.java`
    
2. **See the content change of a file in the 'stage' area:**
    
    
    `$ git diff --staged Login.java`
    
3. **See the content change of a file after the commit:**
    
    
    
    `$ git show 123abc456`
    

### Deleting a File

1. Delete the file and add it to the staged area:
    

    
    `$ git rm OMS.java $ git commit -m "Removed OMS.java" $ git push`
    

### Renaming a File/Folder

1. Rename the file and commit the changes:
    
    
    `$ git mv Login.java Login1.java $ git commit -m "Renamed Login to Login1" $ git push`
    
    - Git will carry the history of the old file to the new file. To check the complete history:
    

    
    `$ git log $ git log --follow Login1.java`
    

### Undoing Changes

1. **Undo/Revert local changes from the source area:**

    
    `$ git restore LoginWeb.java`
    
2. **Unstage the changes from the staging area:**

    
    `$ git restore --staged LoginWeb.java $ git add . $ git status $ git reset HEAD <filename>`
    

---

## Branching

### What is a Branch?

A branch in Git is a lightweight movable pointer to one of these commits. The default branch name in Git is `master`. As you start making commits, you're given a master branch that points to the last commit you made.

### Why and When We Create a Branch?

Branches allow you to work on different parts of a project without affecting the main codebase. You create a branch to work on new features, bug fixes, or experiments.

### Branching Strategies

- **Feature Branching**: Create a new branch for each feature.
- **Release Branching**: Create a branch for each release.
- **Hotfix Branching**: Create a branch for urgent fixes.

### Git Branching Commands

- **List All Active Branches in Local Repository:**
    
    
    `$ git branch -a`
    
- **Create a New Branch:**

    
    `$ git branch dev_1.2.3`
    
- **Push New Branch to Remote Repository:**

    
    `$ git push origin dev_1.2.3`
    
- **Switch from One Branch to Another:**
    

    
    `$ git checkout dev_1.2.3`
    
- **Create and Switch to a Newly Created Branch:**
    

    `$ git checkout -b dev_1.2.4`
    
- **Clone a Remote Repository with a Particular Branch as Default:**

    
    `$ git clone -b dev_1.2.4 https://github.com/nageshvkn/flipkart899.git`
    
- **List All Remote Branches:**

    
    `$ git branch -r`
    
- **Deleting a Branch:**
    

    
    `$ git branch -d dev_1.2.3 $ git push origin --delete dev_1.2.3`
    

---

## Setting Up Token/Password to Access GitHub

1. **Generate Token from GitHub:**
    
    - Go to [https://github.com](https://github.com)
    - Click on the user-profile icon (top right).
    - Click on 'Settings'.
    - Click on 'Developer settings'.
    - Click on 'Personal access tokens'.
    - Click on 'Generate new token'.
    - Give a name under 'Note' (example: class).
    - Select 'No expiration' from the 'Expiration' drop-down box.
    - Click on the 'repo' checkbox under 'Select scopes'.
    - Click on 'Generate token'.
2. **Store the Token in Your Machine Using Below Command:**
    
    
    `$ git remote set-url origin <github-link>`
    
    - `username` is your GitHub username.
    - `sdsddfsdfsdfsdf` is your token generated from GitHub.
    - `github.com/user/repo` is your repository path. Don't include 'https'.

---

## Staging Index/Stage

- **Skip Staging:**
    
    
    `$ git commit -am "submit all pending changes"`
    
    **Note:** If you want to skip the staging, you need to commit all pending changes. For new files, you have to go through the 'stage' process.
    

---

## Git Commit Structure

- **SHA Value / Commit ID**
- **User & Email**
- **Date & Timestamp**
- **Commit