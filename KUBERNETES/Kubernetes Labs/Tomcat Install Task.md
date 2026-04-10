# ✅ **Task Summary**

You must:

1. Install Tomcat on **App Server 1**
    
2. Change Tomcat default port → **8085**
    
3. Copy `ROOT.war` from Jump Host → App Server 1
    
4. Deploy ROOT.war so the app loads directly at:
    
    `curl http://stapp01:8085`
    

Let’s do this.

---

# 🚀 **1. SSH into App Server 1**

From Jump Host:

`ssh tony@stapp01`

(If password is needed, use what the task provides.)

---

# 🎯 **2. Install Tomcat (CentOS-based)**

On **stapp01**:

`sudo yum install tomcat tomcat-webapps tomcat-admin-webapps -y`

Enable & start:

`sudo systemctl enable tomcat sudo systemctl start tomcat`

---

# 🔧 **3. Change Tomcat port to 8085**

Edit **server.xml**:

`sudo vi /etc/tomcat/server.xml`

Find this line:

`<Connector port="8080" protocol="HTTP/1.1"`

Change 8080 → **8085**:

`<Connector port="8085" protocol="HTTP/1.1"`

Save and restart Tomcat:

`sudo systemctl restart tomcat`

Check it’s running:

`sudo systemctl status tomcat`

---

# 🗃️ **4. Copy ROOT.war from Jump Host → App Server 1**

On **Jump Host**, run:

`scp /tmp/ROOT.war tony@stapp01:/tmp/`

Then SSH back to App Server 1:

`ssh tony@stapp01`

---

# 📦 **5. Deploy ROOT.war to Tomcat**

Tomcat webapps folder:

`/usr/share/tomcat/webapps/`

So move the file:

`sudo cp /tmp/ROOT.war /usr/share/tomcat/webapps/`

Make sure correct ownership:

`sudo chown tomcat:tomcat /usr/share/tomcat/webapps/ROOT.war`

Restart Tomcat so it extracts the WAR:

`sudo systemctl restart tomcat`

---

# 🧪 **6. Test the application**

On **App Server 1**:

`curl http://stapp01:8085`

On Jump Host you can test:

`curl http://stapp01:8085`

You should see your application content.

---

# 🎉 **DONE**

You have completed:

✔ Installed Tomcat  
✔ Changed port to **8085**  
✔ Copied & deployed `ROOT.war`  
✔ Application loads at base URL (no /ROOT needed)