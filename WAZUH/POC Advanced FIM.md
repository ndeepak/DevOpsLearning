Red Hat-basedDebian-based
`yum install audit`
For Audit 3.1.1 and later, install the audispd af_unix plugin and restart the Audit service.
```
yum install audispd-plugins
systemctl restart auditd
```
Debian-based
`apt-get install auditd`
For Audit 3.1.1 and later, install the audispd af_unix plugin and restart the Audit service.
```
apt-get install audispd-plugins
systemctl restart auditd
```


In most systems, auditd includes a rule to skip processing of every audit rule by default. This setting prevents the reporting of any whodata-related information. To ensure that auditd is not [DISABLED BY DEFAULT](https://man7.org/linux/man-pages/man8/auditctl.8.html#DISABLED_BY_DEFAULT), follow these steps.
1. Check the output of this command to find out if the auditd rules include the `-a never,task` rule.
	`auditctl -l | grep task
2. If the output displays the `-a never,task` rule, remove it from the audit rules file located at `/etc/audit/rules.d/audit.rules`.
3. After that, restart auditd and Wazuh agent to apply the changes:
    `systemctl restart auditd
    `systemctl restart wazuh-agent


Configure who-data monitoring for the `/etc/` directory.
1. Edit the Wazuh agent `/var/ossec/etc/ossec.conf` configuration file and add the configuration below:   
```
	<syscheck>
       <directories check_all="yes" whodata="yes">/etc</directories>
    </syscheck>
```    
2. Once you add this configuration, restart the Wazuh agent to apply the changes. This will add an audit rule for the monitored directory:
	`systemctl restart wazuh-agent
3. Execute the following command to check if the audit rule for monitoring the selected directory is applied:    
    `auditctl -l | grep wazuh_fim
    From the output, you can see the rule was added:
    Output    
    `auditctl -w /etc -p wa -k wazuh_fim


More on this:
https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/advanced-settings.html#who-data-monitoring-linux

