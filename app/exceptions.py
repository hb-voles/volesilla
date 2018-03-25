'''Exceptions'''
from flask import jsonify


def template(data, code=500):
    '''Helper'''
    return {'message': {'errors': {'body': data}}, 'status_code': code}


USER_NOT_FOUND = template(['User not found'], code=404)
USER_ALREADY_REGISTERED = template(['User already registered'], code=422)
UNKNOWN_ERROR = template([], code=500)
ARTICLE_NOT_FOUND = template(['Article not found'], code=404)
COMMENT_NOT_OWNED = template(['Not your article'], code=422)


class InvalidUsage(Exception):
    '''Exception INvalidUsage'''

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        '''Init'''
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        '''Helper'''
        return jsonify(self.message)

    @classmethod
    def user_not_found(cls):
        '''User not found'''
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls):
        '''User already registered'''
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def unknown_error(cls):
        '''Unknown error'''
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def article_not_found(cls):
        '''Article not found'''
        return cls(**ARTICLE_NOT_FOUND)

    @classmethod
    def comment_not_owned(cls):
        '''Comment not owned'''
        return cls(**COMMENT_NOT_OWNED)
