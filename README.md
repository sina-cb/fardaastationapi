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

To install requirements locally, run this command:
 - pip install -t lib -r requirements.txt

To upload to GAE run this command:
 - gcloud app deploy app.yaml --project fardastationapi