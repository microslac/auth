from datetime import timedelta

from api.settings import env

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": env.str("SIMPLE_JWT_ALGORITHM", default="HS256"),
    "VERIFYING_KEY": env.str("SIMPLE_JWT_VERIFYING_KEY", default="", multiline=True),  # public
    "SIGNING_KEY": env.str("SIMPLE_JWT_SIGNING_KEY", default="", multiline=True),  # secret
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "aid",
    "TOKEN_TYPE_CLAIM": "swt",
}
