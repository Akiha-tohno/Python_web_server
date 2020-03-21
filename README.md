# Python_web_server
Basic web message board and video server using sockets in python
## socket_http_server.py

* Default server address: localhost:3000
* Route:
    * / : Homepage
    * /login : Login page
    * /register : Register page
    * /sdqe : Show an image
    * /i19 : Show an image
    * /all : Show an image
    * /message : Message board
    * /hello : Helloworld test
* The contents of the message board were saved in memory.
* Username and password were saved in user.txt file in json format.
* Custom 404 error page were shown when route is not satisfied