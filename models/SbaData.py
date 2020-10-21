import json
import os
import sys


class SbaData:
    def __init__(self):
        self.root_dir = os.path.dirname(sys.modules['__main__'].__file__)
        self.data_path = self.root_dir + '/json/' + 'sba_data.json'


    def GetRawJson(self):
        with open(self.data_path, encoding='utf8') as f:
            entries_dict = json.load(f)
        return entries_dict
    # returns array of SbaEntry objects
    def ParseJsonData(self):
        entry_list = []
        try:
            print('Parsing sba_data.json...')
            with open(self.data_path, encoding='utf8') as f:
                entries_dict = json.load(f)
            for entry in entries_dict['dataset']:
                # set ContactPoint object
                contact = entry['contactPoint']
                cont_obj = ContactPoint(contact['fn'], contact['hasEmail'])
                # set list of Distribution objects
                distr_obj = []
                distr = entry.get('distribution')
                if distr is not None:
                    for d in distr:
                        distr_obj.append(Distribution(d.get('mediaType'), d.get('title'),
                                                      d.get('description'), d.get('downloadURL'), d.get('accessURL')))
                new_entry = SbaEntry(entry['title'], entry['description'], entry['modified'], entry['accessLevel'], entry['identifier'],
                                     entry.get('issued'), entry.get('landingPage'), entry['license'], Publisher(entry['publisher']['name']),
                                     entry.get('accrualPeriodicity'), entry.get('isPartOf'), cont_obj, distr_obj, entry['keyword'], entry['bureauCode'][0],
                                     entry['programCode'][0], entry.get('language'), entry.get('theme'))
                entry_list.append(new_entry)
            print('Parse complete')
        except Exception as e:
            print(e)
        return entry_list


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
