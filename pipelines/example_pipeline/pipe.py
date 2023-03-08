from dag import Dag
from task import Task


class ExtractTask(Task):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        print("Running extract task with config: ", self.config)
        

class TransformTask(Task):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        print("Running transform task with config: ", self.config)
        

class LoadTask(Task):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        print("Running load task with config: ", self.config)
        

class ExamplePipeline(Dag):
    def __init__(self):
        super().__init__()
        self.add_task(ExtractTask({'source': 's3://example_bucket/example_data.csv'}))
        self.add_task(TransformTask({'transform': 'standardize'}))
        self.add_task(LoadTask({'target': 's3://example_bucket/example_data.csv'}))

    def run(self):
        super().run()
        
if __name__ == "__main__":
    pipeline = ExamplePipeline()
    pipeline.run()
