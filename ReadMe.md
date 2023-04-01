# Django-Google Calendar Integration

This project lays out how to integrate google Calendar with your Django application using Service accounts. It should give you enough to integrate your application without problems. For more information please look it up using google or email me. 

### Why Service Accounts?
Service accounts allow you to integrate your application without needing permissions from each user and without having to make them log into their Google account. 


## Start 

1. Run the following command to initialize the Django Project 
```
pip install django google-api-python-client oauth2client gunicorn whitenoise 
or 
pipenv install 
or
pip install requirements.txt
```

Set the values in the .env file

``` .env file
calendarId=...
UPDATE_GOOGLE=True
client_secret=...
```

## The Google Part

1. Go to the [Google Cloud Platform](https://console.cloud.google.com/) and make and account/log in.
1. Create a new Google Cloud and call it whatever you want. Im calling mine `Test Google Events`
1. On the top left of the screen next to the Google Cloud logo, click and select your project. 

### Creating a Sercive account

1. On the home page of your project click the APIs and Services Option
1. Go to the Credentials tab (on the left menu)
1. Select 'Manage service accounts' (for me it was just above the Service Account table on the right)
1. Select Create Service Account on the top 
    1. fill in everything normally
    1. Give it the role of owner (You can give it a more defined role if you wish but it is up to you to research which role you want for that service account)
    1. Administrators are optional 
    1. Once you save you will be take back to the service account page
    1. Save the service account email that is genereated
1. Under Actions click the menu of the service account you want to use 
and select 'Manage Keys' 
1. Select 'Add Key'
    1. Select JSON and press 'Create'(this will download a key file to your computer)
1. Open this file and put it all into one line (so that we can add it to the environment variables)
1. Add it to the environment variables under the name `client_secret`
1. (for this to work you need to make sure that the key can be read by json.load(os.environ.get('client_secret')) otherwise it will not work correctly)

### Giving API access 

1. Click on the menu on the top left and select APIs & Services
1. In the 'Enabled APIs & services' screen, press 'Enable APIS and Services'
1. Find and enable the 'Google Calendar API'


### Link Google Calendar 
1. Go to [Google Calendar](https://calendar.google.com/calendar/u/0/r) 
1. (Make a new Google Calendar if you dont have one already)
1. On into the Settings of the Calendar
1. Go to Share with specific people or groups 
    1. Share with the service account 
    1. 'Give make changes to events' Permisson
1. Scroll down to Integrate Calendar
1. Copy "Calendar ID" and add it as an environment variable called "calendarId"

### Your Django project and Google Calendar are now linked 

## Back to the Project 

1. launch the project 
```
gunicorn google_events.wsgi --log-file - 
or 
python manage.py runserver
```
2. Create an Event this should now show up on the Google Calendar you linked

Thats is it!

## Final Notes 

When you open the admin interface you will see that there is a Google events page. This page shows all the events that are in the google calendar it and whether they are linked to an event in your Database. 

If you set `UPDATE_GOOGLE` environment variable to False, 0 events will not be sent to google.

## adding to this repo

If you feel like there is a better way of doing something, please create a merge request and i will have a look at it and merge it if it is good.


### hope this has been helpful 


## More information on the Calendar API can be found in the [Google's Quickstart Guide](https://developers.google.com/calendar/api/quickstart/python)