from typing import Callable

from promise.promise import Promise


def awaiter(func: Callable[..., Promise]) -> Callable[..., Promise]:
	"""
	A decorator that awaits the promise to be resolved before calling the function.
	"""

	def wrapper(*args, **kwargs):
		promise = func(*args, **kwargs)
		promise.__execution_thread.join()
		return promise

	return wrapper