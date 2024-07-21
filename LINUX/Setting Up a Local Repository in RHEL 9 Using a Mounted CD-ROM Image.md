## Prerequisites
1. RHEL 9 installation DVD or ISO image.
2. A system running RHEL 9 with root privileges.
3. The ISO image mounted on the system.
## Steps
### Step 1: Mount the ISO Image

First, you need to mount the ISO image to a directory.

1. Create a directory to mount the ISO image:
    `mkdir -p /mnt/cdrom`
    
2. Mount the ISO image to the directory:
    `mount -o loop /path/to/rhel-9.iso /mnt/cdrom`
### Step 2: Create a Repository Configuration File
Create a `.repo` file in the `/etc/yum.repos.d/` directory to configure the local repository.
1. Create a new file named `local.repo`:
    `nano /etc/yum.repos.d/local.repo`
    
2. Add the following content to the `local.repo` file:    
```
    [local] name=RHEL 9 Local Repository 
    baseurl=file:///mnt/cdrom 
    enabled=1 
    gpgcheck=1 
    gpgkey=file:///mnt/cdrom/RPM-GPG-KEY-redhat-release
    # or simply, gpgcheck=0
```
3. Save and close the file.
### Step 3: Disable Other Repositories (Optional)
If you want to ensure that only the local repository is used, you can disable all other repositories.
1. Edit the repository configuration files in `/etc/yum.repos.d/` and set `enabled=0` for each repository, except for the local repository.

### Step 4: Clean YUM Cache and Verify the Repository

1. Clean the YUM cache:    
    `yum clean all`
    
2. Verify the repository:
        `yum repolist`
    
    You should see the `RHEL 9 Local Repository` listed.
### Step 5: Install Packages from the Local Repository
Now you can install packages from your local repository.
1. For example, to install the `httpd` package:
    `yum install httpd`

### Step 6: Unmount the ISO Image (Optional)
If you no longer need the ISO image mounted, you can unmount it.
1. Unmount the ISO image:
        `umount /mnt/cdrom`
### Notes
- Ensure the `baseurl` in the `.repo` file points to the correct mount point of your ISO image.
- If the ISO image is unmounted, the repository will no longer be available.
- The `gpgkey` line ensures the packages are verified with the GPG key provided in the ISO.

By following these steps, you will have a local repository set up in RHEL 9 using a mounted CD-ROM image. This setup is useful for installing packages on systems without direct internet access.