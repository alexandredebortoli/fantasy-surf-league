# Fantasy Surf League

This project is a web application built as the final project for the CS50W course. It is a World Surf League Championship Tour game, similar to a fantasy sports league, where users can make event predictions for surfers and accumulate points based on the accuracy of their predictions. The app allows users to join or create leagues to compete with friends and track their rankings.

The application is designed to provide a dynamic and engaging experience for surf enthusiasts, allowing them to stay updated with the latest championship tour information and compete with others in a friendly competition.

## Distinctiveness and Complexity

This project stands out from other projects in the CS50W course due to its unique combination of features and technologies that have not been implemented in the other projects.

1. **Web Scraping**: One of the key features of this project is the integration of web scraping to fetch real-time data from the official [World Surf League website](https://www.worldsurfleague.com/). This data includes information about surfers, events, and rankings, which is then stored and updated in the database. Implementing web scraping adds a unique and dynamic aspect to the application, ensuring that users have access to the latest information about the championship tour.

2. **Custom Middleware**: To automate the web scraping process, a custom middleware has been implemented to run the scraper based on the information available in the database. This middleware ensures that the application stays up-to-date with the latest data without manual intervention, enhancing the user experience and the overall functionality of the app. The middleware will run the scrapper if events table is empty or if there is a event whose end date has passed and status is not Completed or if there is a event whose start date has passed however status is not Completed or Live. 

3. **User Interaction**: The application utilizes JavaScript to enhance user interaction and provide a seamless experience. For example, users can view each event prediction they've made on the profile page without needing to reload the entire page. This improves usability and makes the application more responsive to user actions.

4. **League Creation and Joining**: Users have the ability to create or join leagues, allowing them to compete with friends and track their performance relative to others. This social aspect adds depth and complexity to the application, creating a community-driven experience for users.

5. **Points System**: The application implements a points system where users earn points for correct event predictions. This adds a competitive element to the game and motivates users to participate actively in making predictions for each event.

6. **Theme Toggle**: The addition of a theme toggle feature, where the theme is automatically set based on the user's device appearance preference, adds an extra layer of complexity to the project. This feature requires detecting and accessing the user's device appearance settings and dynamically applying the appropriate theme to the application. The default theme is set to dark.

## File Contents

- **wsl_fantasy/**: The main project directory.
  - **settings.py**: Contains project settings including database configuration, middleware, static files, and template directories.
- **fantasy/**: The app (WSL Fantasy Game) directory.
  - **static/**: Static files directory.
    - **images/**: Directory containing the app's images such as the favicon.
    - **main.js**: Contains all the javascript code for the project.
    - **static.css**: Contains all css styling for the app other than the bootstrap styling.
  - **templates/**: HTML templates directory for rendering the web pages.
    - **base.html**: HTML template used as base layout that is extended by others HTML templates in the project.
    - **pages/**: HTML templates directory specific for the app's web pages that extend the `base.html` template.
      - **create-or-join-league.html**: HTML templates for creating or joining a league web page.
      - **events.html**: HTML templates for displaying events web page.
      - **index.html**: HTML templates for displaying home web page.
      - **league.html**: HTML templastes for displaying league web page.
      - **login.html**: HTML templates for displaying login web page.
      - **profile.html**: HTML templates for displaying profile web page.
      - **rankings.html**: HTML templates for displaying rankings web page.
      - **register.html**: HTML templates for displaying register web page.
      - **surfers.html**: HTML templates for displaying surfers web page.
  - **models.py**: Defines database models for user, surfer, event, prediction, league, and ranking.
  - **views.py**: Contains view functions for handling HTTP requests and rendering templates.
  - **urls.py**: URL routing for the application.
  - **webscraper.py**: Web scraping functionality.
  - **task.py**: Updating database with latest data from web scraping.
  - **middleware.py**: Custom middleware for web scraping.

## How to Run

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Run migrations to create database tables by running `python manage.py migrate`.
5. Start the development server by running `python manage.py runserver`.
6. Access the application in your web browser at http://localhost:8000.

## How to Play

1. Sign Up/Login: If you haven't already, sign up for an account or log in with your existing credentials.
2. Join or Create a League: Once logged in, you can join an existing league or create your own league to compete with friends.
3. Make Event Predictions: Navigate to the profile page to view upcoming events on the World Surf League Championship Tour. For each event, you can predict the first and second-place surfers. Remember that you cannot repeat the first-place surfer in the second-place prediction.
4. Submit Predictions: Once you've made your predictions for an event, submit them before the event starts. You cannot add predictions to an event that has already started.
5. Earn Points: Points are awarded based on the accuracy of your predictions. See below for details on the points system.

## Points System

The points system for event predictions is as follows:

1. Each prediction starts with 0 points.
2. If your predicted first-place surfer matches the actual first-place surfer of the event, you earn 200 points.
3. If your predicted second-place surfer matches the actual second-place surfer of the event, you earn 100 points.
4. If both your first and second-place predictions are correct (totaling 300 points), you earn an additional 100-point bonus.
5. If your predictions are incorrect, you do not earn any points for that event.

## Tech Stack

- [Django](https://www.djangoproject.com/)

- [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

- [Bootstrap Icons](https://icons.getbootstrap.com/#install)

- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

- [Requests](https://pypi.org/project/requests/)

## Author

- [@alexandredebortoli](https://www.github.com/alexandredebortoli)
