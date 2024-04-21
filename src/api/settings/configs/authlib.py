from api.settings import env

AUTHLIB_OAUTH_CLIENTS = {
    "google": {
        "client_id": env.str("OAUTH2_GOOGLE_CLIENT_ID", default=""),
        "client_secret": env.str("OAUTH2_GOOGLE_CLIENT_SECRET", default=""),
    },
    "github": {
        "client_id": env.str("OAUTH2_GITHUB_CLIENT_ID", default=""),
        "client_secret": env.str("OAUTH2_GITHUB_CLIENT_SECRET", default=""),
    },
    "linkedin": {
        "client_id": env.str("OAUTH2_LINKEDIN_CLIENT_ID", default=""),
        "client_secret": env.str("OAUTH2_LINKEDIN_CLIENT_SECRET", default=""),
    },
}
