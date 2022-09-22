from line_profiler import LineProfiler
import requests
from promise import Promise

def request(method, url, **kwargs) -> Promise:
	"""
	Wrapper for async requests.request
	"""

	def _request(resolve, _):
		"""
		Async request
		"""
		response = requests.request(method, url, **kwargs)
		resolve(response)

	return Promise(_request)