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


def get_card(card_uid):
    # GET Card
    # GET /api/cards/<card_uid>
    try:
        response = requests.get(
            url="{}/cards/{}".format(_API_URL, card_uid),
            headers={
                "Authorization": "Basic ZGlzcnVwdGVkOnNlY3JldA==",
            },
        )
        _LOGGER.debug('Response HTTP Status Code: %s', response.status_code)
        _LOGGER.debug('Response HTTP Response Body: %s', response.content)
        user = response.json()
        return user
    except TypeError as e:
        _LOGGER.error(e)
    except KeyError as e:
        _LOGGER.error(e)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def get_user(user_uid):
    """Retrieve User."""
    # GET /api/users/<user_uid>
    try:
        response = requests.get(
            url="{}/users/{}".format(_API_URL, user_uid),
            headers={
                "Authorization": "Basic ZGlzcnVwdGVkOnNlY3JldA==",
            },
        )
        _LOGGER.debug('Response HTTP Status Code: %s', response.status_code)
        _LOGGER.debug('Response HTTP Response Body: %s', response.content)
        return response.json()
    except TypeError as e:
        _LOGGER.error(e)
    except KeyError as e:
        _LOGGER.error(e)
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
        _LOGGER.debug('Response HTTP Status Code: %s', response.status_code)
        _LOGGER.debug('Response HTTP Response Body: %s', response.content)
        _LOGGER.info('Created checkin')
        return response.json()
    except TypeError as e:
        _LOGGER.error(e)
    except KeyError as e:
        _LOGGER.error(e)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


while True:
    print('Waiting for Card...')
    tag_id = reader.read_tag()
    card = get_card(tag_id)
    if 'user_uid' in card:
        user_uid = card['user_uid']
        _LOGGER.info('User ID: %d', user_uid)
        user = get_user(user_uid)

        _LOGGER.info('user for tag_id %s - %s', tag_id, user)
        if user:
            create_checkin(user['id'])
    else:
        _LOGGER.error('No user found for tag_id %s', tag_id)

    sleep(2)
