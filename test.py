import performance_analysing

p = performance_analysing.time_analysing()


def start():
    p.set_time_point("Start")


def stop():
    p.set_time_point("stop")


class INT:
    def __init__(self, o):
        self.value = o

    def __add__(self, other):
        return INT(other + self.value)

    def __gt__(self, other):
        return self.value > other

    def __lt__(self, other):
        return self.value < other

    def __str__(self):
        return str(self.value)


def f(x: INT):
    if x > 800: return
    print(x)
    f(x + 1)


start()

for i in range(1000):
    f(INT(0))

stop()

# ohne :INT => 5.690603256225586
# mit :INT =>
