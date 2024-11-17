### **Extending LVM in Linux

When additional storage is required for a virtual machine (VM) hosted on platforms like **ESXi** or **VMWARE** or **OTHER**, it's common to expand the existing disk instead of adding a new one. Expanding the current disk minimizes fragmentation and performance issues. After increasing the disk capacity in the hypervisor, follow these steps to extend the **LVM (Logical Volume Manager)** in Ubuntu.

---
### **Step 1: Resizing the Partition**

1. **Launch the `fdisk` Tool**: Use the `fdisk` utility to resize the partition that hosts the LVM.    
    `sudo fdisk /dev/sda`
2. **Delete the Current Partition**: Select the partition to delete (e.g., `/dev/sda3`). **This does not delete data, only the partition entry.**
    `d `
    `3`
1. **Recreate the Partition**: Use the same partition number and ensure the start sector remains unchanged. This incorporates the newly added disk space.
```
n
3
> [Press Enter for the default first sector]
> [Press Enter for the default last sector]
```
4. **Do Not Add a New Signature**: When prompted, choose not to add a new partition signature to preserve the existing data.
    `N`
5. **Write the Changes**: Save the changes and exit `fdisk`.
    `w`
    The partition size is now updated.
---
### **Step 2: Extend the LVM**

1. **Resize the Physical Volume (PV)**: Update the physical volume to recognize the increased disk space.
    `sudo pvresize /dev/sda3`
    
2. **Extend the Logical Volume (LV)**: Allocate the newly added space to the logical volume. The `--extents +100%FREE` flag allocates all free space.
    `sudo lvextend --extents +100%FREE --resizefs /dev/ubuntu-vg/lv-0`
    - `--resizefs`: Automatically resizes the filesystem to match the new LV size.

---

### **Verifying the Changes**

1. Check the updated PV size:
    `sudo pvs`
    
2. Check the updated LV size:
    `sudo lvs`
    
3. Verify the new filesystem size:
    `df -h`

---

### **Conclusion**
By resizing the partition and extending the LVM, the additional disk space is successfully allocated. This approach ensures that the VM benefits from seamless storage expansion without fragmentation or performance degradation. Always back up critical data before making changes to partitions or logical volumes.