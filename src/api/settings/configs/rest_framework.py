REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["auth_.auth.authentication.JWTAuthentication"],
    # "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "EXCEPTION_HANDLER": "micro.jango.exceptions.handler.exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "micro.jango.renderers.ResponseRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ],
}
