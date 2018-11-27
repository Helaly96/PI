class Observer_Pattern:
    def __init__(self):
        self._eventListeners ={}
    def registerEventListener(self, event_name , listener_update):
        # if new event => value = new list
        if self._eventListeners[event_name] == None:
            self._eventListeners[event_name] = [listener_update]
        # if old event => add the listener to the list
        else:
            self._eventListeners[event_name].append(listener_update)

    def delete_event_listener(self,event_name,listener):
        self._eventListeners[event_name].remove(listener)

    # Check for *args https://www.programiz.com/python-programming/args-and-kwargs
    def emit_Signal(self,*args):
        event_name = args[0]
        for update in self._eventListeners[event_name]:
            update(*args)
