# OUT SOURCES EXCEPTIONS
class ApiNinjaUnreachable(Exception):
    pass


class ApiNinjaCantFindName(Exception):
    pass


# RESOURCES EXCEPTIONS
class DishNotFound(Exception):
    pass


class ResourceNotFound(Exception):
    pass


class ResourceAlreadyExists(Exception):
    pass


# HELPERS EXCEPTIONS
class InvalidBodyParameter(Exception):
    pass


class MissingBodyParameter(Exception):
    pass
