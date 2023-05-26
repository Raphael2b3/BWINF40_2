goal = 10
bar_length = 20


def show_state(current_value):
    # region Prozessbar
    fortschritt = round(current_value/ goal, 2)
    l = int(fortschritt * bar_length)
    a = "#" * l
    b = "_" * int(bar_length - l)
    p = round(fortschritt*100)
    print("\r", f"{p}% [{a + b}]", end="")
