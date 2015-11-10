import time

working = 1

start_time = time.time()
print (start_time)
time.sleep(30)

print (time.time() - start_time)


while working == 1:
    print ("What do you want to do? \n\t 1. Calibrate the model. \n\t 2. Get new tweets.")
    decision = input(">")

    if(decision == "1"):
        print ("Launching calibration module.")
        working = 0
    elif (decision == "2"):
        print ("Launching Twitter Streaming")
        working =
    else:
        print ("Press 1 or 2 to select an option")
