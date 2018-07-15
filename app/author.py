"""Authorization functions"""


def get_rights_name(group, permission):
    """Get rights name"""

    return 'right_{}_{}'.format(group, permission)
