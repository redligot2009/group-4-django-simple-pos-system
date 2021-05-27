# Group 4 Django Simple POS System

A simple POS system built with Django, Bootstrap, and JQuery. Painstakingly deployed on an AWS EC2 instance (http://35.173.164.153/), with a simple CI/CD pipeline using Gitlab for our **ISCS 30.28A-Q4 (Introduction to Continous Integration / Delivery)** class.

## Resources consulted ##

* **"Dockerizing Django with Postgres, Gunicorn, and Nginx"** by Michael Herman, June 2020
https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
* **"Continuously Deploying Django to AWS EC2 with Docker and GitLab"** by Michael Herman, April 27 2020
https://testdriven.io/blog/deploying-django-to-ec2-with-docker-and-gitlab/

## Project structure in a nutshell ##
All Gitlab build and deployment related files, `docker-compose` files, as well as the `deploy.sh` and `setup_env.sh` scripts run during the `deploy` stage are declared at the root-level directory.

The `nginx` folder contains a simple Nginx configuration to redirect requests for both the actual live app, and its related static assets to the correct places.

The actual Django app lives inside an `app` directory for ease of local testing, containerization, and eventual deployment. Also defined here are the testing and production `Dockerfile` with their respective `entrypoint.sh` which is used when being `docker-compose`'d.

## Testing environment in a nutshell ##

For testing, it uses the default **SQLite** database that comes with Django projects, while running the development server through `python manage.py runserver` (either in a Docker container or within a local virtual environment).

## Production environment in a nutshell ##

For the actual production environment, it uses **PostgreSQL** as the database, running on top of **Gunicorn** as a WSGI compliant **HTTP Server** to serve our Django app, while using **Nginx** as a **reverse proxy server** to redirect the live production app's requests for static assets to the correct volume location in the Docker container that the entire app lives in.


## CI / CD setup in a nutshell ##

The project is hosted on Gitlab, and declares a CI pipeline inside `.gitlab-ci.yml` containing the `build` and `deploy` stages, and their respective jobs.

Builds are performed using a Gitlab runner that uses a Docker image (dind / Docker-in-docker) underneath. 

The deployed app is composed of three Docker services living in their own containers: 

- `web` - the Django app proper, served via Gunicorn.
- `db` - the PostgreSQL database where all persistent data is stored. *(Built from a Postgres Alpine docker image for simplicity.)*
- `nginx` - the Nginx reverse-proxy server which redirects requests accordingly based on a pre-defined `nginx.conf` file. *(Built from an Nginx Alpine image for simplicity)*

There are three `docker-compose` files in the project:
- **`docker-compose.yml`** - the default `docker-compose` for when you're testing locally on your machine.
- **`docker-compose.ci.yml`** - the `docker-compose` for when you're triggering the `build` stage related jobs of the Gitlab CI pipeline.
- **`docker-compose.prod.yml`** - the `docker-compose` for when you're triggering the `deploy` stage related jobs of the Gitlab CI pipeline.

Each of these are used depending on the `stage` of the Gitlab CI pipeline, and on which particular job is being performed.

For the `deploy` stage, environment variables are declared in the Gitlab project settings which defines variables such as the `SECRET_KEY`, `SQL_USER`, `SQL_PASSWORD`, among many others which are utilized in the different `docker-compose`  and `Dockerfile` variants.

## AWS EC2 setup in a nutshell ##

The project's EC2 instance lives on the `us-east-1` region, as per what our class's AWS Educate accounts permit, and was built through the default AMI image. 

As the IP address changes when the instance is automatically stopped after some time, a fixed AWS Elastic IP has been associated with the instance to prevent any headaches pertaining to doing SSH-related tasks on the live instance.

The `deploy.sh` script, responsible for the actual deployment, *enters* into the AWS EC2 instance via SSH, passing in the correct SSH Private Key for the allowed public keys defined in the AWS EC2.

It runs a set of `bash` commands in order to:
* Log in to the Gitlab container registry for the project where our built Docker images live.
* Pull changes from the Docker images built in the previous `build` stage.
* `docker-compose` everything so that all three services of the app are running on the live instance.

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
        
        This is done in order to **install all dependencies**.


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

        **NOTE:** When collapsing a Docker container, volumes get left behind so that when you restart the containers, the data inside the container persists.

        If you need to "clear" the database contents before closing the container and restarting anew, you can run:

        ```bash
        docker-compose down -v
        ```

        Where the additional `-v` flag tells Docker to also clear the volumes on your machine after shutting down the containers.