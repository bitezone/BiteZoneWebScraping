# April 16 9:33 PM
Working on extending the web scraping application to scrape nutritional value
- The category is closed - required to open the category box to be interactable to click on the menu

# April 17

** IMPORTANT ** - when introducing new columsn you have to run
```ALTER TABLE menu_items ADD COLUMN serving_size VARCHAR```
This will add a new column of your desired (will need to fix in production)

# April 18
Today we will try to do three main things
1) Set up web scraping for the four categories
[] Calories - Done
[] Serving Size - Done
[] Ingredients - Done
[] Allergies - Done
- Then, we will store these data information in the storage

1) We will crate API endpoints Backend
   - Research on what API endpoints to create
     - Added allergy_id for filtering
     - Added endpoint for each menu_item

2) We will then use all these information to display on the frontend
   - Work on displaying these dining hall information

3) We will then start researching on how to create a good calorie tracking
   - Create an idea board that display the interaction between different points to communicate with the user information and storage

How long do you expect each to take?
1
Ingredients - 30 mins
Allergies - 30 mins
Getting the data into the database - 30 mins

2
Backend endpoints - total 1.5 hour

3
Frontend - 1.5 hour

4
Calorie Tracking - 3 hours

- Time now 3:41 PM
