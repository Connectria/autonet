class AutonetException(Exception):
    """
    A passthrough of the `Exception` class.  Classes that inherit from this
    class will be displayed in error messages even without debugging turned
    on.
    """

    def __init__(self, *args):
        super().__init__(*args)


class DeviceNotFound(AutonetException):
    """
    Raised when a device cannot be found in the backend database.
    """

    def __init__(self, device_id, backend):
        super().__init__(f"Could not find device_id: {device_id} in backend {backend}")


class DeviceCredentialsNotFound(AutonetException):
    """
    Raised when a device's credentials cannot be found in the backend database.
    """

    def __init__(self, device_id, backend):
        super().__init__(f"Could not find credentials for "
                         f"device_id: {device_id} in backend: {backend}")


class DeviceDriverNotDefined(AutonetException):
    """
    Raised when the driver for a device cannot be determined.
    """

    def __init__(self, device_id, backend):
        super().__init__(f"Could not retrieve driver information for "
                         f"device_id: {device_id} from backend: {backend}")


class DriverNotFound(AutonetException):
    """
    Raised when a driver could not be loaded.
    """

    def __init__(self, driver_name):
        super().__init__(f"Could not load driver {driver_name}")


class DriverLoadError(AutonetException):
    """
    Raised when a driver module fails to import.
    """

    def __init__(self, driver_name, message):
        super().__init__(f"Failed to import driver {driver_name}.  Module "
                         f"load failed with message: {message}")


class DeviceOperationUnsupported(AutonetException):
    """
    Raised when the driver for a device determines that a device does not
    support the requested operation.
    """

    def __init__(self, driver, operation, device_id):
        super().__init__(f"Device driver {driver} cannot execute {operation} "
                         f"on device_id: {device_id}.")


class DriverOperationUnsupported(AutonetException):
    """
    Raised when the driver for a device does not support the requested operation.
    """

    def __init__(self, driver, operation):
        super().__init__(f"Device driver {driver} does not support {operation}")


class DriverResponseInvalid(AutonetException):
    """
    Raised when a device driver returns a value that was unexpected or
    incorrectly formatted.
    """

    def __init__(self, driver):
        super().__init__(f"Device driver {driver} did not supply a "
                         f"properly formatted reponse.")


class DriverRequestError(AutonetException):
    """
    Raised by a driver when an otherwise well-formed request cannot be
    fulfilled due to platform limitations.
    """
    def __init__(self, msg=None):
        msg = msg or 'The driver cannot perform this request as presented' \
                     'due to platform specific limitations.'
        super().__init__(msg)


class RequestValueError(AutonetException):
    """
    Raised when invalid data is passed in a request.
    """

    def __init__(self, field, value, valid_values: list = None):
        msg = f"Invalid value '{value}' for field '{field}'."
        if valid_values:
            msg += f" Valid values are {valid_values}"
        super().__init__(msg)


class RequestValueMissing(AutonetException):
    """
    Raised when a request is sent without the required data.
    """

    def __init__(self, field: str, valid_values: list = None):
        valid_part = f" to one of these values {valid_values}"
        msg = f"Missing field '{field}'.  Try resending the request " \
              f"with {field} set{valid_part}."
        super().__init__(msg)


class RequestTypeError(AutonetException):
    """
    Raised when data in a field is of the wrong type.
    """

    def __init__(self, field, value, data_type, valid_types: tuple = None):
        valid_types = valid_types or ()
        msg = f"Value '{value}' for field '{field}' is not the correct type: {data_type}."
        if valid_types:
            msg += f" Valid types are {valid_types}"
        super().__init__(msg)


class ObjectNotFound(AutonetException):
    """
    Raised when a request for an object could not be completed
    because the driver could not find the object as described.
    """

    def __init__(self):
        super().__init__("Object not found.")


class ObjectExists(AutonetException):
    """
    Raised when a create requests attempts to create an object that
    already exists.
    """

    def __init__(self, name: str = None):
        super().__init__(f"Object {name + ' ' if name else ''}already exists.")
