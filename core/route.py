

class Router:

    def __init__(self, method, title, path, controller):
        self.title = title
        self.method = method
        self.path = path
        self.controller = controller
