"""
All host permissions.
"""


HOST_PERMISSIONS = {
    "Ask to download": {
        "type": "bool",
        "explaination": "Turning this on will prevent the other side from downloading the file unless you accept it.",
        "default": True
    },
    "Post-download message": {
        "type": "string",
        "explaination": "Do NOT write any sensitive information. The message can be accessed by anyone having your hosting link.",
        "default": "Thanks for downloading!"
    }
}