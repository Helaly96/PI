import threading


class Timer:

    def __init__(self, callback_function,arguments,sample_time):
        self.sample_time = sample_time
        self.register(callback_function, arguments)

    def register(self, callback_function,arguments):
        callback_function(arguments)
        threading.Timer(self.sample_time, self.register, [callback_function,arguments]).start()
