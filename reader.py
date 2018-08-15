import logging
from pirc522 import RFID
RDR = RFID()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


def read_tag():
    while True:
        RDR.wait_for_tag()
        (error, tag_type) = RDR.request()
        if not error:
            (error, uid) = RDR.anticoll()
            if not error:
                _LOGGER.info("Tag of type %s detected - UID %s", tag_type, uid)
                # return byte array as hex string (only the first 4 bytes are relevant)
                return bytes(uid[:4]).hex().upper()


def main():
    print(read_tag())
    RDR.cleanup()


if __name__ == '__main__':
    main()
