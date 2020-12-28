from datetime import datetime, timezone


class UserInfo:
    name: str
    last_login: datetime

    def __init__(self, user_info: str):
        # string format username|last login (yyyy.mm.dd.hh.mm.ss)
        temp_login_str = ""
        self.name = ""

        mode = 0
        for char in user_info:
            if char == "|":
                mode = 1
            elif mode == 0:
                self.name += char
            else:
                temp_login_str += char

        self.last_login = self.str_to_date(temp_login_str)

    def get_login_str(self) -> str:
        login_str = ""

        time_since_last_login = (datetime.now() - self.last_login)

        time_since_last_login_str = str(time_since_last_login.days) + \
        " days and " + str(round(time_since_last_login.seconds / 3600)) + \
        " hours ago"

        login_str += "Welcome back " + self.name + "\n" + \
                     "Your last login was at: " + \
                     str(self.last_login.strftime("%b %d %Y at %I:%M%p")) + \
                     ", approximately " + time_since_last_login_str + "."

        return login_str

    def str_to_date(self, input_str: str) -> datetime:
        date = datetime.strptime(input_str, '%Y-%m-%d %H:%M:%S')
        return self.utc_to_local(date)

    def date_to_str(self, input_date: datetime) -> str:
        return str(input_date)

    def utc_to_local(self, utc_dt: datetime):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
