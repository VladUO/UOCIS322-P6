# UOCIS322 - Project 6 #
Brevet time calculator with AJAX, MongoDB, and a RESTful API!

Author: Vladimir Shatalov
Address: vvs@uoregon.edu


This is a major modification/addition to the brevets program that we built earlier. Or latest version of the brevets program stored the open and close times in a MongoDB database. This addition uses Flask API to retrieve that information from the database and to display it for a user in either JSON or CSV format.

The new program uses docker-compose to build three separate containers, one container contains the original brevets app in it, another container has the new input/output website, and the third container has the API.

The “admin” user can enter some values in the brevets app and submit those to the database. Then a user that wants to retrieve the numbers opens a different html file using another port. Inside that HTML file the user can pick which times to display, in what format, and how many from the top. The values default to JSON and “full list” for output.

Once the user selects what they want displayed, they can click the Submit button and the selections are sent to the website.py file in the form of a POST request. My program has three separate post requests: All, OpenTimes and CloseTimes. In the website.py the selections are extracted and a request url is formatted, then a request is made to a function in api.py running in another container.

Within api.py there are three functions: listAll which lists all the times, listOpenOnly which lists open times only and listCloseOnly which lists close times only. There are also two support functions: toJson converts the output to a JSON format, and toCSV which converts the output to CSV format. 

Inside the list functions the data is pulled from the database and the unnecessary values are discarded. Afterwards, depending on the format selected, the remaining list is sent to the appropriate support function for processing, and from there returned to website.py.

The website.py function simply sends out the data in whatever format through a return statement. In my program that data is then output on the submit page. 



     
