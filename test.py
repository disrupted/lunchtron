from time import sleep
import reader
import parser

while True:
    tag_id = reader.read_tag()
    user = parser.lookup_user(tag_id)

    if user:
        print('{} -> {} {}'.format(tag_id, user['u_fname'], user['u_lname']))
    else:
        print('User {} not found'.format(tag_id))

    sleep(3)
