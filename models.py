import requests
import sys


class Connection:
    def __init__(self, **kwargs):
        self.url_json = kwargs['url_json']

        self.user_password = kwargs['user_password']
        if not self.user_password is None:
            self.user, self.password = self.user_password.split(":")

        self.web_hook_token = kwargs['web_hook_token']

    def get_response(self):
        try:
            if self.user_password is None:
                response = requests.get(self.url_json)
            else:
                response = requests.get(self.url_json, auth=(self.user, self.password))
            return response
        except:
            print("get_response except: " + sys.exc_info()[0])

    def get_content(self):
        return self.get_response().content

    def get_json(self):
        try:
            return self.get_response().json()
        except:
            print(self.get_content())
            return None
