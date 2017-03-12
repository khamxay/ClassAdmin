import http_codes

class Error(Exception):
	'''Base class for all the exceptions'''
	error_message = ""

	def __init__(self):
		pass

	def __init__(self, message):
		self.error_message = message


class NotFoundError(Error):
	error_code = http_codes.HTTP_NOT_FOUND


class BadInputError(Error):
	error_code = http_codes.HTTP_BAD_INPUT


class AlreadyExistsError(Error):
	error_code = http_codes.HTTP_ALREADY_EXISTS

class ServerSideError(Error):
	error_code = http_codes.HTTP_SERVER_SIDE_ERROR

class BadCredentialsError(Error):
	error_code = http_codes.HTTP_UNAUTHORIZED

class TokenExpiredError(Error):
	error_code = http_codes.HTTP_UNAUTHORIZED