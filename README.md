# Japan Travel Survery

#### Video Demo: <https://youtu.be/rvVj_HIw04E>

#### Description:

My project is a web-based application built with Flask. It features a Japan travel survey that provides personalized recommendations for destinations and activities based on user responses.

My project contains many files:

### app.py file

Handles most of the logic for the project.
I used the flask library, that incorporated
**render_template** which rendered all the templates that are in the project
**request** because I was using GET and POST in my routes
**redirect** which redirects the user the to the results page and keeps track of their user_id
**url_for** which is a jinja syntax
I imported **sqlite3** so I could make a database

### The routes

There is a route that renders the index.html file.
That is the first page of the user sees to introduce the user to the survey.
**survey route** that takes the user to the survey that has 8 questions for the user to answer
**submit route** gets the user responses form the form. It uses **with** to open
and close the database file. After the user answers, the answers are stored in the
user repsonse table. Then the page is redirected to the results page of the specific users answers.
**results route** it connects to the database and converts the stored answers to the answer id's. It queries the database for the matching destinations for each question and counts how many times a destination was chosen; **there are multiple destinations that correspond to each answer**. The destinations are scored and orderd by descending order. There are three rankings for the destinations. The users **top choice**, **second choice**, and **third choice**. 
Destinations are ranked based on a scoring system:
* Top Choice: Score of 5 or more
* Second Choice: Score of 3–4
* Third Choice: Score of 2 or less
  - This ranking system ensures users receive multiple travel suggestions while still prioritizing the best-matching options.
I wanted to show all possible choices, to give the user options. I also figured the user would never see all the choices no mater how many times the survey was taken.


**destination route** After the survey is done the results page shows the ranked destinations. I wanted the user to be able to click on the destinations to see possible activites that they can do in those places. So the destination route leads the user to a "destination".html file for the destination that is clicked.

### The Templates 

**layout.html** has the main boilerplate "layout" for all the html files. Which all files use jinja syntax to extend the layout.html.
**index.html** is the welcome page to the survey. I has a simple title, two paragraph tags, and a button that takes you to the survey.
**survey.html** lists all 8 questions to the survey. The style is a radio type input. This allows the user to see all the questions at once and be able to go back and change any of their answers before moving to the results page. This page used input tags that connect the answers to the answers in the database using the answer id. It also uses label tags, which is what the user sees when looking at the survey. Then there is a submit button that brings the user to the results page.
**results.html** separates the users choices into the different rankings using a h2 tag, that was previously mentioned. It uses jinja to reference the css.html page for the style of the destination cards. The destination links open a new tab, by using target="\_blank". I wanted the user to be able to easily go back to the survey and click on the other choices, while still being able to keep the specific destination page. There is also a "Retake Survey" button that takes the user page to the beginning page.
**destination.html** There are 12 destinations: Fukuoka, Hakone, Hiroshima, Kanazawa, Kyoto, Nara, Okinawa, Sapporo, Shikoku, and Tokyo. Each page follows the same structure. It includes an <h1> tag for the destination title and multiple paragraph tags. I separated each activity description for clarity. There are also img tags to show an example of the place to go to. Each page also has links to the event page if you have to buy a ticket or just want more information about the activity. i also figured 

### The Static pages

There is an **image folder** that holds the pictures for the destination cards along with individual "destination" picture folders that has all the pictures connected to the activities described in each destination page.
There is a **style.css** file that holds all the style for the pages. Each destination page has a quote to describe each destination that is centered on the screen and italicized. All the wording and pictures are centered on the page as well. I first wanted the text to wrap around the pictures, but some descriptions did not have enough text to wrap around the pictures like I wanted, so I came to the conclusion of just centering everything. I placed the picture above or below the text depending on what the other information looked like. If there was a picture below text then the next description text would have the picture also below it. However, some descriptions I could not find license free pictures so some of the picture are above the text.

### The Questions database

"The database consists of multiple tables, including:

* Questions Table: Stores the survey questions.
* Answers Table: Contains possible responses and their corresponding destinations.
* Destinations Table: Lists the destinations with descriptions and images.
* Recommendations Table: Maps answers to destinations.
* User Responses Table: Stores individual survey responses for result generation.

ChatGPT helped with coming up with the questions and some destinations. ChatGPT also characterized each destination to the proper question description. ChatGPT also helped with debugging the code. ChatGPT provided the quotes for each destination.
Google also helped with adding more destinations.



