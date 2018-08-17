import logging
from pprint import pprint
from random import randint

import db
import xml_parser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

data = xml_parser.parse()

for user in data:
    try:
        name = ' '.join([user['u_fname'], user['u_lname']])
        balance = randint(0, 9)
        user_uid = db.add_user(name, balance)
        card_uid = user['u_number']
        db.add_card(user_uid, card_uid)
    except KeyError as e:
        pprint(user)
        raise e
