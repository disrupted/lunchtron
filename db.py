# -*- coding=utf-8 -*-
"""Database."""
import logging
from pprint import pprint

import pymysql.cursors
from passlib.hash import sha256_crypt

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

# Connect to the database
try:
    conn = pymysql.connect(read_default_file="credentials.cnf",
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


def add_admin(username, password):
    with conn.cursor() as cursor:
        # Create a new record
        password_hash = sha256_crypt.hash(password)
        sql = "INSERT INTO `admins` (`username`, password_hash`) VALUES (%s, %s)"
        _LOGGER.info('adding new admin %s', username)
        cursor.execute(sql, (username, password_hash))
        conn.commit()
        admin_uid = cursor.lastrowid
        return admin_uid


def add_user(name, balance):
    """Create a new User record.

    Arguments:
        name {str} -- full name of the user
        balance {float} -- initial balance for lunch

    Returns:
        int -- user_uid
    """
    with conn.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`name`, `price`, `balance`) VALUES (%s, %s, %s)"
        _LOGGER.info('adding user %s with balance %d', name, balance)
        cursor.execute(sql, (str(name), float(1.00), float(balance)))
        conn.commit()
        user_uid = cursor.lastrowid
        return user_uid


def add_card(user_uid, card_uid):
    """Create a new Card record.

    Arguments:
        user_uid {int} -- user identifier
        card_uid {str} -- card identifier
    """
    with conn.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `cards` (`card_uid`, `user_uid`) VALUES (%s, %s)"
        _LOGGER.info('adding card %s for user %s', card_uid, user_uid)
        cursor.execute(sql, (card_uid, int(user_uid)))
        conn.commit()


def create_checkin(user_uid):
    """Create a new Checkin record.

    Arguments:
        user_uid {int} -- user identifier
    """
    with conn.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `checkins` (`user_uid`) VALUES (%s)"
        _LOGGER.info('registering new checkin for user %s', user_uid)
        cursor.execute(sql, user_uid)
        conn.commit()
        checkin_uid = cursor.lastrowid
        _LOGGER.debug('checkin created %d', checkin_uid)
        print(checkin_uid)
        return checkin_uid


def update_balance(user_uid, balance_change):
    balance_old = query_user_by_id(user_uid)['balance']
    with conn.cursor() as cursor:
        sql = "UPDATE `users` SET `balance`=`balance`+%s WHERE `user_uid`=%s"
        _LOGGER.info('updating balance for user %s', user_uid)
        cursor.execute(sql, (balance_change, user_uid))
        conn.commit()
        balance_new = query_user_by_id(user_uid)['balance']
        _LOGGER.info('balance updated: {} -> {}'.format(balance_old, balance_new))


def query_user(name):
    with conn.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `users` WHERE `name`=%s"
        cursor.execute(sql, name)
        result = cursor.fetchone()
        pprint(result)
        return result


def query_user_by_id(user_uid):
    with conn.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `users` WHERE `user_uid`=%s"
        cursor.execute(sql, user_uid)
        result = cursor.fetchone()
        pprint(result)
        return result


def query_users():
    _LOGGER.info('Querying all user data')
    with conn.cursor() as cur:
        # Read all records
        sql = "SELECT * FROM `users`"
        cur.execute(sql)
        rv = cur.fetchall()
        pprint(rv)
        return rv


def query_checkins():
    _LOGGER.info('Querying all checkin data')
    with conn.cursor() as cur:
        # Read all records
        sql = "SELECT * FROM `checkins`"
        cur.execute(sql)
        rv = cur.fetchall()
        pprint(rv)
        return rv


def query_checkin_by_id(checkin_uid):
    _LOGGER.info('Querying checkin by id')
    with conn.cursor() as cur:
        sql = "SELECT * FROM `checkins` WHERE `checkin_uid`=%s"
        cur.execute(sql, checkin_uid)
        rv = cur.fetchone()
        pprint(rv)
        return rv


def query_cards():
    _LOGGER.info('Querying all cards data')
    with conn.cursor() as cur:
        # Read all records
        sql = "SELECT * FROM `cards`"
        cur.execute(sql)
        rv = cur.fetchall()
        pprint(rv)
        return rv


def query_card_by_id(card_uid):
    _LOGGER.info('Querying card by id %s', card_uid)
    with conn.cursor() as cur:
        sql = "SELECT * FROM `cards` WHERE `card_uid`=%s"
        cur.execute(sql, card_uid)
        rv = cur.fetchone()
        pprint(rv)
        return rv


def get_password_hash(username):
    _LOGGER.info('Querying password hash for admin %s', username)
    try:
        with conn.cursor() as cur:
            sql = "SELECT `password_hash` FROM `admins` WHERE `username`=%s"
            cur.execute(sql, username)
            return cur.fetchone()['password_hash']
    except TypeError:
        _LOGGER.error('No password_hash found for admin %s', username)


def verify_login(username, password_candidate):
    _LOGGER.debug('Login attempt – username: %s, password candidate: %s',
                  username, password_candidate)
    if username and password_candidate:
        password_hash = get_password_hash(username)
        if password_hash:
            return sha256_crypt.verify(password_candidate, password_hash)
    _LOGGER.warning('AUTHENTICATION FAILED')
    return False


if __name__ == "__main__":
    query_users()
