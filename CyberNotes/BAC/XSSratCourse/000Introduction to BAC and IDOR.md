# Introduction to BAC and IDOR

## Agenda
* Syllabus
* How to get support
* Introduction to our labs
* Why BAC and IDOR
* API vs WEB
* 3 Types of BAC on API level
* 2 Types of BAC on WEB level
* Tools we are going to use
---
### How to get support
ser@thexssrat.atlassian.net
https://thexssrat.atlassian.net/servicedesk/customer/portal/4,

---
### Introduction to our labs

https://labs.hackxpert.com
---

### Why BAC and IDOR
* 3 times in OWASP top 10 API
* twice in OWASP web 10
* One of most found bounties
* Often overlooked and very difficult to automate
* The developers need to be right 100% of the time, for use only one time can be enough
* This is pretty consistent money
* A lot of other hackers suck at testing for this exploit
* But not us after this course
---

### API vs WEB
* BAC on Web
	* Browser takes care of authentication
	* 2 types
	* Semi automate-able
	* easier to find initially ~ less lot for us
* BAC on API
	* We have to take care of auth handling
	* 3 types
	* Also semi-automate-able
	* Still easy to find but auth is harder

---

### 3 Types of BAC on API level
* API's are application programming interfaces
	* Access control is put on functions
		* makeUser()
		* openFile()
	* Can be on objects
		* editInvoice(11)
		* delete.php?user=123
	* Property level
		* editUser?id=1234&type=admin
	* Or a combination of the above 

---

### 2 Types of BAC on WEB level
* Function level
	* rideCoaster()
	* eatCheese()
* Object level
	* IDORq
---

### Tools we are going to use
* Burpsuite
* ZAP
* Chrome developer tools
* Firefox developer tools
* Autorize
* Auth Matrix
* ChatGPT
* More...

---

