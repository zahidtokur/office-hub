## Office Hub
Office Hub is a project that contains a collection of API endpoints for creating a platform where in-office events can be organized and followed, requests, suggestions and complaints can be forwarded to managers and surveys can be made.

For my first proper introduction to **Django REST Framework**, I wanted to create something that can be directly used in my environment.

## Features
 - (Fun) user profiles.
	 - A job title can be added.
	 - A self-description can be created to better describe who you are, what you do etc.
	 - Create skill tags.
 - Creating and following up on events.
	 - Create events and invite people to your events.
	 - Events can only be viewed by people invited to it, and the person who created it.
	 - Comment on events.
 - Forward your requests, suggestions and complaints to managers.
	 - Feedbacks will only be seen by managers and users who created it.
	 - Feedbacks can be anonymous or not.
 - Create surveys (not added yet).

## Requirements

To install requirements, run:

    pip3 install -r requirements.txt

Then, create a django secret key [here](https://djecrety.ir/) and put it in ***secret_key.txt*** file at root directory or directly paste in project's ***settings*** file.

Lastly, migrate.

    python manage.py migrate

## API Documentation
You can head over to [my documentation on POSTMAN](https://documenter.getpostman.com/view/8627195/TVKHUFHe) to view the documentation for the endpoints.
