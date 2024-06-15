# AI_Anomaly_Detection

**Download "POSTMAN" app.**

https://www.postman.com/downloads/

After setting up the postman application.

**NOTE --- While doing operation in Postman the server flask app should be running.**

**This is for user Login -->**

Open Postman.

Create a new POST request.

Set the URL to http://127.0.0.1:5000/login.

Go to the "Body" tab, select "raw", and choose "JSON" from the dropdown menu.

{
    "username": "user1",
    "password": "pass123"
}

**This is for user Logout -->**

Create a new POST request in Postman.

Set the URL to http://127.0.0.1:5000/logout.

Go to the "Body" tab, select "raw", and choose "JSON" from the dropdown menu.

Enter the following JSON data:

{
    "username": "user1"
}

**This is for Monitoring -->**

Create a new GET request in Postman.

Set the URL to http://127.0.0.1:5000/monitor?username=user1.

Click "Send".

**Local server deployment.**

Run server.py

#NOTE --- While doing operation in Postman the server flask app should be running.

**server.py**

Contains a code for deploying local server.

Once the user logs in, this python code will collect network information like :- IP Address, MAC Address, Login date&time, Logout date&time, source byte sent, destination byte received.

These details will be stored in CSV file.

