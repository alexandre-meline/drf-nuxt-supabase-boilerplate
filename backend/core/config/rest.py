from __future__ import annotations


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'user.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
    ],
}