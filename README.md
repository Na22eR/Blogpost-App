Blog-it
=====================================

## About
GitHub repository for the 2023 Object-Oriented Software Development lecture at the University of Applied Sciences Augsburg.

The project aims to create a blogpost application with user management using the Django framework.

## Getting started

### Prerequisites
- Python 3.11 or later, download [here](https://www.python.org/downloads/release/python-3110/)

    
  
- PIP
  
        # python -m ensurepip --default-pip


### Installation
Clone the repository 

    # git clone https://github.com/Na22eR/Blogpost-App.git
   
Run the command in the project directory

    # pip install -r requirements.txt


### Setup
To use the password reset function, you will have to provide a "credentials.py" file specifying the variables "C_EMAIL_HOST_USER" and "C_EMAIL_HOST_PASSWORD" for a Google Account that has an app password set.
Alternatively, you can directly change the "settings.py" file and specify your login credentials there. 

### Start
To start the application run the following command in the project directory

    # python manage.py runserver

## Usage
After you have used the runserver command, the path to the application will be displayed on the command line.

In order to use Blog-it, you will need to create an account. Note that to reset the password, you will have to specify the email linked to your account.

## License
This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
