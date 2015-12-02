class DataExtractionError(Exception):
    def __init__(self, message, errors):

        # Call the Exception base class's constructor
        super(DataExtractionError, self).__init__(message)

        # Errors that we might have
        self.errors = errors