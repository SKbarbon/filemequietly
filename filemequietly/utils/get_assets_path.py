import os



def get_assets_path ():
    """returns the full path of the assets dir"""
    assets_path = os.path.dirname(__file__)
    assets_path = os.path.dirname(assets_path)
    assets_path = os.path.join(assets_path, "assets")
    return assets_path


def get_asset_in_github_link (*paths):
    """Pass path names to get a link to the assets located in GitHub in FileMeQuietly repo."""

    base_url = "https://raw.githubusercontent.com/SKbarbon/filemequietly/main/filemequietly/assets"

    for p in paths:
        base_url = f"{base_url}/{p}"

    return base_url
