# **Insecure Design**

### **Insecure Design:**

1. **Understanding Secure Design Principles**:
    - **Defense in Depth**: Layering security mechanisms to ensure no single point of failure.
    - **Least Privilege**: Granting only the minimum necessary access or permissions.
    - **Fail Securely**: Systems should default to a secure state during failures.
    - **Economy of Mechanism**: Keeping designs simple to reduce potential vulnerabilities.
    - **Complete Mediation**: Every access request should be checked against security rules.
    - **Open Design**: Security should not rely on obscurity; mechanisms should be open and tested.
    - **Separation of Duties**: Split responsibilities so no single entity has full control.
    - **Least Common Mechanism**: Minimize shared resources to reduce potential attack vectors.
    - **Psychological Acceptability**: Security mechanisms should not make the resource harder for legitimate users to access.
2. **Identifying Design Flaws**:
    - **Lack of Input Validation**: Trusting all user inputs without validation.
    - **Improper Error Handling**: Revealing too much information in error messages.
    - **Misconfigured Security Headers**: Not setting or improperly setting HTTP security headers.
    - **Lack of Multi-factor Authentication**: Relying solely on passwords for authentication.
    - **Inadequate Session Management**: Not properly handling user sessions, making them vulnerable to hijacking.
    - **Insecure Data Storage**: Storing sensitive data without proper encryption or in easily accessible locations.
    - **Insecure Communication**: Not encrypting data in transit.
    - **Lack of Logging and Monitoring**: Not tracking or alerting on suspicious activities.
    - **Hardcoded Secrets**: Embedding secrets like API keys directly in the code.
    - **Using Outdated or Vulnerable Components**: Not updating libraries or using components with known vulnerabilities.

Checklist

### **Vulnerability Checklist: Insecure Design & Design Flaws:**

### 1. **General Design Principles**:

- [ ]  **Defense in Depth**: Check if multiple layers of security controls are in place.
- [ ]  **Principle of Least Privilege**: Ensure every module, process, or user operates with the minimum set of privileges.
- [ ]  **Fail Securely**: Systems should handle failures without exposing sensitive information or insecure states.
- [ ]  **Economy of Mechanism**: Verify that the design is simple and doesn't have unnecessary complexities.
- [ ]  **Complete Mediation**: Ensure every access request is checked for authorization.
- [ ]  **Open Design**: Confirm that security doesn't rely on obscurity.
- [ ]  **Separation of Duties**: Check if responsibilities are divided, preventing a single point of compromise.
- [ ]  **Least Common Mechanism**: Ensure minimal sharing of resources among users or processes.
- [ ]  **Psychological Acceptability**: Verify that security mechanisms are user-friendly.

### 2. **Design Flaws**:

- [ ]  **Lack of Input Validation**: Ensure all inputs are validated and sanitized before processing.
- [ ]  **Improper Error Handling**: Check if errors reveal sensitive information or system details.
- [ ]  **Inadequate Session Management**: Ensure sessions are securely managed, timed out, and invalidated.
- [ ]  **Insecure Data Storage**: Confirm sensitive data is encrypted and stored securely.
- [ ]  **Insecure Default Configurations**: Ensure systems are not using default settings that might be insecure.
- [ ]  **Lack of Encryption**: Verify that data at rest and in transit is encrypted.
- [ ]  **Inadequate Logging and Monitoring**: Ensure all critical operations are logged, and there's a mechanism for real-time monitoring and alerting.
- [ ]  **Hardcoded Secrets**: Check the system for hardcoded credentials or API keys.
- [ ]  **Using Outdated Components**: Ensure all software components, libraries, and plugins are up-to-date and patched.
- [ ]  **Lack of Multi-factor Authentication**: Confirm critical operations or access requires more than one method of authentication.
- [ ]  **Misconfigured Security Headers**: Ensure HTTP headers are set correctly to prevent attacks like clickjacking.
- [ ]  **Lack of Rate Limiting**: Check if systems are vulnerable to brute force or DDoS attacks due to missing rate limits.
- [ ]  **Unrestricted API Access**: Ensure APIs have proper authentication and authorization mechanisms.
- [ ]  **Lack of Data Validation for APIs**: Confirm that data sent to APIs is validated and sanitized.








- [ ]  **Insecure Third-party Integrations**: Verify that third-party services integrated into the system are secure and don't introduce vulnerabilities.