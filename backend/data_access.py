# TODO implement data store


def check_cache():
    return False

def get_data_from_cache(website_url):
    try:
        return check_cache()
    except Exception:
        return False