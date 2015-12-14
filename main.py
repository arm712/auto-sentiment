from tweepy import Stream
from ingestion.database import twitterDB
from ingestion.api import API
from ingestion.sniffer import MySniffer
import time

def ask_number(max_num, min_num):
    aux = 1
    while aux == 1:
        print("Please enter the option number.")
        option = input(">")
        try:
            option = int(option)
            if (option >= min_num and option <= max_num):
                return option
            else:
                print("Number not valid. Enter a number between %d and %d." %(min_num, max_num))
        except ValueError as e:
            print("Input %s is incorrect, please enter a number." % str(e))

def select_collection(db):
    collections = db.get_collection_names()
    i = 1
    print("Please type the number of the collection you want to read.")
    for c in collections:
        print("%d.- %r" %(i, c))
        i += 1
    number = ask_number(i-1, 1)
    return collections[number-1]

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

option = ask_number(3,1)

if (option == 1):
    print("For how many minutes do you want to get Tweets?")
    minutes = ask_number(480,1)
    seconds = minutes*60
    print("Reading twitter for %d minutes." %minutes)
    sniffer = Stream(api.auth, MySniffer(api, db, seconds))
    sniffer.filter(track = ['volkswagen', 'toyota', 'general motors'], languages = ['en'])
elif (option == 2):
    print("Calling the model")
elif (option == 3):
    collection = select_collection(db)
    db.load_coll(collection)

    print("What do you want to do?")
    print("1.- One-by-one classifier.")
    print("2.- By-word classifier.")
    print("3.- Get the classified tweets")
    print("4.- Get the tweets of this collection")


    cal_option = ask_number(4,1)

    if (cal_option == 1):
        db.calibrate_tweet()
    elif (cal_option == 2):
        aux = 1
        while aux == 1:
            word = input("Give me a word> ")
            db.get_tweets_with_word(word)
            cont = input("Type 1 to continue>")
            aux = int(cont)
    elif (cal_option == 3):
        db.export_csv_user_sentiment()
    elif (cal_option == 4):
        db.export_csv_collection()

