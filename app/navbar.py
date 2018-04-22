'''Module for navigation bar'''

from flask import url_for


def build_navbar():
    '''Return navbar according to visibility (is_public)'''

    navbar = [
        {
            'link': url_for('voles.index'),
            'label': 'Hell-Bent VoleS',
            'position': 'main',
            'visibility': 'both',
        },
        {
            'link': url_for('account.login'),
            'label': 'Sign In',
            'position': 'right',
            'visibility': 'public',
        },
        {
            'link': url_for('account.logout'),
            'label': 'Sign Out',
            'position': 'right',
            'visibility': 'private',
        },
    ]

    bar_data_public = [item for item in navbar if
                       (item['visibility'] == 'both') or (
                           item['visibility'] == 'public')]

    bar_public = {
        'main': [item for item in bar_data_public if
                 item['position'] == 'main'],
        'left': [item for item in bar_data_public if
                 item['position'] == 'left'],
        'right': [item for item in bar_data_public if
                  item['position'] == 'right'],
    }

    bar_data_private = [item for item in navbar if
                        (item['visibility'] == 'both') or (
                            item['visibility'] == 'private')]

    bar_private = {
        'main': [item for item in bar_data_private if
                 item['position'] == 'main'],
        'left': [item for item in bar_data_private if
                 item['position'] == 'left'],
        'right': [item for item in bar_data_private if
                  item['position'] == 'right'],
    }

    return dict(navbar={'public': bar_public, 'private': bar_private})
