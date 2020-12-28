from datetime import datetime


class User:
    __username: str
    __last_login: datetime
    __key: int

    def __init__(self, username: str, last_login: datetime, key: int):
        self.__username = username
        self.__last_login = last_login
        self.__key = key

    def get_login_str(self) -> str:
        """Generates the message that is displayed when the user is logged in"""
        login_str = ""

        time_since_last_login = (datetime.now() - self.__last_login)

        time_since_last_login_str = str(time_since_last_login.days) + \
                                    " days and " + str(
            round(time_since_last_login.seconds / 3600)) + \
                                    " hours ago"

        login_str += "Welcome back " + self.__username + "\n" + \
                     "Your last login was at: " + \
                     str(self.__last_login.strftime("%b %d %Y at %I:%M%p")) + \
                     ", approximately " + time_since_last_login_str + "."

        return login_str

    @staticmethod
    def str_to_date(input_str: str) -> datetime:
        date = datetime.strptime(input_str, '%Y-%m-%d %H:%M:%S')
        return date

    @staticmethod
    def date_to_str(input_date: datetime) -> str:
        return input_date.strftime('%Y-%m-%d %H:%M:%S')

    def get_username(self) -> str:
        """Returns this user's username"""
        return self.__username

    def get_key(self):
        """Returns this user's key"""
        return self.__key
