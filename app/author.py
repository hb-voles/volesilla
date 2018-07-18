"""Authorization functions"""


def get_rights_name(group, permission):
    """Get rights name"""

    return 'rights_{}_{}'.format(group, permission)


def get_role_name(role):
    """Get role name"""

    return 'role_{}'.format(role)
