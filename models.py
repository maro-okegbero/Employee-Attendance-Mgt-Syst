from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from pymodm.connection import connect

connect("mongodb://localhost:27017/myDatabase")


class User(MongoModel):
    email = fields.EmailField(primary_key=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    phone_number = fields.CharField(required=True, max_length=14)
    address = fields.CharField(required=True)
    employee = fields.BooleanField(default=True)
    role = fields.CharField(required=False, blank=True)
    password = fields.CharField(blank=True)
    timestamps = fields.ListField()

    @property
    def stats(self):
        """this will return the quick stats about an employees attendance habits"""

        global login_hours_average, login_minutes_average, login_seconds_average, logout_minutes_average, logout_hours_average, logout_seconds_average
        n = len(self.timestamps)
        login_hours, login_minutes, login_seconds, logout_hours, logout_minutes, logout_seconds = 0
        for time in self.timestamps:
            login_times = time['login_time']
            login_hour_second_minute = login_times.time()
            login_hours += login_hour_second_minute.hour
            login_hours_average = login_hours // n
            login_minutes += login_hour_second_minute.minute
            login_minutes_average = login_minutes // n
            login_seconds += login_hour_second_minute.second
            login_seconds_average = login_seconds // n
            logout_times = time['logout_time']
            logout_hour_second_minute = logout_times.time()
            logout_hours += logout_hour_second_minute.hour
            logout_hours_average = logout_hours // n
            logout_minutes += logout_hour_second_minute.minute
            logout_minutes_average = logout_minutes // n
            logout_seconds += logout_hour_second_minute.second
            logout_seconds_average = logout_seconds // n

        average_login = str(login_hours_average) + ':' + str(login_minutes_average) + ':' + str(login_seconds_average)
        average_logout = str(logout_hours_average) + ':' + str(logout_minutes_average) + ':' + str \
            (logout_seconds_average)
        statistics = {'Average login_time': average_login, 'average logout_time': average_logout}
        return statistics


class TimeStamp(MongoModel):
    user = fields.ReferenceField(User)
    date = fields.CharField(primary_key=True)
    login_time = fields.DateTimeField()
    logout_time = fields.DateTimeField()
    purpose_of_visit = fields.CharField(default='Work')

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + ' - ' + self.role

    class Meta:
        write_concern = WriteConcern(j=True)

        connection_alias = 'AppMi'
