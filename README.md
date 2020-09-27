# E-commerce Monitoring System

<br>


 ## Setup the Project
 
 1. Install Python 3.6
 
 2. Create a virtualenv and activate it
 
    ```
    $ pip install virtualenv
    $ virtualenv venv
    $ venv\Scripts\activate        # For Windows
    $ source venv/bin/activate     # For Linux
    ```
 
 3. Goto root directory named "games_of_data" of django project and Install dependencies
    ```
    cd games_of_data
    pip install -r requirements.txt
    ```
 
 <br/>
 
 ## Run the Project
    
 * Open terminal and go to project (games_of_data) directory in terminal and run the command
    
    ```
    cd games_of_data
    python manage.py migrate
    python manage.py runserver
    ```
  
    - browse the [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
