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

        print("Reaching Point:", message)
        print("It took:", fromstart, "sec")
        print("It took from lastpoint:", fromlastpoint, f"sec. LP({self.lastmessage})")
        self.delta = currenttime
        self.lastmessage = message