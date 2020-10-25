# Ardoq Code Tasks 1 & 3


Task 3 takes a given month of historical data and displaying it out over google maps,
along with a chart displaying the amount of bikes that have been locked and unlocked
in (up to) the last twelve hours.
Green circles indicate a bike being unlocked, while a red circle
indicates that a bike was locked.

#### Running Task 3:

Generate a google maps API key.
Paste the key into line 9, col 54 in index.html: ```src="https://maps.googleapis.com/maps/api/js?key=<PASTE KEY HERE>...```

Then run the following shell commands to start the application:
```
$ pip install -r requirements.txt
$ python task3.py -y <year> -m <month>
```

Year and month must be between april 2019 and october 2020 (inclusive)

If a browser window does not automatically open upon task3.py completing, 
you will have to open ```index.html``` manually (in a browser of your choice).
