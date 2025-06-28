# **Nutrition assistant**
<img src="https://res.cloudinary.com/dufdl1zxp/image/upload/v1702123395/give-me-an-onion-and-tomato-logo_1_wzn4b3.png" height="80" width="80" align="center">

#### Description: Nutrition assistant is an app built to aid the daily nutritional lives of users.

## Languages;

HTML, CSS, JavaScript, flask and SQL

## Folders;

### templates:
Nutrition assistant has a total of 11 HTML files in the template folder

**index.html:**
This contains code for the structure of the index page from which you can navigate to login or signup through the menu.

**layout.html:**
This contains code for the nav and background layout of the login and signup pages.

**layout2.html:**
This contains code for the nav and background layout of the profile.html, meal.html, search.html, track.html, search.html

**login.html:**
This contains code for collecting input which are username and password for login.

**me.html:**
This contains code to display the account details and account control.

**meal.html:**
This contains code to display meal suggested to the user from where users can navigate to the steps for preparation.

**profile.html:**
This contains code to display a page from where users can access the app features.

**search.html:**
This contains code to display results and receive input from the users

**signup.html:**
This contains code to collect users information for signup

**track.html:**
This contains code to display a page from where users see a chart of their water intake trend


### static:
This app has 7 image, 2 javascript files, and 3 CSS files files in the static folder:

**images:**
bac.png, female.png, icon.png, img-1.png, img-2.png, img-3.png, img-4.png, male.png

**CSS:**

layout.css: styles the login and signup page

layout2.css: styles the profile, meal, layout2, me, search, and track page

styles.css: styles the index page

**JS files:**

layout2.js: controls user interaction for the profile, meal, layout2, me, search, and track page

index.js: controls animation and interaction for the index, signup and login page


## Backend files:

**app.db:**
It consists of 5 diffrent tables:

users: stores the users name, username, password, gender, diet and id

tracker: this table stores the users water intake data

tips: Bunch of nutritional tips which is rendered on the users profile page daily

history: stores date of when the user was last sen

sqlite_sequence: stores the number of rows in each table

**app.py:**

This consists of the routes and functions that makeup the backend



## Main features;

### Daily tips:
Gives diffrent nutritional tip each day

### Meal suggestion:
This suggests meals to the user based on the data inputed on signup, It also provides a link to get preparation process. This was implemented using ***edamam API***, and ***themealDB API***.

### Recipie Search:
This feature allows users to search for recipies based on the meal name, calorie range or diet preference, it outputs varieties of results each have health_labels, caution, diet_labels, ingredients and nutritional value. This was also implemented using ***edmam API***.

### Water intake tracker:
This feature helps users track their water intake, it also provides a graph/chart where users can view their water intake trend, this chart was implemented with ***chart.js***
