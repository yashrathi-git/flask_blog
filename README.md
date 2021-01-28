# To run the project in the local machine
1. Set the following environment variables\
EMAIL (gmail account email for email verification functionality)\
PASSWORD (corresponding password)\
SECRET_KEY (random string)\
\
2. Install all packages listed in requirments.txt file.\
\
3. Restart terminal or cmd and naviage back to the project folder.Here run the following commands( to initialize SQLite database )\
`flask db init`\
`flask db migrate`\
`flask db upgrade`\
\
4. Finally inside project directory containing `app.py` file execute `python app.py` to start the local server.\


