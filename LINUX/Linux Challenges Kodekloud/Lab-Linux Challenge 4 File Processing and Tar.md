# Lab-Linux Challenge 4
Some of our apps generate some raw data and store the same in `/home/bob/preserved` directory. We want to clean and manipulate some data and then want to create an `archive` of that data
`Note:` The validation will verify the final processed data so some of the tests might fail till all data is processed as asked.
Inspect the requirements in detail by clicking on the icons of the interactive architecture diagram on the right and complete the tasks. Once done click on the `Check` button to validate your work.
Do not delete any files from "/home/bob/preserved" directory.

![](LINUX/Linux%20Challenges%20Kodekloud/Attachments/Pasted%20image%2020260409163744.png)


```bash
sudo su -
```
---
## /home/bob/preserved
Do not delete any files from "/home/bob/preserved" directory.

## /opt/appdata  
Create "/opt/appdata" directory.
`mkdir /opt/appdata`

## filter.sh
Create a script called "/home/bob/filter.sh".
`echo "#!/bin/bash" > /home/bob/filter.sh`

## find
Find the "hidden" files in "/home/bob/preserved" directory and copy them in "/opt/appdata/hidden/" directory (create the destination directory if doesn't exist).
```bash
find /home/bob/preserved/ -type f -name ".*" -exec cp {} /opt/appdata/hidden/ \;
```

Find the "non-hidden" files in "/home/bob/preserved" directory and copy them in "/opt/appdata/files/" directory (create the destination directory if doesn't exist).
```bash
find /home/bob/preserved/ -type f ! -name ".*" -exec cp {} /opt/appdata/files/ \;
```

Find and delete the files in "/opt/appdata" directory that contain a word ending with the letter "t" (case sensitive).
```bash
rm -f $(find /opt/appdata/ -type f -exec grep -l 't\>' "{}"  \; )
```

## replace
Change all the occurrences of the word "yes" to "no" in all files present under "/opt/appdata/" directory.
```bash
find /opt/appdata -type f -name "*" -exec sed -i 's/\byes\b/no/g' "{}" \;
```

Change all the occurrences of the word "raw" to "processed" in all files present under "/opt/appdata/" directory. It must be a "case-insensitive" replacement, means all words must be replaced like "raw , Raw , RAW" etc.
```bash
find /opt/appdata -type f -name "*" -exec sed -i 's/\braw\b/processed/ig' "{}" \;
```

## appdata.tar.gz  
Create a "tar.gz" archive of "/opt/appdata" directory and save the archive to this file: "/opt/appdata.tar.gz"
```bash
cd /opt
tar -zcf appdata.tar.gz appdata
```
The "appdata.tar.gz" archive should have the final processed data.

## permissions
Add the "sticky bit" special permission on "/opt/appdata" directory (keep the other permissions as it is).
```bash
chmod +t /opt/appdata
ls -lsd /opt/appdata
```
Make "bob" the "user" and the "group" owner of "/opt/appdata.tar.gz" file.
```bash
chown bob:bob /opt/appdata.tar.gz
```
The "user/group" owner should have "read only" permissions on "/opt/appdata.tar.gz" file and "others" should not have any permissions.
```bash
**chmod 440 /opt/appdata.tar.gz**
```
## softlink
Create a "softlink" called "/home/bob/appdata.tar.gz" of "/opt/appdata.tar.gz" file.

```bash
ln -s /opt/appdata.tar.gz /home/bob/appdata.tar.gz
```

## filtered.txt
The script should filter the lines from "/opt/appdata.tar.gz" file which contain the word "processed", and save the filtered output in "/home/bob/filtered.txt" file. It must "overwrite" the existing contents of "/home/bob/filtered.txt" file
```bash
cat <<'EOF' > /home/bob/filter.sh
#!/bin/bash

tar -xzOf /opt/appdata.tar.gz | grep processed > /home/bob/filtered.txt
EOF
```