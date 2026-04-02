# Installing Go (Golang) on Kali Linux — Clean, Safe, and Future-Proof

If you’re working on Kali Linux—whether for development, automation, or security research—**Go (Golang)** is one of those languages you’ll keep coming back to. It’s fast, simple, secure by design, and incredibly good at handling concurrency.

Go was created by Google with a clear goal: make it easy to build reliable and scalable systems without unnecessary complexity. Today, it powers everything from cloud platforms and DevOps tools to security scanners and network services.

This guide walks you through installing Go on Kali Linux in a way that is:
- **Evergreen** (no hard-coded versions)    
- **Safe** (won’t destroy an existing setup)    
- **Official** (uses Go’s recommended installation method)    

---
## Why Install Go Manually on Kali?

Kali’s repositories often lag behind the latest Go releases. Installing Go directly from the official source gives you:
- The **latest stable version**    
- A clean, predictable directory layout    
- Easy upgrades without dependency issues    
Once installed, Go takes care of the rest.

---
## Step 1: Download the Latest Go Release
Always grab Go from the official source:
`https://go.dev/dl/`

Choose the **Linux amd64** archive (or ARM if applicable), then download it:
`wget https://go.dev/dl/go<latest>.linux-amd64.tar.gz`

> Replace `<latest>` with the version currently listed on the Go website.

---

## Step 2: Extract Go Safely (Without Breaking Existing Installations)
Instead of deleting an existing Go installation immediately, extract the new version **alongside** your current setup first.
`sudo tar -C /usr/local -xzf go<latest>.linux-amd64.tar.gz`

This will extract Go into:
`/usr/local/go`

If Go is already installed, **do not proceed yet**—verify first.

---

## Step 3: Check If Go Is Already Installed
Run:
`go version`
If Go is already present and working, you have two safe options:

### Option A: Keep the Existing Version
If everything works and you don’t need the latest release, you’re done.

### Option B: Upgrade Cleanly (Recommended)
Once you’re sure you want to upgrade, remove the old version and extract the new one **in a controlled way**:
`sudo rm -rf /usr/local/go sudo tar -C /usr/local -xzf go<latest>.linux-amd64.tar.gz`

This ensures:
- No leftover files    
- No mixed versions    
- A clean Go installation    

---

## Step 4: Add Go to Your PATH
### Bash users
Edit your `.bashrc`:
`nano ~/.bashrc`

Add:
`export PATH=$PATH:/usr/local/go/bin`

Apply changes:
`source ~/.bashrc`

---
### Zsh users (default on newer Kali)
Edit `.zshrc`:
`nano ~/.zshrc`

Add:
`export PATH=$PATH:/usr/local/go/bin`

Reload:
`source ~/.zshrc`

---
## Step 5: Verify the Installation
`go version`

You should see output like:
`go version goX.Y.Z linux/amd64`

(The version number will vary—and that’s the point.)

---
## Optional: Set Up a Go Workspace
Go modules work anywhere, but a workspace is still useful:
`mkdir -p ~/go/{bin,src,pkg}`

Optionally add:
`export GOPATH=$HOME/go export PATH=$PATH:$GOPATH/bin`

---

## Updating Go in the Future
Updating Go is simple and repeatable:
1. Download the latest archive    
2. Remove the old installation (if upgrading)    
3. Extract the new one    
4. Verify with `go version`    

No additional cleanup required.

---

## Final Thoughts
Go feels right on Kali Linux. It’s fast, predictable, and built for serious work—whether that’s backend development, tooling, or security research. By installing it manually from the official source, you get full control and future-proof stability.

Install it once, upgrade it cleanly, and let Go do what it does best.