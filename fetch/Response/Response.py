from typing import Any
import requests

from fetch.Response.Headers import Headers

# class Response:

# 	def __init__(self, response: requests.Response, options: dict = {}):

# 		#>> private properties
# 		self.__response = response

# 		#>> public properties
# 		self.status_code = self.__parse_options(options, "status_code", response.status_code)
# 		self.ok = self.__parse_ok(response.status_code)

# 	def __parse_options(self, options: dict, parameter: str, default_value: Any = None):
# 		if parameter in options: return options[parameter]
# 		else: return default_value

# 	def __parse_ok(status_code: int):
# 		return status_code >= 200 and status_code < 300


class Response:

	def __init__(self, body: requests.Response, options: dict = {}):

		#>> private properties
		# self.__response = response
		self.__type = None

		#>> public properties
		self.status = self.__parse_options(options, "status", 200)
		self.statusText = self.__parse_options(options, "statusText", '')
		self.headers = self.__parse_headers(options)
		self.ok = self.__parse_ok(body.status_code)

	def __parse_options(self, options: dict, parameter: str, default_value: Any = None):
		if parameter in options: return options[parameter]
		else: return default_value

	def __parse_headers(self, options: dict):
		if "headers" in options: return Headers(options["headers"])
		else: return Headers()

	def __parse_ok(status_code: int):
		return status_code >= 200 and status_code < 300