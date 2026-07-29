Day 11: Install and Configure Tomcat Server



```
cat /etc/os-release
```


```
sudo yum update -y

java -version
sudo yum install java-17-openjdk -y # For CentOS/RHEL
java -version


sudo mkdir -p /opt/tomcat
sudo chown -R <app-server-user>:<app-server-user> /opt/tomcat  
ls -la

sudo wget https://archive.apache.org/dist/tomcat/tomcat-9/v9.0.80/bin/apache-tomcat-9.0.80.tar.gz

sudo tar -xf apache-tomcat-9.0.80.tar.gz  
sudo mv apache-tomcat-9.0.80 tomcat

sudo /opt/tomcat/tomcat/bin/startup.sh

scp /tmp/ROOT.war <app-server-user>@<app-server-name>:/opt/tomcat/tomcat/webapps/


curl http://stapp01:8085


sudo /opt/tomcat/tomcat/bin/shutdown.sh


curl http://stapp01:8085
```