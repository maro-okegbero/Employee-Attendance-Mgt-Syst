import inspect
import jwt
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields, EmbeddedMongoModel
from pymodm.connection import connect
from sendbox_core.base.utils import convert_dict

connect("mongodb://localhost:27017/myDatabase")


class AppMixin:
    """ App mixin will hold special methods and field parameters to map to all model classes"""

    def to_dict(self):
        if isinstance(self, (MongoModel, EmbeddedMongoModel)):
            return self.to_son().to_dict()
        return self._dict_

    def to_full_dict(self):
        """
        Retrieve all values of this model as a dictionary including values of methods that are
        wrapped with the @property decorator
        """
        data = inspect.getmembers(self)
        data_ = dict()
        for d in data:
            if not inspect.ismethod(d[1]) and '__' not in d[0] \
                    and type(d[1]) in [str, int, dict, list, float, datetime, ObjectId, unicode, tuple] \
                    or isinstance(d[1], (MongoModel, EmbeddedMongoModel)):

                data_[d[0]] = d[1]
                if type(d[1]) == ObjectId:
                    data_[d[0]] = str(d[1])
                if isinstance(d[1], (MongoModel, EmbeddedMongoModel)) and getattr(d[1], 'to_son', None):
                    data_[d[0]] = d[1].to_son().to_dict()
                #     for k,v in data_[d[0]].items():
                #         print k, v, type(v)
                #         if type(v) == list:
                #             for c in v:
                #                 if isinstance(c, (MongoModel, EmbeddedMongoModel)):
                #                     data_[d[0]][k].append(c.to_son().to_dict())
                if type(d[1]) in [list, tuple] and len(d[1]) > 0:
                    sub = []
                    for i in d[1]:
                        if getattr(i, 'to_son', None):
                            sub.append(i.to_son().to_dict())
                    data_[d[0]] = sub
                    #     print (i)

        # pprint(data_)
        return data_

    def to_full_json(self):
        """
        Retrieve all values of this model as a dictionary including values of methods that are
        wrapped with the @property decorator
        """
        data_ = self.to_full_dict()
        if data_.has_key("_defaults"):
            data_.pop("_defaults")
        data_ = convert_dict(data_)
        return data_


class User(MongoModel, AppMixin):
    email = fields.EmailField()
    firstname = fields.CharField(required=True)
    lastname = fields.CharField(required=True)
    phonenumber = fields.CharField(required=True, max_length=17)
    address = fields.CharField(required=True)
    employee = fields.BooleanField(required=True)
    role = fields.CharField(required=False, blank=True)
    password = fields.CharField(blank=True)
    timestamps = fields.ListField()
    date_created = fields.DateTimeField()
    last_updated = fields.DateTimeField()
    auth = fields.CharField(required=False, blank=True)
    admin = fields.BooleanField(required=False)

    def created(self):
        self.date_created = datetime.utcnow()
        self.save()

    def set_auth(self):
        profiles = [dict(id=str(self.pk), domain='employee_attendance_mgt_syst', perm=[])]

        payload = dict(uid=str(self.pk), username=self.firstname, admin=self.admin,
                       email=self.email, phone=self.phonenumber, profiles=profiles,
                        aud=['employee_attendance_mgt_syst'])

        token = jwt.encode(payload=payload, key='123456')

        self.auth = token

        self.save()

    @property
    def stats(self):
        """

        :return: A report of a user's average login and logout time
        """

        n = len(self.timestamps)
        login_hours = 0
        login_minutes = 0
        login_seconds = 0
        logout_hours = 0
        logout_minutes = 0
        logout_seconds = 0
        for time in self.timestamps:
            # Get Login time in H:M:S format
            login_times = time.get('login_time')
            login_hour_second_minute = login_times.time()
            # login average hours
            login_hours += login_hour_second_minute.hour
            login_hours_average = login_hours // n
            # login average minutes
            login_minutes += login_hour_second_minute.minute
            login_minutes_average = login_minutes // n
            # login average seconds
            login_seconds += login_hour_second_minute.second
            login_seconds_average = login_seconds // n

            # Get Logout time in H:M:S format
            logout_times = time.get('logout_time')
            logout_hour_second_minute = logout_times.time()
            # Logout average hour
            logout_hours += logout_hour_second_minute.hour
            logout_hours_average = logout_hours // n
            # Logout average minutes
            logout_minutes += logout_hour_second_minute.minute
            logout_minutes_average = logout_minutes // n
            # Logout average seconds
            logout_seconds += logout_hour_second_minute.second
            logout_seconds_average = logout_seconds // n

        average_login = '{0}:{1}:{2}'.format(str(login_hours_average), str(login_minutes_average),
                                             str(login_seconds_average))
        average_logout = '{0}:{1}:{2}'.format(str(logout_hours_average), str(logout_minutes_average),
                                              str(logout_seconds_average))
        statistics = {'Average login_time': average_login, 'Average logout_time': average_logout}
        return statistics


class TimeStamp(MongoModel, AppMixin):
    user = fields.ReferenceField(User)
    date = fields.CharField(primary_key=True)
    login_time = fields.DateTimeField()
    break_time = fields.CharField()
    logout_time = fields.DateTimeField()
    purpose_of_visit = fields.CharField(default='Work')

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + ' - ' + self.role

    class Meta:
        write_concern = WriteConcern(j=True)

        # connection_alias = 'AppMi'
