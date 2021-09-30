class Schema:

    def __str__(self):
        return self.name + 'Schema'

    def __init__(self):
        self.name = 'None'
        self.options = {}
        self.requirements = {}
        self.stages = {}