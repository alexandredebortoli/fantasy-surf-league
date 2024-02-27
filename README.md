# World Surf League Championship Tour Game

This project is a web application built as the final project for the CS50W Harvard EdX course. It is a World Surf League Championship Tour game, similar to a fantasy sports league, where users can make event predictions for surfers and accumulate points based on the accuracy of their predictions. The app allows users to join or create leagues to compete with friends and track their rankings.

## Distinctiveness and Complexity

### Why it satisfies the distinctiveness and complexity requirements:

1. **Web Scraping**: One of the key features of this project is the integration of web scraping to fetch real-time data from the official World Surf League website. This data includes information about surfers, events, and rankings, which is then stored and updated in the database. Implementing web scraping adds a unique and dynamic aspect to the application, ensuring that users have access to the latest information about the championship tour.

2. **Custom Middleware**: To automate the web scraping process, a custom middleware has been implemented to run the scraper based on the information available in the database. This middleware ensures that the application stays up-to-date with the latest data without manual intervention, enhancing the user experience and the overall functionality of the app.

3. **User Interaction**: The application utilizes JavaScript to enhance user interaction and provide a seamless experience. For example, users can view and update their event predictions on the profile page without needing to reload the entire page. This improves usability and makes the application more responsive to user actions.

4. **League Creation and Joining**: Users have the ability to create or join leagues, allowing them to compete with friends and track their performance relative to others. This social aspect adds depth and complexity to the application, creating a community-driven experience for users.

5. **Points System**: The application implements a points system where users earn points for correct event predictions. This adds a competitive element to the game and motivates users to participate actively in making predictions for each event.

## What's contained in each file:

- **django_web_app/** \*/: The main Django project directory.
- **settings.py**: Contains project settings including database configuration, middleware, static files, and template directories.
- **urls.py**: Defines URL patterns for routing requests to the appropriate views.
- **wsgi.py**: Configuration for the WSGI application used by the web server.
- **surf_league/**: The Django app directory.
- **models.py**: Defines database models for surfers, events, predictions, leagues, and user profiles.
- **views.py**: Contains view functions for handling HTTP requests and rendering templates.
- **forms.py**: Defines forms for user authentication, event predictions, and league creation.
- **templates/**: HTML templates for rendering the web pages.
- **static/**: Static files such as CSS, JavaScript, and images.

## How to run the application:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Run migrations to create database tables by running `python manage.py migrate`.
5. Start the development server by running `python manage.py runserver`.
6. Access the application in your web browser at http://localhost:8000.

## Additional information:

- This project was developed as the final project for the CS50W Harvard EdX course.
- It utilizes Django for the backend, JavaScript for interactivity, and Bootstrap for styling.
- Web scraping is used to fetch real-time data from the official World Surf League website.
- A custom middleware automates the web scraping process based on information in the database.
- Users can make event predictions, earn points for correct predictions, and join or create leagues to compete with friends.
- The application is designed to provide a dynamic and engaging experience for surf enthusiasts, allowing them to stay updated with the latest championship tour information and compete with others in a friendly competition.#

# Strategies

- web scraping
- cache

### Dependencies

- [Django](https://www.djangoproject.com/)

- [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

- [Bootstrap Icons](https://icons.getbootstrap.com/#install)

- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

- [Requests](https://pypi.org/project/requests/)
