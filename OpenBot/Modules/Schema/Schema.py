class Schema:

    def __str__(self):
        return self.name

    def __init__(self):
        self.name = 'None'
        self.options = {}
        self.schema_options = {}
        self.requirements = {}
        self.stages = {}