# FardaaStationAPI
This project has two main purposes:
 1. To scrape Radio Farda's website for new episodes of Fardaa Station and keep
 a database locally of the information of each episode.
 2. Serve as a web service API that clients can call to get the most updated 
 episode information
 
Episode information that I store locally are:
 - Episode title
 - Publish date
 - Image URL
 - High quality audio file download URL
 - Low quality audio file download URL
 - Timestamp for the time the episode was scraped
 - Base URI for the episode on Radio Farda's website

To install requirements locally, run these commands in the root directory of the project:
 - virtualenv env
 - source env/bin/activate
 - pip install -t lib -r requirements.txt

To test the app locally, run this command in the root directory of the project:
 - dev_appserver.py .

To deploy to GAE run this command:
 - gcloud app deploy
 
To deploy the crop job to GAE run this command:
 - gcloud app deploy cron.yaml