# Visma Business NXT - API Examples

## Introduction
This repository conatins a Pyton Flask Application which contains code-examples for integrating to Visma Business NXT using the GraphQL API.
## Requirements
### Python / Flask
This solution is developed in Python and requires Python to run. Before running you must have Python installed on your computer [https://www.python.org/downloads/]

## Getting started
### Windows
To download the application to your computer you clone it from git:
C:\code>git clone https://github.com/Visma-Software-AS-Product/BusinessNXT_API_Examples.git

The code is now downloaded into the folder C:\code\BusinessNXT_API_Examples

Create a Python Virtual Environment called virtualenv (could be any name) for the application:
C:\code\BusinessNXT_API_Examples>python -m venv virtualenv

Activate the virtual environment:
C:\code\BusinessNXT_API_Examples>virtualenv\Scripts\activate

Your virtual environemnt is now activated and you work within that environment
(virtualenv) C:\code\BusinessNXT_API_Examples>

Install required Python packages into your virtual environment:
(virtualenv) C:\code\BusinessNXT_API_Examples>pip install -r requirements.txt

Run the application:
(virtualenv) C:\code\BusinessNXT_API_Examples>flask run

The application is now running and available on the following url: http://127.0.0.1:5000

Running application on https, for some of the functionality (login with interactive user), it is required that the application runs on https, you can start the application with a adhoc created cert with the following command:
(virtualenv) C:\code\BusinessNXT_API_Examples>flask run --cert=adhoc




### Visual Studio Code

### 

## Links
* [Visma Business NXT API Documentation](https://docs.business.visma.net/)
* [Visma Developer Portal](https://oauth.developers.visma.com/)
