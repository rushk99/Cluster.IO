# TODO Add comments and more documentation in general for structure of these error messages

"""
A class which contains all of the Exceptions we will use in the project.
"""


class InvalidClusteringMethodError(Exception):
    def __init__(self, method):
        self.method = method
        self.message = "Invalid clustering method"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.method} -> {self.message}'


class InvalidClusteringColumn(Exception):
    def __init__(self, method):
        self.method = method
        self.message = "Invalid clustering column, column not supported"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.method} -> {self.message}'


class InvalidClusteringFileFormat(Exception):
    def __init__(self, method):
        self.method = method
        self.message = "Invalid file format"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.method} -> {self.message}'
