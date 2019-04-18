# parking_Lot_Management_System
Environment
Our system is developed by Django framework, the requirement of environment is listed as below.
Python 3.5.1
Django 2.1.7
The required python libraries are:
hashlib
dicttoxml
urllib
urllib3
nexmo
mailjet_rest

How to run the server?
Once the libraries are installed, we can go into the directory of the project, then type "python3 manage.py runserver" in the terminal
to run the server.The server host and port will be shown in the terminal. After running, we can visit the web page in the browser.
The portal for drivers are "http://host:port/park/" one of the usernames and passwords is: 5823447919/5823447919 (username and password are the same)
The portal for managers are "http://host:port/park/admin" one of the usernames and passwords is: 2974556594/2974556594 (username and password are the same)
The portal for APIs are "http://host:port/park/api"



Structure
Final/
├── parkManagement/     main part of the system.
│   ├── templates/
│   │   └── parkSrc/      The static html pages and javascript files are stored here
│   ├── models.py       maintain the models
│   ├── urls.py        handle the url mapping
│   ├── views.py       main logical part, handle the request and return response
│   └── admin.py
├── utils/               There are some tools files
│   ├── dijkstra.py      To generate the graph and find the shortest path
│   ├── EmailService.py   To send email
│   └── ......
├── db.sqlite3         database
└── manage.py      main manage file
