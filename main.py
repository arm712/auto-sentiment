from tweepy import Stream
from ingestion.database import twitterDB
from ingestion.api import API
from ingestion.sniffer import MySniffer
import time

# Init all the required objects
api = API()
db = twitterDB()
ts = time.strftime("%m%d%y %H%M%S", time.gmtime(time.time()))
db.load_coll(ts)

# Display the options
print("What do you want to do?")
print("1.- Stream tweets from Twitter.")
print("2.- Call the model.") # Not sure how to go from here
print("3.- Calibrate the model.")

working = 1

while working == 1:
    print("Please enter the option number.")
    option = input(">")
    try:
        option = int(option) #
        if (option > 0 and option < 4):
            working = 0
        else:
            print("Option number not valid. Enter a number between 1 and 3.")
    except ValueError as e:
        print("Input %s is incorrect, please enter a number." % str(e))

if (option == 1):
    working = 1
    while working == 1:
        print("For how many minutes do you want to get Tweets?")
        minutes = input(">")
        try:
            seconds = float(minutes)*60
            if (seconds < 30):
                print("Please enter a higher number.")
            else:
                working = 0
        except ValueError as e:
            print("Input %s is incorrect, please enter a number." % str(e))
    print("Reading twitter for %r minutes." %minutes)
    sniffer = Stream(api.auth, MySniffer(api, db, seconds))
    sniffer.filter(track = ['volkswagen', 'toyota', 'general motors'], languages = ['en'])

elif (option == 2):
    print("Calling the model")
elif (option == 3):
    collections = db.get_collection_names()
    i = 1
    print("Please type the number of the collection you want to read.")
    for c in collections:
        print("%d.- %r" %(i, c))
        i += 1

    working = 1

    while working == 1:
        print("Please enter the collection number.")
        option = input(">")
        try:
            option = int(option) #
            if (option > 0 and option < i):
                working = 0
            else:
                print("Option number not valid. Enter a number between 1 and %d." %(i-1))
        except ValueError as e:
            print("Input %s is incorrect, please enter a number." % str(e))

    db.load_coll(collections[option-1])
    db.calibrate_tweet()

