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
 4. Make config.json file from example.config.json
    
    * Make copy of example.config.json and name it config.json
    * Fill your azure account and mail details
 
 <br/>
 
 ## Run the Project
    
 * Open terminal and go to project (Visualization-Dashboard) directory in terminal and run the command
    
    ```
    cd Visualization-Dashboard
    python manage.py migrate
    python manage.py runserver
    ```
  
    - browse the [http://127.0.0.1:8000/dashboard/home/](http://127.0.0.1:8000//dashboard/home/)
