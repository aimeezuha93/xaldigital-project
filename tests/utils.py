class MockResponse:
    def __init__(self, json_data, status_code, ok=True):
        self.json_data = json_data
        self.status_code = status_code
        self.ok = ok

    def json(self):
        if self.json_data is None:
            raise
        else:
            return self.json_data
