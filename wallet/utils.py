from uuid import uuid4


def get_short_uuid():
    return str(uuid4())[:8]


def get_invite_link(uuid):
    return f"https://t.me/kowelbot?start={uuid}"
