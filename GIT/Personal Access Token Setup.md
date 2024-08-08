To avoid typing your username and password every time you push to GitLab, you can set up a personal access token or SSH keys for authentication. Using personal access tokens is generally more secure and straightforward for GitLab repositories.

### Method 1: Using Personal Access Token
1. **Generate a Personal Access Token in GitLab:**
    - Go to GitLab and sign in.
    - Navigate to your user settings (click on your avatar in the top right corner and select "Settings").
    - Go to "Access Tokens" in the left sidebar.
    - Fill in the name, expiry date, and scopes (select `api` and `write_repository`).
    - Click "Create personal access token".
    - Copy the generated token and store it securely.

1. **Configure Git to Use the Token:**    
    - Edit your Git remote URL to include the token.
    - Replace the remote URL in your repository with the following format:
                `git remote set-url origin https://<username>:<personal_access_token>@gitlab.cas.com.np/cas/infra/bpm-ci.git`
        
    
    Example:
        `git remote set-url origin https://deepak.nagarkoti@cas.com.np:<personal_access_token>@gitlab.cas.com.np/cas/infra/bpm-ci.git`
    
3. **Push Your Changes:** Now you should be able to push your changes without being prompted for a username and password.
    

### Method 2: Using SSH Keys
1. **Generate SSH Keys:**
    - Open a terminal and generate an SSH key pair if you don't already have one:
                `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
        
    - Follow the prompts to save the key in the default location (`~/.ssh/id_rsa`) and optionally add a passphrase.

2. **Add the SSH Key to the SSH Agent:**
    `eval "$(ssh-agent -s)" ssh-add ~/.ssh/id_rsa`
    
3. **Add the SSH Key to GitLab:** 
    - Go to GitLab and sign in.
    - Navigate to your user settings (click on your avatar in the top right corner and select "Settings").        
    - Go to "SSH Keys" in the left sidebar.    
    - Copy the contents of your public SSH key file (`~/.ssh/id_rsa.pub`):
                `cat ~/.ssh/id_rsa.pub`
    - Paste the key into the "Key" field in GitLab and click "Add key".

4. **Configure Git to Use SSH:**
    - Edit your Git remote URL to use SSH:
                `git remote set-url origin git@gitlab.cas.com.np:cas/infra/bpm-ci.git`
        
5. **Push Your Changes:** Now you should be able to push your changes without being prompted for a username and password.
### Summary
Using a personal access token or SSH keys can significantly streamline your workflow by removing the need to enter your username and password each time you interact with your GitLab repository. Both methods provide secure and efficient ways to authenticate with GitLab.