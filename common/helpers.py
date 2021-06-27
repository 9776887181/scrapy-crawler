from urllib import parse

def url_params(url):
    params = parse.parse_qs(parse.urlparse(url).query)
    params = {k: v[0] for k, v in params.items()}
    return params

