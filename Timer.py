import threading


class Timer:

    def __init__(self,sample_time):
        self.sample_time = sample_time

    def start(self, callback_function,*args):
        callback_function(*args)
        threading.Timer(self.sample_time, self.start, [callback_function,*args]).start()

