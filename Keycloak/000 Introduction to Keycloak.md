# Introduction to Keycloak

## Content
* Identity and access management
* What is keycloak?
* Keycloak features

## Identity and access management
* Management of users and their privileges for accessing a system
* Perform authentication and authorization
* Many systems depend on an IAM system

# What is Identity and Access Management (IAM)?

Before learning Keycloak, you first need to understand the problem it solves.

Imagine your company has the following applications:

- GitLab
- Jenkins
- Zabbix
- Grafana
- Oracle APEX
- Jira
- Confluence
- Webmail
- Internal HR Portal
- Finacle CBS

Without IAM, every application maintains its own users.

```scss
GitLab
---------
deepak
password123

Jenkins
---------
deepak
admin123

Grafana
---------
deepak
welcome123

Oracle
---------
deepak
oracle123
```

Problems:

- Multiple usernames/passwords
- Users forget passwords
- Password reuse
- Difficult administration
- Difficult employee onboarding/offboarding
- Security risks

Suppose an employee leaves the company.

The administrator now has to:

- Delete GitLab account
- Delete Jenkins account
- Delete Grafana account
- Delete Oracle account
- Delete HR account
- Delete VPN account

If one account is forgotten...

→ Security risk.

---

# What is IAM?

Identity and Access Management (IAM) is a centralized system responsible for managing:

- Users (Identity)
- Authentication (Who are you?)
- Authorization (What can you access?)
- Roles
- Groups
- Permissions
- Login sessions
- Password policies
- MFA
- Federation

Instead of every application managing users independently, all applications trust one IAM server.

```scss
               IAM
            (Keycloak)

              |
      -------------------
      |    |     |      |
   GitLab Jira Grafana Jenkins
```

One user database.

One login.

Centralized control.

---

# Identity

Identity simply means

> "Who is the user?"

Example

```scss
Name:
Deepak Nagarkoti

Username:
deepak

Email:
deepak@example.com

Employee ID:
EMP-001
```

An identity contains information about a person.

Sometimes called:

- Principal
- Subject
- User Identity

---

# Authentication

Authentication answers:

> Are you really who you claim to be?

Examples

Username + Password

```scss
Username:
deepak

Password:
*******
```

Fingerprint
Face ID
OTP
Smart Card
YubiKey
Certificate
MFA
Authentication proves identity.


# Authorization
Authentication answers:
Who are you?

Authorization answers:
What are you allowed to do?

Example
Administrator can:
✓ Create Users
✓ Delete Users
✓ Restart Servers

Developer
```
✓ Push Code
✓ Read Logs
✗ Delete Production
```

Auditor
```
✓ View Reports
✗ Modify Data
```

Authorization comes after authentication.

---

# Authentication vs Authorization

|Authentication|Authorization|
|---|---|
|Who are you?|What can you do?|
|Verify identity|Verify permissions|
|Happens first|Happens second|
|Login|Access Control|

Example

```
Login
↓
Authenticated
↓
Check Role
↓
Authorized
↓
Access Granted
```

---

# Access Control

Suppose your organization has

```scss
CEO
IT Manager
Developer
Network Engineer
Security Engineer
HR
```

Each person should only access required systems.

Example:
Developer
```scss
GitLab
Jenkins
Allowed

Oracle Production
Denied
```

HR
```scss
Payroll
Allowed

GitLab
Denied
```
IAM manages this.

# Why Organizations Need IAM
Without IAM

```scss
100 Applications
100 User Databases
100 Password Policies
100 Admin Panels
```

Huge maintenance.

With IAM

```scss
100 Applications
↓
Keycloak
↓
One Identity
```

Simple.

---

# Enterprise Example

Suppose ABC Bank has

- Finacle
- Internet Banking
- CRM
- HRMS
- Email
- Oracle Database
- GitLab
- Jenkins

Every employee logs in using the same credentials.

```scss
Employee
↓
Keycloak
↓
Token
↓
Access Applications
```

Employee never enters passwords repeatedly.


---
## What is keycloak?
* An open source identity and access management system for modern applications and services
* Apache License 2.0
* Jboss community project
* Initial release in 2014
* It acts as the trusted identity provider (IdP) that applications rely on instead of implementing login functionality themselves.
* Official definition:
> An open-source Identity and Access Management solution for modern applications and services.
## Keycloak Features
* Single Sign On 
* Standard protocol support
	* OpenID connect, OAuth 2.0, SAML
* Identity Brokering and Social Login
* User Federation
* Client Adapters
* Extensible

# History

Keycloak

- Started by the JBoss community
- First released in **2014**
- Licensed under the **Apache License 2.0**, which allows both personal and commercial use
- Originally developed under the JBoss ecosystem and later became part of the Red Hat ecosystem

Today it is widely used in:

- Enterprises
- Banks
- Government organizations
- Universities
- Cloud-native platforms
- Kubernetes/OpenShift environments

# Where Keycloak Fits

```scss
               Users
                  |
              Login Page
                  |
             KEYCLOAK
                  |
            Authentication
                  |
        Generates Token
                  |
------------------------------------
|          |         |             |
GitLab   Jenkins   Grafana     HRMS
```

Applications never validate passwords themselves.
Keycloak does.

# Keycloak Components

```scss
Users
↓
Keycloak
↓
Database
↓
Applications
```

Keycloak stores:

- Users
- Passwords
- Roles
- Groups
- Clients
- Sessions
- Tokens

---

# Keycloak Features

Let's understand each feature in detail.

---

# 1. Single Sign-On (SSO)
This is Keycloak's biggest feature.
Without SSO

```scss
Open GitLab
Login
↓
Open Grafana
Login Again
↓
Open Jenkins
Login Again
↓
Open Jira
Login Again
```

Very frustrating.

With SSO

```scss
Login Once
↓
Keycloak
↓
GitLab
↓
Grafana
↓
Jenkins
↓
Jira
↓
Already Logged In
```

Only one login.

## Real Flow
```scss
User
↓
GitLab
↓
Not Logged In
↓
Redirect
↓
Keycloak
↓
Enter Password
↓
Authenticated
↓
Token
↓
Back to GitLab
↓
Success
```

Later
```scss
Open Grafana
↓
Redirect
↓
Keycloak
↓
Already Logged In
↓
Token
↓
Grafana Opens
```

No password.

# 2. Standard Protocol Support
Different applications speak different authentication "languages."
Keycloak supports all major identity standards.

## OpenID Connect (OIDC)
Modern protocol.
Built on OAuth 2.0.
Uses JSON Web Tokens (JWT).
Most modern applications use this.
Example:
- React
- Angular
- Spring Boot
- Node.js
- Mobile Apps
- Kubernetes Dashboard

---

## OAuth 2.0
OAuth 2.0 is primarily an **authorization framework**, not an authentication protocol.

It allows one application to access another application's resources on behalf of a user without exposing the user's password.

Example:
```scss
Login using Google
↓
Google asks

Allow access?
↓
Yes
↓
Application receives Access Token
```

---

## OpenID Connect (OIDC)

OIDC extends OAuth 2.0 by adding an identity layer. It enables applications to verify who the user is and obtain profile information.

```scss
OAuth
↓
Authorization

OIDC
↓
Authentication + Authorization
```

---

## SAML
Older XML-based enterprise protocol.

Still common in large organizations.

Used by:

- Banks
- Government
- Legacy Enterprise Software

Example

```scss
SAP
Oracle
Old HRMS
Active Directory Federation
```

Keycloak can act as a SAML Identity Provider.

---

# 3. Identity Brokering
One login system trusting another login system.

Example
```scss
User
↓
Login with Microsoft
↓
Keycloak
↓
Application
```

Keycloak does not verify the password itself.

Microsoft does.

Keycloak trusts Microsoft.


## Identity Broker Example
```scss
Google
↓
Keycloak
↓
GitLab
```

or
```scss
Azure AD
↓
Keycloak
↓
Jenkins
```

Keycloak becomes the middleman.

# 4. Social Login

Users can log in using external providers.

Examples
- Google
- GitHub
- Microsoft
- Facebook
- LinkedIn

Flow
```scss
Application
↓
Keycloak
↓
Google
↓
Authentication
↓
Keycloak
↓
Application
```

Useful for public-facing websites and developer portals.

# 5. User Federation
One of the most important enterprise features.

Suppose your company already has
- Microsoft Active Directory
- LDAP

You don't want to recreate every user.

Keycloak can connect directly to those directories.
```scss
Active Directory
↓
Keycloak
↓
Applications
```

Employees continue using their existing credentials.

Supported sources include:
- LDAP
- Microsoft Active Directory
- Other LDAP-compliant directories

---

# 6. Client Adapters

Applications communicate with Keycloak through client libraries (or by using standard protocols directly).

Historically, Keycloak provided adapters for platforms such as:

- Java EE
- Spring
- Tomcat
- WildFly

Many modern applications now use standard OpenID Connect or SAML libraries instead of Keycloak-specific adapters, making integrations more portable.

---

# 7. Extensible

Organizations have unique requirements.

Keycloak can be customized by developing extensions.

Examples:

Custom authentication

```scss
Password
↓
OTP
↓
Smart Card
↓
Biometric
↓
Login
```

Custom User Storage

```scss
Database
↓
Keycloak
↓
Authentication
```

Custom Event Listener

```scss
User Login
↓
Send Email
↓
Write Log
↓
SIEM
```

Custom Themes

```scss
Default Login
↓
Company Branding
↓
Bank Logo
↓
Custom CSS
```

---

# Real Enterprise Architecture

```scss
                    Employees

                         |

                    Browser

                         |

                    Keycloak

        -------------------------------
        |             |               |
     LDAP/AD      Local Users      Social Login
        |
        |
   Authentication

        |

JWT / SAML Assertion / OIDC Token

        |

--------------------------------------------------------
|          |          |          |         |            |
GitLab   Jenkins   Grafana   Jira   Oracle APEX   Internal Apps
```

---

# Why Keycloak is Popular

- Completely open source
- No licensing costs
- Enterprise-ready
- Supports OIDC, OAuth 2.0, and SAML
- Centralized user management
- Single Sign-On (SSO)
- Multi-Factor Authentication (MFA)
- Identity federation with LDAP/Active Directory
- Highly extensible
- Active community and backed by Red Hat

---