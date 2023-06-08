from dotenv import load_dotenv
import os
from pprint import pprint
from requests.exceptions import ReadTimeout, ConnectionError
from time import sleep
from dvmn_handlers import get_polling


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('DVMN_API_KEY')
    last_attempt_timestamp = None
    while True:
        try:
            response = get_polling(api_key, last_attempt_timestamp)
            if response["status"] == "timeout":
                last_attempt_timestamp = response["timestamp_to_request"]
            else:
                last_attempt_timestamp = response["last_attempt_timestamp"]
                response = get_polling(api_key, last_attempt_timestamp)
                pprint(response)
        except ReadTimeout:
            print('Polling time eceeded')
        except ConnectionError as err:
            for n in range(3):
                sleep(30)
                if n <= 3:
                    response = get_polling(api_key, last_attempt_timestamp)
                    pprint(response)
                else:
                    print(err)
