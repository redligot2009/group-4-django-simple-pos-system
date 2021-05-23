# Group 4 Django Simple POS System

A simple POS system built with Django, MySQL, Bootstrap, and JQuery.

## How to set up the project locally ##

1. Ensure you have MySQL (Server, Shell, and Workbench at the very least) installed. Set the password to be empty for your root user.

    https://serverfault.com/questions/103412/how-to-change-my-mysql-root-password-back-to-empty

2. Create a `posdb` database either via command line:
    
    ```cmd
    mysql -u root -p
    ```
    (Inside MySQL shell)
    ```sql
    CREATE DATABASE posdb;
    ```

    Or by using MySQL Workbench:
    https://stackoverflow.com/questions/5515745/create-a-new-database-with-mysql-workbench

3. Ensure you have Python installed. Afterwards, make sure to install `pipenv` globally, which is our virtual environment manager for this project.

    ```cmd
    pip install pipenv
    ```
4. Open project inside VS Code.
5. Run `pipenv shell` inside the integrated terminal (Shortcut: <kbd>CTRL</kbd> + <kbd>`</kbd>). This will set up the virtual environment for the project.
6. Run `pipenv install` to install all project dependencies. (Django, etc.)
7. Run `python manage.py migrate` in order to populate your local `posdb` testing database.
8. Run `python manage.py createsuperuser` to create a superuser if one needs to visit the admin site of the Django project.
9. Run `python manage.py runserver` to run the project's development server.
10. **And you're all done!** :)

