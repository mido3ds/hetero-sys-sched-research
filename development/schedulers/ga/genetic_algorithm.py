import random

class Job:
    def __init__(self, id, burst_time, priority, dependencies=None):
        """
            Initializes the job with the appropriate information
        """
        if not dependencies:
            dependencies = []

        self.id = id
        self.burst_time = burst_time
        self.priority = priority
        self.dependencies = dependencies
        self.min_completion_time = -1

    def is_dependency_of(self, other):
        """
            Returns true if this task is a dependency (direct or indirect) of other
        """
        return (self in other.dependencies) or any(self.is_dependency_of(task) for task in other.dependencies)

    def get_min_completion_time(self):
        """
           Returns the minimum completion time of this task based on the minimum completion times of its dependencies
        """
        if self.min_completion_time < 0:
            self.min_completion_time = self.duration
            if len(self.dependencies) > 0:
                self.min_completion_time += max(
                    [task.get_min_completion_time() for task in self.dependencies])
        return self.min_completion_time

    def __repr__(self):
        """
            Returns the represetation of the job
        """
        return '<Job %s>' % self.identifier


