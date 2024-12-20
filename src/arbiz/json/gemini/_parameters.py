from .. import _parameters


def api_tokens() -> list[str]:
    return _parameters.gemini()["api_keys"]
