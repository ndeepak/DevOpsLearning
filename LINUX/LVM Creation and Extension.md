### Notes on Creating and Extending an LVM Disk
---
#### **1. Overview of LVM**
LVM (Logical Volume Manager) is a flexible disk management system for Linux. It allows dynamic resizing and management of disk partitions.

---
#### **2. Steps to Create an LVM Disk**
1. **Identify the New Disk**  
    Use the `lsblk` command to locate the new disk (e.g., `/dev/sdb`).
    `lsblk`
    
2. **Initialize the Disk as a Physical Volume (PV)**  
    Prepare the disk for LVM:
    `sudo pvcreate /dev/sdb`
    
3. **Create a Volume Group (VG)**  
    Combine one or more physical volumes into a volume group:
    `sudo vgcreate <volume_group_name> /dev/sdb`
    Example:
    `sudo vgcreate VG_WAZUH /dev/sdb`
    
4. **Create a Logical Volume (LV)**  
    Allocate space from the volume group to create a logical volume:
    `sudo lvcreate -L <size> -n <logical_volume_name> <volume_group_name>`
    Example:
    `sudo lvcreate -L 50G -n LV_WAZUH VG_WAZUH`
    
5. **Format the Logical Volume**  
    Format the logical volume with a filesystem (e.g., `ext4`):
    `sudo mkfs.ext4 /dev/<volume_group_name>/<logical_volume_name>`
    Example:
    `sudo mkfs.ext4 /dev/VG_WAZUH/LV_WAZUH`
    
6. **Mount the Logical Volume**  
    Create a directory and mount the logical volume:
    `sudo mkdir -p /mnt/<mount_point> `
    `sudo mount /dev/<volume_group_name>/<logical_volume_name> /mnt/<mount_point>`
    Example:    
    `sudo mkdir -p /home/cas/wazuh `
    `sudo mount /dev/VG_WAZUH/LV_WAZUH /home/cas/wazuh`
    
7. **Update `/etc/fstab` for Persistent Mount**  
    Add an entry in `/etc/fstab` for automatic mounting:
    `echo "/dev/VG_WAZUH/LV_WAZUH /home/cas/wazuh ext4 defaults 0 0" | sudo tee -a /etc/fstab`
---
#### **3. Steps to Extend an LVM Disk**
1. **Add a New Physical Volume**  
    Prepare the new disk for LVM:    
    `sudo pvcreate /dev/sdc`
    
2. **Extend the Volume Group**  
    Add the new disk to the existing volume group:
    `sudo vgextend <volume_group_name> /dev/sdc`
    Example:
    `sudo vgextend VG_WAZUH /dev/sdc`
    
3. **Extend the Logical Volume**  
    Allocate the new space to the existing logical volume:
    - To add a specific size:
        `sudo lvextend -L +<size> /dev/<volume_group_name>/<logical_volume_name>`
        
    - To use all available free space:
        `sudo lvextend -l +100%FREE /dev/<volume_group_name>/<logical_volume_name>`
    Example:
    `sudo lvextend -L +50G /dev/VG_WAZUH/LV_WAZUH `
    `sudo lvextend -l +100%FREE /dev/VG_WAZUH/LV_WAZUH`
    
4. **Resize the Filesystem**  
    Update the filesystem to use the extended space:    
    - For `ext4`:
        `sudo resize2fs /dev/<volume_group_name>/<logical_volume_name>`
        
    - For `xfs`:
        `sudo xfs_growfs /dev/<volume_group_name>/<logical_volume_name>`
    Example:
    `sudo resize2fs /dev/VG_WAZUH/LV_WAZUH`
    
5. **Verify the Changes**  
    Check the updated space:
    `df -h lsblk`

---
#### **4. Key Commands Summary**
- **Create Physical Volume:**  
    `pvcreate /dev/sdX`    
- **Create Volume Group:**  
    `vgcreate <VG_NAME> /dev/sdX`    
- **Create Logical Volume:**  
    `lvcreate -L <size> -n <LV_NAME> <VG_NAME>`    
- **Extend Volume Group:**  
    `vgextend <VG_NAME> /dev/sdX`    
- **Extend Logical Volume:**  
    `lvextend -L +<size> /dev/<VG_NAME>/<LV_NAME>`  
    or  
    `lvextend -l +100%FREE /dev/<VG_NAME>/<LV_NAME>`    
- **Resize Filesystem:**  
    `resize2fs /dev/<VG_NAME>/<LV_NAME>`  
    or  
    `xfs_growfs /dev/<VG_NAME>/<LV_NAME>`    

---
