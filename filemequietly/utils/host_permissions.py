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
    },
    "Play sound on new request": {
        "type": "bool",
        "explaination": "Play a simple notify sound when there is a new request for downloading the file.",
        "default": True
    },
    "Focus window on new request": {
        "type": "bool",
        "explaination": "When there is a new request to download your file, the window will bring itself to the top so you can focus on it and take an action.",
        "default": True
    }
}