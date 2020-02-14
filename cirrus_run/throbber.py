'''
Show progress in terminal
'''


from threading import Thread
from time import sleep


class ProgressBar:
    '''Simple progress indicator for long running CLI task'''

    def __init__(self, char='.', step=1, break_line=60):
        self.char = char
        self.step = step
        self.break_line = break_line
        self.exit = False
        self.thread = Thread(target=self.show)

    def __enter__(self):
        if self.char:
            self.thread.start()

    def __exit__(self, *a, **ka):
        self.exit = True
        if self.char:
            self.thread.join()

    def show(self):
        cutoff = int(self.break_line / self.step)
        ticks = 0
        exit = False
        while not exit:
            exit = self.exit
            end = ''
            if exit:
                end = '\n'
            ticks += 1
            if ticks == cutoff:
                ticks = 0
                end = '\n'
            self.tick(end)
            if not exit:
                sleep(self.step)

    def tick(self, end=''):
        print(self.char, end=end, flush=True)

