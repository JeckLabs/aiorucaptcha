class ResultObject:

    def __init__(self, code, task_id):
        self.code = code
        self.task_id = task_id

    def __str__(self):
        return self.code
