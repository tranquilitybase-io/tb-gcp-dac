# define Python user-defined exceptions
class DacError(Exception):

    """Exception raised for errors in DAC.

    Attributes:
        message -- explanation of the error
    """
    message: str


class DacValidationError(DacError):

    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
    """
    expression: str

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class DacTerraformError(DacError):

    """Exception raised for errors in terraform scripts.
    """

    def __init__(self, message):
        self.message = message
