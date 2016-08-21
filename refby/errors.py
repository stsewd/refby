class PrivateOrInvalidProfileError(Exception):
    def __init__(self, user):
        Exception.__init__(self, "User profile " + "'" + user + "'" + " is private or doesn't exist.")


class UserIdNotFoundError(Exception):
    def __init__(self):
        Exception.__init__(self, "User id not found.")


class OutputDirectoryError(Exception):
    def __init__(self, output):
        Exception.__init__(self, "Output directory doesn't exists: " + output)
