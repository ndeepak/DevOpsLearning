### Curl Commands That You Should Know
**Introduction:**
- **cURL** stands for _Client URL_, a software tool providing both a command-line tool and a library (libcurl).
- It supports multiple protocols such as HTTP, HTTPS, FTP, IMAP, LDAP, and many more.
- It's mainly used to transfer data from or to a server, making it essential for automation, testing, or data transfers without user interaction.
- Common use cases include testing API outputs, working in a terminal environment, or automating file downloads/uploads.

---
### Common `curl` Commands & Options
1. **Requesting a Web Page**: Fetch the HTML content of a web page:
    `curl www.google.com`
    
    - This sends a GET request to the server and prints the page content in the terminal.
2. **Downloading a File**:
    
    - Save the file with the original filename:      
        `curl -O https://testdomain.com/testfile.tar.gz`
        
    - Save the file with a custom name:
        `curl -o custom_file.tar.gz https://testdomain.com/testfile.tar.gz`
        
    - Download multiple files:
        `curl -O https://testdomain.com/file1.tar.gz -O https://testdomain.com/file2.tar.gz`
        
3. **Get HTTP Headers**: Fetch just the headers of a document:
    `curl -I https://www.google.com`
    
    Example output:
```
HTTP/1.1 200 OK
Content-Type: text/html
Date: Thu, 04 Jun 2020
Server: gws
```
    
4. **Ignore Invalid or Self-Signed Certificates**: To bypass SSL certificate verification for testing purposes:
    `curl -k https://localhost/endpointtest`
    
5. **Make a POST Request**:
    - Send form data to an endpoint:
        `curl --data "param1=test1¶m2=test2" http://website.com`
        
    - Send JSON data:
        `curl -H 'Content-Type: application/json' --data '{"param1":"test1","param2":"test2"}' http://www.website.com`
        
6. **Specify the HTTP Method**: To change the request type (e.g., PUT or DELETE):
    `curl -X PUT -d '{"param1":"value1","param2":"value2"}' http://website.com/resource_id`
    
7. **Basic Authentication**: Access protected resources using username and password:
    `curl -u username:password https://my-test-api.com/endpoint1`
    
8. **Update DNS Resolution**: Test a domain name before deploying it by manually setting up DNS resolution:
    `curl --resolve www.test.com:80:localhost http://www.test.com/`
    
9. **Upload a File**: Upload a file with a form-like submission:
    `curl -F field_name=@/path/to/local_file http://test.com/upload`
    
    Upload multiple files:
    `curl -F field_name=@/path/to/file1 -F field_name=@/path/to/file2 http://test.com/upload`
    
10. **Measure Request Time**: Display the total time taken for a curl request to complete:
    `curl -w "%{time_total}\n" -o /dev/null -s www.test.com`
    

### Additional Comprehensive `curl` Commands

11. **Follow Redirects**: To automatically follow HTTP redirects:
`curl -L http://example.com`

12. **Set Request Headers**: To send custom headers with your request:
`curl -H "Authorization: Bearer YOUR_TOKEN" -H "Accept: application/json" https://api.example.com/resource`

13. **Limit Rate of Data Transfer**: To limit the download/upload speed:
`curl --limit-rate 100K https://example.com/largefile.zip`

14. **Use a Proxy Server**: To route your request through a proxy:
`curl -x http://proxyserver:port http://example.com`

15. **Use Cookies**: To send cookies with your request:
`curl -b "name=value" http://example.com`

To save cookies to a file:
`curl -c cookies.txt http://example.com`

16. **Download a File with Resume Support**: To resume an interrupted download:
`curl -O -C - https://example.com/largefile.zip`

17. **Show Progress Meter**: To get a progress meter while downloading:
`curl -# -O https://example.com/largefile.zip`

18. **Post Data from a File**: To send data contained in a file:
`curl --data @data.txt http://test.com`

19. **Send PUT Requests with Data from a File**: To send a PUT request with data from a file:
`curl -X PUT -d @data.json http://test.com/resource_id`

20. **Save Output to a File**: To save the output to a specified file instead of standard output:
`curl -o output.txt https://example.com`

21. **Use Verbose Mode**: To get detailed information about the request and response:
`curl -v http://example.com`

22. **Use Silent Mode**: To run curl in silent mode (suppress progress and error messages):
`curl -s http://example.com`

23. **Check HTTP Response Code**: To retrieve the HTTP status code:
`curl -o /dev/null -w "%{http_code}" -s http://example.com`

24. **Upload Files via FTP**: To upload files to an FTP server:
`curl -T localfile.txt ftp://ftp.example.com/ --user username:password`

25. **Execute Multiple Commands**: To run multiple `curl` commands in a single line:
`curl -O https://example.com/file1.zip && curl -O https://example.com/file2.zip`

26. **Download Files Using FTP with Passive Mode**: To use FTP in passive mode:
`curl -u username:password --ftp-pasv ftp://ftp.example.com/`

27. **Output Timing Information**: To get detailed timing information after the request:
`curl -w "@curl-format.txt" -o /dev/null -s https://example.com`

_(Create a `curl-format.txt` file with timing variables like `%{time_starttransfer}`.)_
28. **Set User-Agent**: To modify the User-Agent string sent in the request:
`curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" http://example.com`

29. **Use Multiple HTTP Methods**: For endpoints that accept both POST and GET methods:
```
curl -X POST -d '{"param1":"value1"}' http://test.com/resource
curl -X GET http://test.com/resource
```

30. **Download HTML Content and Save to a File**:
`curl -o webpage.html http://example.com`

### Conclusion:
These additional commands further enhance your ability to use `curl` effectively for various networking tasks, from downloading files to testing APIs and handling authentication. Whether you're automating tasks in scripts or troubleshooting network requests, mastering `curl` can be a powerful asset in your toolkit.