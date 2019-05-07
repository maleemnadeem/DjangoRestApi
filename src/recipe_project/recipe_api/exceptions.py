from rest_framework.exceptions import APIException


class DuplicateFollowerException(APIException):
    status_code = 404
    default_detail = 'you are already following this user'


class NotMemberException(APIException):
    status_code = 404
    default_detail = 'Given email address is not register'
