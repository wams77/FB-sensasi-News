import json
from pathlib import Path

FILE = Path("data/history.json")


class History:

    def __init__(self):

        FILE.parent.mkdir(exist_ok=True)

        if not FILE.exists():
            FILE.write_text("[]", encoding="utf-8")

    def load(self):

        return json.loads(

            FILE.read_text(

                encoding="utf-8"

            )

        )

    def save(self, data):

        FILE.write_text(

            json.dumps(

                data,

                indent=2,

                ensure_ascii=False

            ),

            encoding="utf-8"

        )

    def exists(self, url):

        return url in self.load()

    def add(self, url):

        history = self.load()

        history.append(url)

        history = history[-1000:]

        self.save(history)
