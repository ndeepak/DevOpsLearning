### **Ephemeral File System in Docker – Practical Examples**

---
### **1. Demonstrating Ephemeral Storage:**
**Step 1: Create a Docker Container and Write Data**
Run an `Ubuntu` container and create a file inside it:
`docker run -it --name ephemeral-test ubuntu bash`

Inside the container:
`echo "This is a test file" > /testfile.txt cat /testfile.txt   # Verify the content`

**Step 2: Exit and Remove the Container**
Exit the container:
`exit`

Remove the container:
`docker rm ephemeral-test`

**Step 3: Re-run the Same Image and Check Data**
Start a new container:
`docker run -it ubuntu bash`

Check if the file exists:
`ls /testfile.txt`

**Outcome:**  
The file does **not** exist, demonstrating the ephemeral nature of container storage.

---
### **2. Using Volumes for Persistent Storage:**
**Step 1: Create a Docker Volume**
`docker volume create mydata`

**Step 2: Start a Container with the Volume**
`docker run -it -v mydata:/data --name volume-test ubuntu bash`

Inside the container:
```
echo "Persistent Data" > /data/persistent.txt
cat /data/persistent.txt   # Verify the content
```

**Step 3: Remove and Recreate the Container**
Exit and remove the container:
`exit docker rm volume-test`

Start a new container using the same volume:
`docker run -it -v mydata:/data ubuntu bash`

Verify the data:
`cat /data/persistent.txt`

**Outcome:**  
The file persists because it’s stored in the Docker volume.

---
### **3. Using Bind Mounts for Data Persistence:**
**Step 1: Create a Directory on the Host**
```
mkdir ~/docker-data
echo "Bind Mount Data" > ~/docker-data/bindfile.txt
```
**Step 2: Run a Container Using Bind Mount**
`docker run -it -v ~/docker-data:/app --name bind-mount-test ubuntu bash`

Inside the container:
`cat /app/bindfile.txt  # Access the file from the host`

**Step 3: Modify the File in the Container**
`echo "Updated from container" >> /app/bindfile.txt`

**Step 4: Check the File on the Host**
Exit the container and check the file on the host:
`cat ~/docker-data/bindfile.txt`

**Outcome:**  
Changes made in the container are reflected on the host.

---
### **4. Demonstrating Tmpfs Mounts:**

**Step 1: Run a Container with Tmpfs**
`docker run -it --tmpfs /tmpfs:rw,size=64m --name tmpfs-test ubuntu bash`

Inside the container:
```
echo "Tmpfs Data" > /tmpfs/tmpfile.txt
cat /tmpfs/tmpfile.txt
```
**Step 2: Exit and Remove the Container**
`exit `
`docker rm tmpfs-test`

**Step 3: Re-run the Container and Verify**
Start the container again:
`docker run -it --tmpfs /tmpfs:rw,size=64m ubuntu bash`

Check the `/tmpfs` directory:
`ls /tmpfs`

**Outcome:**  
The file is gone, as tmpfs mounts store data in memory and do not persist.

---
### **Summary:**
- **Ephemeral Storage:** Data in the container’s default file system is lost when the container is removed.
- **Volumes:** Persistent storage managed by Docker, ideal for data that needs to be retained.
- **Bind Mounts:** Direct mapping to a host directory, useful for development and sharing files.
- **Tmpfs:** Temporary in-memory storage, useful for sensitive or non-persistent data.

These practical examples help ensure your containerized applications handle data appropriately, whether temporary or persistent.