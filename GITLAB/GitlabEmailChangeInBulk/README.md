# Changing Bulk Emails in Self Hosted Gitlab Instance

In Linux,
```bash
python -m venv venv
source venv/bin/activate
export GITLAB_URL="https://gitlab.yourcompany.com"
export TOKEN="YOUR_ADMIN_ACCESS_TOKEN"
```


In Windows,
```powershell
python -m venv venv
venv\Scripts\activate.bat
.\venv\Scripts\Activate.ps1
$env:GITLAB_URL="https://gitlab.yourcompany.com"
$env:GITLAB_TOKEN="YOUR_ADMIN_TOKEN"
```

---
Folder Structure
```scss
gitlab_email/
│
├── extract_gitlab_users.py
├── update_gitlab_emails.py
│
├── all_gitlab_users.csv
├── users_to_update.csv
└── email_migration_log.csv
```


### Extracting all users and users to update the emails
`python3 extract_gitlab_users.py`
Gives:
* all_gitlab_users.csv
* users_to_update.csv

### Review the users
`users_to_update.csv`

### changes made to new_email in the same files as required

### Dry Run
`python3 update_gitlab_emails.py --dry-run` 

It just outputs what it will do.


## !!! Warning !!!
### Execute the script
`python3 update_gitlab_emails.py --execute`


### Audit the log in the file:
`email_migration_log.csv`

---