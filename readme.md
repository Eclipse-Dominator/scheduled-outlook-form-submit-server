This project is an automated server service that submits outlook based surveys/forms on a regular basis.

Users will register their automated service via a POST request to the flask server and specify the timing to submit the survey. Tasks will then be generated for the users and upon the right timing, it will be automatically submitted.
Should there be any issues, the selenium will snap a screenshot of the error and forward it to the admin and user via telegram

As it was only meant for a tiny group of users and a private project, all the data are stored via pickle.

The task queue is handled using a Priority Queue and threading.Timer.

This is not a secure server and should only be hosted in a private/local network.
The content of the code has been modified for general usage although it may not be functional.

OutlookFormController -> handles selenium/browser control

OutlookUser -> handles user objects and management of users

interface -> contains global constant as well as values used for the survey

app -> contain the flask web app that handles api request to add/delete user

Queue -> contain class for the Priority Queue implementation



packages installed

certifi==2020.12.5
chardet==4.0.0  
click==7.1.2  
Flask==1.1.2  
idna==2.10
itsdangerous==1.1.0
Jinja2==2.11.3  
MarkupSafe==1.1.1  
requests==2.25.1  
selenium==3.141.0  
urllib3==1.26.4  
waitress==2.0.0  
Werkzeug==1.0.1
