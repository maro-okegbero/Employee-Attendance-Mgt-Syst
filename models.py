from typing import Any, Union

from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from pymodm.connection import connect

connect("mongodb://localhost:27017/myDatabase")


class Employee(MongoModel):
    email = fields.EmailField(primary_key=True)
    first_name = fields.CharField()
    last_name = fields.CharField()
    role = fields.CharField()
    password = fields.CharField()
    timestamps = fields.ListField()

    @property
    def stats(self):
        """this will return the quick stats about an employees attendance habits"""

        n = len(self.timestamps)
        inhsH = 0
        inhsM = 0
        inhsS = 0
        outhsH = 0
        outhsM = 0
        outhsS = 0
        for time in self.timestamps:
            login_times = time['login_time']#
            hs = login_times.time()
            inhsH += hs.hour
            hsHA = inhsH//n
            inhsM += hs.minute
            hsMA = inhsM//n
            inhsS += hs.second
            hsSA = inhsS//n

            logout_times = time['logout_time']  #
            ouths = logout_times.time()
            outhsH += ouths.hour
            outhsHA = outhsH // n
            outhsM += ouths.minute
            outhsMA = outhsM // n
            outhsS += ouths.second
            outhsSA = outhsS // n

        Average_login = str(hsHA) + ':' + str(hsMA) + ':' + str(hsSA)
        Average_logout = str(outhsHA) + ':' + str(outhsMA) + ':' + str(outhsSA)
        statistics = {'Average login_time': Average_login, 'Average logout_time' : Average_logout}
        return statistics





class TimeStamp(MongoModel):
    employee = fields.ReferenceField(Employee)
    date = fields.CharField(primary_key=True)
    login_time = fields.DateTimeField()
    logout_time = fields.DateTimeField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + ' - ' + self.role

    class Meta:
        write_concern = WriteConcern(j=True)

        connection_alias = 'AppMi'
