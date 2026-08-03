import requests
from config import FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN


class FacebookPublisher:

    def __init__(self):

        self.url = f"https://graph.facebook.com/v23.0/{FACEBOOK_PAGE_ID}/feed"

    def publish(self, message, link=None):

        data = {
            "message": message,
            "access_token": FACEBOOK_ACCESS_TOKEN
        }

        if link:
            data["link"] = link

        r = requests.post(self.url, data=data, timeout=60)

        if r.status_code == 200:

            print("Facebook Post Success")

            return True

        print(r.text)

        return False
