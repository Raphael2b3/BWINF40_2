from builtins import print as _print


class safeOutputToFile:
    outputstr = ""

    def start_listen(self):
        self.outputstr = ""

    def safe_to_file(self, filename):
        try:
            file = open(filename, "x")
            file.write(self.outputstr)
            file.close()
        except:
            file = open(filename, "w")
            file.write(self.outputstr)
            file.close()

    def print(self, *argumente, end="\n"):
        for arg in argumente:
            self.outputstr += str(arg) + (" " if len(argumente) != 0 else "")
        self.outputstr += end
        _print(*argumente, end=end)


def print(*argumente, end="\n"):
    __safing_instance.print(*argumente, end=end)


def OUTPUT_SAFER_start_listening():
    __safing_instance.start_listen()


def OUTPUT_SAFER_safe_to_file(filename):
    __safing_instance.safe_to_file(filename)


__safing_instance = safeOutputToFile()
