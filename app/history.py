import json
import os

FILE = "data/history.json"


class History:

    def __init__(self):

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(FILE):

            with open(FILE, "w") as f:

                json.dump([], f)

    def load(self):

        with open(FILE, "r", encoding="utf8") as f:

            return json.load(f)

    def save(self, data):

        with open(FILE, "w", encoding="utf8") as f:

            json.dump(data, f, indent=4)

    def exists(self, link):

        return link in self.load()

    def add(self, link):

        data = self.load()

        data.append(link)

        data = data[-500:]

        self.save(data)
