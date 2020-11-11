# laba4

#create and activate virtualenv throuth scripts/activate.bat

#install python and packages versions from requirements.txt(run pip install -r /path/to/requirements.txt)

#add solve.wsgi to solve.conf in your Apache/conf
example for .conf:

	<VirtualHost *:80>
    	ServerName localhost:80
    	WSGIScriptAlias / "C:\Users\andrii.riabchuk\Documents\GitHub\laba4\solve.wsgi"
     	DocumentRoot "C:\Users\andrii.riabchuk\Documents\GitHub\laba4"
    	<Directory "C:\Users\andrii.riabchuk\Documents\GitHub\laba4">
        	Require all granted
    	</Directory>
	</VirtualHost>

#include solve.conf in httpd.conf
Example: # Include Flask file
	Include conf/solve.conf

#run httpd.exe