### Step-by-Step Instructions to Install Java SE JDK 22 on Ubuntu

### Step 1: Download JDK 22 from Oracle

1. **Visit the Oracle JDK Downloads Page** Go to the [Oracle JDK Downloads](https://www.oracle.com/java/technologies/javase-jdk22-downloads.html) page and download the appropriate package for your system (e.g., `jdk-22_linux-x64_bin.tar.gz` for 64-bit systems).
    
2. **Download the JDK Package** You can use the browser to download the package or use `wget` from the terminal. Here is an example using `wget`:
        `wget https://download.oracle.com/java/22/latest/jdk-22_linux-x64_bin.tar.gz`
        
### Step 2: Extract the JDK Package
1. **Extract the Tarball** Navigate to the directory where the tarball was downloaded (usually `~/Downloads`):
    `cd ~/Downloads`
    Extract the tarball:
    `tar -xvf jdk-22_linux-x64_bin.tar.gz`
    
2. **Move the Extracted JDK to `/opt`** Move the extracted JDK directory to `/opt`:    
    `sudo mv jdk-22 /opt/`
    
### Step 3: Set Up the Java Environment
1. **Update Alternatives** Configure your system to use the newly installed JDK:
    `sudo update-alternatives --install /usr/bin/java java /opt/jdk-22/bin/java 1 sudo update-alternatives --install /usr/bin/javac javac /opt/jdk-22/bin/javac 1`
    
2. **Select the New Java Version** If you have multiple versions of Java installed, you can select JDK 22 as the default:    
```
sudo update-alternatives --config java
sudo update-alternatives --config javac
```
    
    Follow the prompts to select the JDK 22 path (`/opt/jdk-22/bin/java` and `/opt/jdk-22/bin/javac`).
    
### Step 4: Set Environment Variables
1. **Edit the Profile File** Open the `/etc/profile` file in a text editor:
    `sudo nano /etc/profile`
    
2. **Add the Following Environment Variables** Add the following lines to the end of the file:
```
export JAVA_HOME=/opt/jdk-22
export PATH=$JAVA_HOME/bin:$PATH
```
    
3. **Apply the Changes** Save the file and reload the profile:
    `source /etc/profile`

### Step 5: Verify the Installation
1. **Check the Java Version** Verify that JDK 22 is installed and set up correctly by checking the Java version:
    `java -version`
    
    You should see output similar to:
```
java version "22"
Java(TM) SE Runtime Environment (build 22)
Java HotSpot(TM) 64-Bit Server VM (build 22, mixed mode)
```
    ![[Pasted image 20240722112704.png]]
2. **Check the Javac Version** Also, check the `javac` version:
    `javac -version`
    
    You should see:
    `javac 22`
### Conclusion
By following these steps, you can successfully install Java SE JDK 22 on your Ubuntu system. This guide covers downloading the JDK package from Oracle, extracting it, configuring your system to use the new JDK, and verifying the installation. This ensures you have the latest Java Development Kit set up for your development needs.