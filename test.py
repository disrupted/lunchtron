import json
import logging
from time import sleep

import requests

import reader

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

_LOGGER = logging.getLogger(__name__)
_API_URL = 'http://10.1.128.140:5000/api'


def get_user_uid(card_uid):
    # GET Card
    # GET /api/cards/<card_uid>
    try:
        response = requests.get(
            url="{}/cards/{}".format(_API_URL, card_uid),
            headers={
                "Authorization": "Basic ZGlzcnVwdGVkOnNlY3JldA==",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
        try:
            user_uid = response.json()['user_uid']
            return user_uid
        except KeyError as e:
            _LOGGER.error(e)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def get_user(user_uid):
    """Retrieve User"""
    # GET /api/users/<user_uid>
    try:
        response = requests.get(
            url="{}/users/{}".format(_API_URL, user_uid),
            headers={
                "Authorization": "Basic ZGlzcnVwdGVkOnNlY3JldA==",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def create_checkin(user_uid):
    """Create new Checkin."""
    # POST /api/checkins/
    try:
        response = requests.post(
            url=_API_URL + "/checkins/",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "user_uid": str(user_uid)
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# while True:
#     tag_id = reader.read_tag()
#     user = parser.lookup_user(tag_id)

#     if user:
#         print('{} -> {} {}'.format(tag_id, user['u_fname'], user['u_lname']))
#     else:
#         print('User {} not found'.format(tag_id))

#     sleep(3)

while True:
    tag_id = reader.read_tag()
    user_uid = get_user_uid(tag_id)
    print(user_uid)
    user = get_user(user_uid)
    print(user)

    if user:
        print('{} -> {} {}'.format(tag_id, user['name'], user['balance']))
        create_checkin(user_uid)
    else:
        print('User {} not found'.format(tag_id))

    sleep(3)
