# File integrity monitoring
### Ubuntu
```
<directories check_all="yes" report_changes="yes" realtime="yes">C:\Users\<USER_NAME>\Desktop</directories>
```

```
sudo systemctl restart wazuh-agent
```

### Windows endpoint[Permalink to this headline](https://documentation.wazuh.com/current/proof-of-concept-guide/poc-file-integrity-monitoring.html#windows-endpoint "Permalink to this headline")

Take the following steps to configure the Wazuh agent to monitor filesystem changes in the `C:\Users\Administrator\Desktop` directory.
1. Edit the `C:\Program Files (x86)\ossec-agent\ossec.conf` configuration file on the monitored Windows endpoint. Add the directories for monitoring within the `<syscheck>` block. For this use case, you configure Wazuh to monitor the `C:\Users\Administrator\Desktop` directory. To get additional information about the user and process that made the changes, enable [who-data audit](https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/advanced-settings.html#who-data-monitoring-windows):
```
<directories check_all="yes" report_changes="yes" realtime="yes">C:\Users\<USER_NAME>\Desktop</directories>
```

```
Restart-Service -Name wazuh
```
## Test the configuration
1. Create a text file in the monitored directory then wait for 5 seconds.
2. Add content to the text file and save it. Wait for 5 seconds.
3. Delete the text file from the monitored directory.
## Visualize the alerts
Ubuntu - `rule.id: is one of 550,553,554`
Windows - `rule.id: is one of 550,553,554
[[POC Advanced FIM]]