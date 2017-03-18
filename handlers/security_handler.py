from itsdangerous import (TimedJSONWebSignatureSerializer as JWT, BadSignature, SignatureExpired)
from common.common_error_codes import *

import user_handler

jwt = None

def initialize_token_serializer(config):
	global jwt
	jwt = JWT(config['SECRET_KEY'], expires_in=config['TOKEN_VALIDITY'])

def generate_token(fields_dict):
	return jwt.dumps(fields_dict)

def validate_token(token):
	try:
		data = jwt.loads(token)
	except SignatureExpired:
		raise TokenExpiredError("The token is expired. Please authenticate again.")
	except BadSignature:
		raise BadCredentialsError("Invalid token.")
	return data

def verify_credentials(username, password):
	user = user_handler.get_user_by_username(username)
	if user['password'] == password:
		return user
	raise BadCredentialsError("The username and/or password does not match.")