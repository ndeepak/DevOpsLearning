### File Capabilities in Linux
File capabilities provide a fine-grained privilege management mechanism, allowing specific capabilities to be granted to executables without requiring full root privileges. These capabilities divide the root’s all-encompassing power into smaller, discrete privileges, ensuring better security control over processes.

Instead of using **SetUID** (which grants complete root-level access), file capabilities allow processes to only have the specific privileges they need, minimizing the risk of privilege escalation vulnerabilities.

#### 1. **Understanding Linux Capabilities**
Linux capabilities are individual privileges that can be given to executables. They are defined in the `man 7 capabilities` page and include things like:

- `CAP_NET_BIND_SERVICE`: Allow binding to low-numbered (privileged) ports.
- `CAP_SYS_TIME`: Allow setting the system clock.
- `CAP_DAC_OVERRIDE`: Bypass file read, write, and execute permission checks.

These are just a few examples, and the kernel includes many more capabilities that can be assigned.

#### 2. **Checking File Capabilities**
To check the capabilities of a file, use the `getcap` command:
`$ getcap /path/to/file`

For example, checking the capabilities of the `ping` command:
```
$ getcap /bin/ping
/bin/ping = cap_net_raw+ep
```
This shows that `ping` has been granted the `cap_net_raw` capability, allowing it to send and receive raw network packets, even though it's not running as root.

#### 3. **Setting File Capabilities**
You can set file capabilities using the `setcap` command. The syntax is as follows:
`$ sudo setcap <capability>=<flag> /path/to/file`

- **Capability**: The specific capability you want to grant (like `cap_net_bind_service`).
- **Flags**:
    - `e`: Effective — the capability is enabled for the running process.
    - `p`: Permitted — the capability can be used by the process.
    - `i`: Inherited — the capability can be passed through to child processes.

For example, to allow a program to bind to low-numbered ports (which normally require root privileges):
`$ sudo setcap cap_net_bind_service=+ep /path/to/program`

You can also add multiple capabilities at once:
`$ sudo setcap cap_net_bind_service,cap_sys_time=+ep /path/to/program`

#### 4. **Removing File Capabilities**
To remove specific capabilities from a file, use `setcap` with the `-` operator:
`$ sudo setcap cap_net_bind_service=-ep /path/to/program`

To remove **all capabilities** from a file:
`$ sudo setcap -r /path/to/program`

#### 5. **Listing All Available Capabilities**
To view all available Linux capabilities, you can refer to the `man` page:
`$ man 7 capabilities`

Some commonly used capabilities include:
- **CAP_CHOWN**: Change file owner.
- **CAP_DAC_OVERRIDE**: Ignore file permission checks.
- **CAP_FOWNER**: Bypass permission checks on operations that normally require the file owner.
- **CAP_NET_ADMIN**: Perform various network-related operations (like interface configuration).
- **CAP_SETUID**: Allow the changing of user IDs.

#### 6. **Practical Example: Granting Capabilities to a Program**
Let's consider a scenario where you want to allow a non-root user to bind to ports below 1024 (e.g., HTTP, HTTPS ports) using a custom web server program. Normally, only root can bind to these "privileged" ports. Using capabilities, you can allow the program to bind to low-numbered ports without running it as root.

1. Check the current capabilities of the program:
    `$ getcap /usr/local/bin/my-web-server`
    
2. Grant the `CAP_NET_BIND_SERVICE` capability:    
    `$ sudo setcap cap_net_bind_service=+ep /usr/local/bin/my-web-server`
    
3. Verify that the capability has been applied:
```
$ getcap /usr/local/bin/my-web-server
/usr/local/bin/my-web-server = cap_net_bind_service+ep
```
Now, the program can bind to ports below 1024 without needing root privileges.
#### 7. **Security Considerations**
- **Advantages**:
    - File capabilities provide more granular control over the privileges of executables, avoiding the security risks associated with SetUID programs.
    - They reduce the attack surface, as processes don’t need full root privileges.
- **Risks**:
    - Improperly assigning capabilities can lead to unintended privilege escalation. For example, if a program with vulnerabilities is granted too many capabilities, it can be exploited by attackers to gain unauthorized access.
- **Best Practices**:
    - Only assign the capabilities that are absolutely necessary.
    - Regularly audit files with capabilities to ensure that no unnecessary privileges are assigned.

#### 8. **Common Capabilities and Their Usage**

| Capability             | Purpose                                          | Example Use Case                                   |
| ---------------------- | ------------------------------------------------ | -------------------------------------------------- |
| `CAP_NET_BIND_SERVICE` | Bind to ports below 1024                         | Running a web server on port 80 as a non-root user |
| `CAP_SYS_TIME`         | Change the system clock                          | Programs that need to adjust the system time       |
| `CAP_NET_ADMIN`        | Perform network-related administration tasks     | Programs managing network interfaces and routes    |
| `CAP_DAC_OVERRIDE`     | Bypass file read, write, and execute permissions | Backup programs that need to read all files        |
| `CAP_SETUID`           | Change user ID (without full root privileges)    | Programs that require dynamic user ID switching    |
| `CAP_CHOWN`            | Change file ownership                            | System utilities that manage file ownership        |

#### 9. **Conclusion**
File capabilities in Linux offer a secure and flexible way to manage privileges for executables. By assigning only the necessary capabilities to a program, you can avoid the risks associated with giving full root access, while still allowing the program to perform privileged actions. Use tools like `getcap` and `setcap` to manage and audit these capabilities, ensuring a secure operating environm