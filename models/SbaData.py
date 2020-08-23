class SbaEntry:
    def __init__(self, title, description, modified, accessLevel, identifier, issued,
                 landing_page, license_link, publisher, accrual_periodicity, is_part_of, contact_point,
                 distributions, keywords, bureau_code, program_code, language, themes):
        self.title = title
        self.description = description
        # datetime
        self.modified = modified
        self.accessLevel = accessLevel
        self.identifier = identifier
        # datetime
        self.issued = issued
        self.landingPage = landing_page
        self.license = license_link
        # Publisher object
        self.publisher = publisher
        self.accrualPeriodicity = accrual_periodicity
        self.isPartOf = is_part_of
        # ContactPoint object
        self.contactPoint = contact_point
        # array of Distribution objects
        self.distributions = distributions
        # array of strings
        self.keywords = keywords
        self.bureauCode = bureau_code
        self.programCode = program_code
        # array of strings
        self.languages = language
        # array of strings
        self.theme = themes



class Publisher:
    def __init__(self, name):
        self.name = name


class ContactPoint:
    def __init__(self, fn, has_email):
        self.fn = fn
        self.email = has_email


class Distribution:
    def __init__(self, media_type, title, description, download_url, access_url):
        self.mediaType = media_type
        self.title = title
        self.description = description
        self.downloadUrl = download_url
        self.accessUrl = access_url
