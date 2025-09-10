# linkedin-profile-data-collection
Automated the process of collecting LinkedIn user profiles based on roles

## Data Collection
Users working in Tech, Consulting and Entrepreneurship, located in North American region. Based on the profile scoring, the top 3 users are considered for all roles.

Then the user profiles are saved in a csv file as:
'''
username, name, location, category, role, url
'''

### Working with automation script
Create a new project in Google cloud -> Enable Custom Search API -> Create an API key => Google API Key

Programmable Search Engine -> Create a new engine -> This create a search engine id => Search Engine ID

## Extracting info about the user profile using RAPIDAPI
https://rapidapi.com/karimgreek/api/linkedin-scraper-api-real-time-fast-affordable/playground/apiendpoint_8343c264-1a96-43d6-807d-d73559461670

Using the RAPIDAPI key, access the API Endpoint by setting the username param with the actual username collected from the automation.
Info like basic_info, education and experience is retrieved as response.



