from utils.get_assets_path import get_assets_path
import platform, os, flet



def play_alert_sound (page: flet.Page=None):
    """Uses the flet's Audio class to play an alert sound stored in the assets."""
    os_name = platform.system()

    assets_path = get_assets_path()
    alert_file_link = os.path.join(assets_path, "Notification Alert Sound.mp3")
    if not os.path.isfile(alert_file_link):
        print("Alert not exist")

    
    a = flet.Audio(src=alert_file_link, autoplay=True)
    page.overlay.append(a)
    page.update()
    page.overlay.remove(a)