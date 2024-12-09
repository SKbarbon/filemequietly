import os



def get_assets_path ():
    """returns the full path of the assets dir"""
    assets_path = os.path.dirname(__file__)
    assets_path = os.path.dirname(assets_path)
    assets_path = os.path.join(assets_path, "assets")
    return assets_path