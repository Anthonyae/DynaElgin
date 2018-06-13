from sqlalchemy import inspect
import datetime
import time


# Calculate elapsed time, return as hours:minutes:seconds
def elapsed_time(start_time, end_time):
    ''' Caluculate elapsed time between two different datetimes
        Returns the time difference as a string in hours:minutes:seconds. '''
    delta = end_time-start_time
    s = delta.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{}:{}:{}".format(hours, minutes, seconds)


def query_to_list(query, include_field_names=True):
    """Turns a SQLAlchemy query into a list of data values."""
    column_names = []
    for i, obj in enumerate(query.all()):
        if i == 0:
            column_names = [c.name for c in obj.__table__.columns]
            if include_field_names:
                yield column_names
        yield obj_to_list(obj, column_names)


def obj_to_list(sa_obj, field_order):
    """Takes a SQLAlchemy object - returns a list of all its data"""
    return [getattr(sa_obj, field_name, None) for field_name in field_order]


def to_dict(model_instance, query_instance=None):
    if hasattr(model_instance, '__table__'):
        return {c.name: str(getattr(model_instance, c.name)) for c in model_instance.__table__.columns}
    else:
        cols = query_instance.column_descriptions
        return { cols[i]['name'] : model_instance[i]  for i in range(len(cols)) }


class String_time():
    """Takes a timedelta string representation. hours:minutes:seconds and after calling a method will turn the string into a int of total seconds"""
    def __init__(self, time_string):
        '''initialize time'''
        self.time = time_string.split(":")

    def string_seconds(self):
        hours = int(int(self.time[0]) * 3600)
        minutes = int(int(self.time[1]) * 60)
        seconds = int(self.time[2])
        x = hours + minutes + seconds
        return x

def s_to_string_time(seconds):
    s = seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{}:{}:{}".format(hours, minutes, seconds)