# To run the project in the local machine
1. Set the following environment variables<br>
EMAIL (gmail account email for email verification functionality)<br>
PASSWORD (corresponding password)<br>
SECRET_KEY (random string)<br><br>
2. Install all packages listed in requirments.txt file.<br><br>
3. Restart terminal or cmd and naviage back to the project folder.Here run the following commands( to initialize SQLite database )<br>
`flask db init`<br>
`flask db migrate`<br>
`flask db upgrade`<br><br>
4. Finally inside project directory containing `app.py` file execute `python app.py` to start the local server.


