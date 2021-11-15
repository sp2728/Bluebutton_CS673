#EMR Blue Button Integration Team

###Steps to Install the application

Requirements to install the application:
- Python 3 or greater
- Sqlite3


Code the Github repository

``git clone https://github.com/sp2728/Bluebutton_CS673.git ``

Install the requirement

```pip install -r requirements.txt```

Create a .env file in you local and add the secret keys and redirect URI

```
CLIENT_ID = xxxxxxxxx
CLIENT_SECRET = xxxxxxx
REDIRECT_URI= xxxxxxx
```

Run the application using

```python app.py```