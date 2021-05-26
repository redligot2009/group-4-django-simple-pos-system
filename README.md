# Group 4 Django Simple POS System

A simple POS system built with Django, MySQL, Bootstrap, and JQuery. Deployed on an AWS EC2 instance, with a simple CI/CD pipeline using Gitlab.

## How to set up the project locally ##

1. Ensure you have **Docker** and **Python** installed at the very least. Installation instructions can be googled.

    1. Ensure that `pipenv` is installed globally by running the following command: 
    
        ```bash
        pip install pipenv
        ```
        **Pipenv**, for context, is a relatively **user friendly** way of **managing dependencies** and Python **virtual environments**. It will be important for local testing later on, so make sure it really is installed.

    2. Afterwards, **ensure that you have the `docker-compose` command line interface installed** after installing Docker Desktop. To check if you have installed both correctly, simply do the following commands:

        ```bash
        docker --version
        docker-compose --version
        ```
        If there are no problems (e.g. "command not found"), then it means you have installed them correctly.

    3. **If you are on a Windows machine, there are extra steps** to follow in order to use Docker in a performative way on your machine.

    4. In particular, you have to **set up WSL 2 (Windows Subsystem for Linux)** in order for Docker to not be slow as molasses.
    https://docs.microsoft.com/en-us/windows/wsl/install-win10

    1. Afterwards, assuming that you have already cloned the project using `git clone`, you should navigate to the `app` folder: 

        ```bash
        cd app
        ```

        And then run in order to **activate the virtual environment**: 
        ```bash
        pipenv shell
        ```
        
        Followed by: 
        ```bash
        pipenv install
        ``` 
        
        in order to **install all dependencies**.


2. After having done all of the prior steps, for purely local development purposes, **you may test the project locally by doing the usual set of steps**:
   1. `python manage.py migrate` in order to apply database migrations.
   2. `python manage.py runserver` in order to run the local development server.
3. However, in addition to this, **you also have the option to run the following commands to build the project inside a Docker container**:
    1. `docker-compose up -d --build` <-- what this does is, it spins up your container in a "detached" instance (with the `d` tag) running in the background. 
   
        **If the image has not yet been built, it will be built beforehand** with the use of the `--build` tag.

        **Important note:** when coding with a container, you will have to either: rebuild with each change, or code *inside* the container.

        **For practical reasons, it might be best to opt for the usual local development workflow with Django**, and only build the container when you want to make sure it will *really* work live.

    2. Once the project has fully built, and the entire build log of Docker has finished, **you can visit `localhost:8000` in your browser and see the exact same thing** as you would if you were deploying the app live on an AWS EC2 instance.

    3. To **shut down the container** when not in use, simply run `docker-compose down` to "collapse" it for until the next time you need it.