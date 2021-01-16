import typing


# ******************** Classes *********************

class ExternalUrls(typing.TypedDict):
    spotify: str


class Artists(typing.TypedDict):
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class Copyrights(typing.TypedDict):
    text: str
    type: str


class ExternalIds(typing.TypedDict):
    upc: str


class Images(typing.TypedDict):
    height: int
    url: str
    width: int


class Tracks(typing.TypedDict):
    href: str
    items: typing.List[Artists]
    limit: int
    next: None
    offset: int
    previous: None
    total: int


class GenericDict(typing.TypedDict):
    albums: typing.List[Artists]


# --------------------------------------------------
