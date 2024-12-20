from .. import _base

def unignore_chat(chat_id: str) -> None:
    ignored_chats: list[str] = _base.get("avito", "ignored", "chat_ids")
    if chat_id in ignored_chats:
        ignored_chats.remove(chat_id)
        _base.set("avito", "ignored", "chat_ids", value=ignored_chats)


def unignore_user(user_id: int) -> None:
    ignored_users: list[int] = _base.get("avito", "ignored", "user_ids")
    if user_id in ignored_users:
        ignored_users.remove(user_id)
        _base.set("avito", "ignored", "user_ids", value=ignored_users)


def ignore_chat(chat_id: str) -> None:
    ignored_chats: set[str] = set(_base.get("avito", "ignored", "chat_ids"))
    ignored_chats.add(chat_id)
    _base.set("avito", "ignored", "chat_ids", value=list(ignored_chats))


def ignore_user(user_id: int) -> None:
    ignored_users: set[int] = set(_base.get("avito", "ignored", "user_ids"))
    ignored_users.add(user_id)
    _base.set("avito", "ignored", "user_ids", value=list(ignored_users))
