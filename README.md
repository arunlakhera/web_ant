# web_ant

The Web Ant Crawler is developed to scrape through courses offered in the iNeuron website.

1. It scrapes list of all the courses provided in the iNeuron website including Category and SubCategories.
2. User then can browse through these categories / subcategories to view all the courses within them.
3. When user clicks on any course , they can view the summary detail of the course from the website.
4. User can then save the course detail in Amazon S3 storage.
5. All the course related data scraped is stored in mongo DB.
6. We also store the course related details in MySQL using this application.
7. This application is deployed in the Beanstalk , Azure & AWS.
8. The application uses logging to log all the information.
9. All the required packages have been provided in the requirements.txt file.
10. Data is scraped only for learning purpose and is deleted and app removed from deployed server.


