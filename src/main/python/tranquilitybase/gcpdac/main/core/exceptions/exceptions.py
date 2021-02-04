# define Python user-defined exceptions
class DacError(Exception):
    message: str


class DacValidationError(DacError):
    expression: str

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class DacTerraformError(DacError):

    def __init__(self, message):
        self.message = message

class DacJenkinsError(DacError):

    def __init__(self, message):
        self.message = message
