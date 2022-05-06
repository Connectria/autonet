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


class DeviceDriverNotFound(AutonetException):
    """
    Raised when the driver for a device cannot be determined.
    """

    def __init__(self, device_id, backend):
        super().__init__(f"Could not load driver {backend} "
                         f"for device_id: {device_id}")


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
    Raised when the driver for a device determines that a device does not
    support the requested operation.
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


class RequestValueError(AutonetException):
    """
    Raised when invalid data is passed in a request.
    """

    def __init__(self, field, value, valid_values: list = None):
        valid_values = valid_values or []
        msg = f"Invalid value '{value}' for field '{field}'."
        if valid_values:
            msg += f" Valid values are {valid_values}"
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
    Raised when a request for an object could no be completed
    because the driver could not find the object as described.
    """
    def __init__(self):
        super().__init__("Object not found.")
