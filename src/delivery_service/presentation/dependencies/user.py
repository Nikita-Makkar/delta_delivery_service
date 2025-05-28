from fastapi import Request


def get_user_id_from_cookie(request: Request) -> str | None:
    """
    Returns user_id from cookies.
    """
    return request.cookies.get("user_id")
