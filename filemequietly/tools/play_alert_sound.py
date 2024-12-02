import platform, os



def play_alert_sound ():
    os_name = platform.system()

    if os_name == "Darwin":
        os.system('afplay /System/Library/Sounds/Sosumi.aiff')
    elif os_name == "Windows":
        print("\a")
    elif os_name == "Linux":
        print("\a")
    else:
        print("Unknown Operating System.")
