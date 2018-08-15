from pprint import pprint
import xmltodict

XML_PATH = 'resources/keycards.xml'


def parse():
    with open(XML_PATH, 'r', encoding='utf-8') as f:
        xml = f.read()
    data = xmltodict.parse(xml)['users']['user']
    return data


def lookup_user(tag_id):
    data = parse()
    for user in data:
        if tag_id.upper() == user['u_number']:
            return user


if __name__ == '__main__':
    pprint(parse())
