class Error(Exception):
    pass


class PageNotFound(Error):
    pass


class DatabaseConfigNotFound(Error):
    pass


class ContentTypeNotFound(Error):
    pass
