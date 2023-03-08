class Task():
    
    def __init__(self, config):
        self.config = config

    def run(self):
        print("Running task with config: ", self.config)