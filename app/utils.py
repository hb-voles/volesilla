'''Utils module'''

import dateutil.parser


def iso2datetime(iso_date):
    '''Convert ISO datetime format to datetime'''
    return dateutil.parser.parse(iso_date)


def datetime2iso(dt_struct):
    '''Convert datetime to ISO datetime format'''
    return dt_struct.isoformat(timespec='milliseconds')
