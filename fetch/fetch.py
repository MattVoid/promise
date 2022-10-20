from typing import Any
from fetch.Response.Response import Response
from promise import Promise
import requests


def _parse_parameter(options, parameter: Any) -> Any:
	
	default_value = None

	#>> default value switch
	if parameter == "headers": default_value = {}
	elif parameter == "body": default_value = None
	elif parameter == "mode": default_value = "cors"
	elif parameter == "credentials": default_value = "same-origin"
	elif parameter == "cache": default_value = "default"
	elif parameter == "redirect": default_value = "follow"
	elif parameter == "referrer": default_value = "client"
	elif parameter == "referrerPolicy": default_value = "no-referrer-when-downgrade"
	elif parameter == "integrity": default_value = ""
	elif parameter == "keepalive": default_value = False
	elif parameter == "signal": default_value = None

	return options[parameter] if parameter in options else default_value


def _fetch(url: str, options: dict = {}):
	"""Fetch a URL and return the response body.

	Args:
		url: The URL to fetch.
		options: A dictionary of options.

	Returns:
		The response body.
	"""

	#>> requeired parameters
	method = _parse_parameter(options, "method")

	#>> parse headers
	headers = _parse_parameter(options, "headers")
	mode = _parse_parameter(options, "mode")
	redirect = _parse_parameter(options, "redirect")
	referrer = _parse_parameter(options, "referrer")
	cache = _parse_parameter(options, "cache")
	referrerPolicy = _parse_parameter(options, "referrerPolicy")
	integrity = _parse_parameter(options, "integrity")
	keepalive = _parse_parameter(options, "keepalive")
	signal = _parse_parameter(options, "signal")
	

	body = _parse_parameter(options, "body")
	credentials = _parse_parameter(options, "credentials")
	
	requests_response = requests.request(
		method=method,
		url=url,
		headers=headers,
		data=body,
		mode=mode,
		credentials=credentials,
		cache=cache,
		redirect=redirect,
		referrer=referrer,
		referrerPolicy=referrerPolicy,
		integrity=integrity,
		keepalive=keepalive,
		signal=signal
	)

	response = Response(requests_response)

def fetch(url: str, options: dict = {}) -> Promise:
	"""Fetch a URL and return the response body.

	Args:
		url: The URL to fetch.
		options: A dictionary of options.

	Returns:
		The response body.
	"""
	return Promise(_fetch)