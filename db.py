"""Database."""
import logging
from pprint import pprint

import pymysql.cursors

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

# Connect to the database
try:
    connection = pymysql.connect(read_default_file="credentials.cnf",
                                 db='lunchtron',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
except pymysql.err.OperationalError:
    _LOGGER.error("Invalid Input: Wrong username/database or password.")

# try:
# with connection.cursor() as cursor:
    # Read a single record
    # sql = cursor.execute("SELECT `card_uid`, `uid` FROM `cards`")
    # result = cursor.fetchone()
    # print(result['card_uid'])
# finally:
#     connection.close()


def add_user(name, balance):
    """Create a new User record.

    Arguments:
        name {str} -- full name of the user
        balance {float} -- initial balance for lunch

    Returns:
        int -- user_uid
    """
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`name`, `price`, `balance`) VALUES (%s, %s, %s)"
        _LOGGER.info('adding user %s with balance %d', name, balance)
        cursor.execute(sql, (str(name), float(1.00), float(balance)))
        connection.commit()
        user_uid = cursor.lastrowid
        return user_uid


def add_card(user_uid, card_uid):
    """Create a new Card record.

    Arguments:
        user_uid {int} -- user identifier
        card_uid {hex} -- card identifier
    """
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `cards` (`card_uid`, `uid`) VALUES (%s, %s)"
        _LOGGER.info('adding card %s for user %s', card_uid, user_uid)
        cursor.execute(sql, (int(card_uid, base=16), int(user_uid)))
        connection.commit()


def add_checkin(user_uid):
    """Create a new Checkin record.

    Arguments:
        user_uid {int} -- user identifier
    """
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `checkins` (`uid`) VALUES (%s)"
        _LOGGER.info('registering new checkin for user %s', user_uid)
        cursor.execute(sql, int(user_uid))
        connection.commit()


def query_user(name):
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `users` WHERE `name`=%s"
        cursor.execute(sql, name)
        result = cursor.fetchone()
        pprint(result)
        return result


def query_users():
    _LOGGER.info('Querying all user data')
    with connection.cursor() as cursor:
        # Read all records
        sql = "SELECT * FROM `users`"
        cursor.execute(sql)
        result = cursor.fetchall()
        pprint(result)
        return result


if __name__ == "__main__":
    query_users()
