class Error(Exception):
    pass


class PageNotFound(Error):
    pass


class ContentTypeNotFound(Error):
    pass


class ContentTypeNotAccepted(Error):
    def __init__(self, content_type):
        self.content_type = content_type


class RedirectOverSeedRoot(Error):
    def __init__(self, redir_url):
        self.redir_url = redir_url
