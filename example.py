import typing


# ******************** Classes *********************

class Externalurls2(typing.TypedDict):
    spotify: str


class Externalurls1(typing.TypedDict):
    spotify: str


class Artists0(typing.TypedDict):
    external_urls: Externalurls1
    href: str
    id: str
    name: str
    type: str
    uri: str


class Items(typing.TypedDict):
    artists: typing.List[Artists0]
    available_markets: typing.List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: Externalurls2
    href: str
    id: str
    is_local: bool
    name: str
    preview_url: str
    track_number: int
    type: str
    uri: str


class Tracks(typing.TypedDict):
    href: str
    items: typing.List[Items]
    limit: int
    next: None
    offset: int
    previous: None
    total: int


class Images(typing.TypedDict):
    height: int
    url: str
    width: int


class Externalurls0(typing.TypedDict):
    spotify: str


class ExternalIds(typing.TypedDict):
    upc: str


class Copyrights(typing.TypedDict):
    text: str
    type: str


class ExternalUrls(typing.TypedDict):
    spotify: str


class Artists(typing.TypedDict):
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class Albums(typing.TypedDict):
    album_type: str
    artists: typing.List[Artists]
    available_markets: typing.List[str]
    copyrights: typing.List[Copyrights]
    external_ids: ExternalIds
    external_urls: Externalurls0
    genres: typing.List[None]
    href: str
    id: str
    images: typing.List[Images]
    label: str
    name: str
    popularity: int
    release_date: str
    release_date_precision: str
    total_tracks: int
    tracks: Tracks
    type: str
    uri: str


class GenericDict(typing.TypedDict):
    albums: typing.List[Albums]


# --------------------------------------------------
