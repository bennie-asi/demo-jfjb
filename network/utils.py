def jointURL(baseURL, date, after=''):
    import urllib.parse as urlparse
    res = urlparse.urljoin(baseURL, date)+'/'
    # print(res)
    if after:
        res = urlparse.urljoin(res, after)
    return res
