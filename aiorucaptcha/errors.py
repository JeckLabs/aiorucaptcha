
__all__ = ('TimeoutError', 'HttpError', 'GeneralApiError',
        'WrongUserKeyError', 'KeyDoesNotExistError', 'ZeroBalanceError',
        'NoSlotAvailableError', 'ZeroCaptchaFilesizeError',
        'TooBigCaptchaFilesizeError', 'WrongFileExtensionError',
        'ImageTypeNotSupportedError', 'IpNotAllowedError', 'IpBannedError',
        'TooBigCaptchaFilesizeError', 'NoSlotAvailableError',
        'WrongIdFormatError', 'CaptchaUnsolvableError', 'WrongCaptchaIdError',
        'BadDuplicatesError', 'NotRecordedError', 'WrongIdFormatError',
        'CaptchaUnsolvableError', 'WrongCaptchaIdError', 'BadDuplicatesError',
        'ReportNotRecordedError')

class TimeoutError(Exception):
    pass

class HttpError(Exception):
    pass

class GeneralApiError(Exception):
    pass

class WrongUserKeyError(GeneralApiError):
    pass

class KeyDoesNotExistError(WrongUserKeyError):
    pass

class ZeroBalanceError(GeneralApiError):
    pass

class NoSlotAvailableError(GeneralApiError):
    pass

class ZeroCaptchaFilesizeError(GeneralApiError):
    pass

class TooBigCaptchaFilesizeError(GeneralApiError):
    pass

class WrongFileExtensionError(GeneralApiError):
    pass

class ImageTypeNotSupportedError(GeneralApiError):
    pass

class IpNotAllowedError(GeneralApiError):
    pass

class IpBannedError(GeneralApiError):
    pass

class TooBigCaptchaFilesizeError(GeneralApiError):
    pass

class NoSlotAvailableError(GeneralApiError):
    pass

class WrongIdFormatError(GeneralApiError):
    pass

class CaptchaUnsolvableError(GeneralApiError):
    pass

class WrongCaptchaIdError(GeneralApiError):
    pass

class BadDuplicatesError(GeneralApiError):
    pass

class NotRecordedError(GeneralApiError):
    pass

class WrongIdFormatError(GeneralApiError):
    pass

class CaptchaUnsolvableError(GeneralApiError):
    pass

class WrongCaptchaIdError(GeneralApiError):
    pass

class BadDuplicatesError(GeneralApiError):
    pass

class ReportNotRecordedError(GeneralApiError):
    pass
