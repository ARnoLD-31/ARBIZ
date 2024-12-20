from google.api_core.exceptions import InternalServerError, ResourceExhausted

from .. import output


class GeminiException(Exception):
    pass


class Unknown(GeminiException):
    pass


class UnsupportedLocation(GeminiException):
    pass


class Overload(GeminiException):
    pass


class EmptyQueue(GeminiException):
    pass


class ProhibitedContent(GeminiException):
    pass


class NoPrompt(GeminiException):
    pass


def handle(chat_id: str, exception: Exception) -> GeminiException:
    output.warning(chat_id, f'While responding: "{exception}"')
    custom_exception: GeminiException = Unknown(exception)
    if "if the prompts was blocked" in str(exception):
        print(exception)
        custom_exception = ProhibitedContent()
    elif "User location is not supported for the API use" in str(exception):
        custom_exception = UnsupportedLocation(exception)
    elif isinstance(exception, (ResourceExhausted, InternalServerError)):
        custom_exception = Overload(exception)
    return custom_exception
