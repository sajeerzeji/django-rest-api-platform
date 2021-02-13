import jwt


class JWTUtils:
    @staticmethod
    def encode(payload, key="dTHCAfWq3qXUtgDIGQNp8OPQFuB1YnwI"):
        return jwt.encode(payload, key)

    @staticmethod
    def decode(string, key="dTHCAfWq3qXUtgDIGQNp8OPQFuB1YnwI", verify=False):
        return jwt.decode(string, key, algorithm="HS256", verify=verify)

    @staticmethod
    def encode_access_token(payload):
        return jwt.encode(payload, "dTHCAfWq3qXUtgDIGQNp8OPQFuB1YnwI", "HS256").decode("utf-8")

    @staticmethod
    def encode_refresh_token(payload):
        return jwt.encode(payload, "dTHCAfWq3qXUtgDIGQNp8OPQFuB1YnwI", "HS256").decode("utf-8")

    @staticmethod
    def decode_access_token(token, verify=False):
        if "Bearer" in token:
            token = token.replace("Bearer ", "")
            token = token.strip()
        return jwt.decode(token, "0VYVGEHMlXDDsdKloKKyHVr8e5slQd7r", algorithm="HS256", verify=verify)

    @staticmethod
    def decode_refresh_token(token, verify=False):
        return jwt.decode(token, "0VYVGEHMlXDDsdKloKKyHVr8e5slQd7r", algorithm="HS256", verify=verify)
