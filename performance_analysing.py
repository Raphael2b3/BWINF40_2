import time


class time_analysing:
    start = 0
    delta = 0
    lastmessage = "Starting"

    def __init__(self):
        self.delta = self.start = time.time()

    def set_time_point(self, message):
        currenttime = time.time()
        fromstart = currenttime - self.start
        fromlastpoint = currenttime - self.delta
        print(message, "Currenttime:", fromstart, "since last check:", fromlastpoint)
        self.delta = currenttime
        self.lastmessage = message
