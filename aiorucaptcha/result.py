class ResultObject:

    def __init__(self, result, task_id):
        self.result = result
        self.task_id = task_id

    def __str__(self):
        return self.result
