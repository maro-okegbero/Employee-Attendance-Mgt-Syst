from datetime import datetime


def convert_to_json_dict(obj):
    """
    :param obj: object to be converted
    :return: json dict
    """
    obj = obj.to_son().to_dict()
    return obj


def append_timestamp(obj):
    """

    :param obj: object to be updated
    :return: updated object with new timestamp
    """
    arrival_time = datetime.now()
    arrival_day = arrival_time.strftime("%d %B, %Y")

    obj.timestamps.append({'date': arrival_day,
                           'login_time': arrival_time})
    obj.save()

    return obj


def update_timestamp(obj, **kwargs):
    """

    :param obj:
    :return: object with updated timestamp
    """
    departure_time = datetime.now()
    user_timestamps = obj.timestamps
    lastentry_of_user_timestamps = len(user_timestamps) - 1
    if kwargs:
        pov = kwargs.pop("pov")
        user_timestamps[lastentry_of_user_timestamps].update(logout_time=departure_time, purpose_of_visit=pov)
    else:
        user_timestamps[lastentry_of_user_timestamps].update(logout_time=departure_time)

    obj.save()
    return obj
