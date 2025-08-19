class WorkerNotFound(Exception):

    def __str__(self):
        return "Worker not found"


class WorkerWithNameAlreadyExists(Exception):

    def __str__(self):
        return "The given worker already exists"
