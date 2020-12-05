import threading
import time

def timerCallBack(iTimeSec,isRepeated):
    print("timerCallBack!")
    if isRepeated == True :
        threading.Timer(iTimeSec,timerCallBack,[iTimeSec,isRepeated]).start()

def startTimer(iTimeSec,isRepeated):
    threading.Timer(iTimeSec,timerCallBack,[iTimeSec,isRepeated]).start()


def main():
    startTimer(3,False)

    while True:
        print("while loop!")
        time.sleep(1)

if __name__ == '__main__':
    main()