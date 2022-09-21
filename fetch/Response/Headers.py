# https://developer.mozilla.org/en-US/docs/Web/API/Headers/delete
# https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_header_name
# https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_response_header_name
from functools import wraps
import functools
import re
from typing import Callable

class Headers:

	def __init__(self, init: dict = {}):
		"""
		The Headers() constructor creates a new Headers object.

		Parameters
		----------
		init : dict
			An object containing any HTTP headers that you want to 
			pre-populate your Headers object with. This can be a simple 
			object literal with String values, an array of name-value pairs, 
			where each pair is a 2-element string array; or an existing 
			Headers object. In the last case, the new Headers object copies 
			its data from the existing Headers object.
		"""

		self.__headers = self.__parse_init(init)


	def __parse_init(self, init: dict):

		headers = {}

		for name, value in init.items():

			name = name.lower()

			if name in headers: 
				headers[name] = f"{headers[name]}, {value}"
			else: 
				headers[name] = value

		return headers


	#* ██████╗ ███████╗ ██████╗ ██████╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗ ███████╗
	#* ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝
	#* ██║  ██║█████╗  ██║     ██║   ██║██████╔╝███████║   ██║   ██║   ██║██████╔╝███████╗
	#* ██║  ██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗╚════██║
	#* ██████╔╝███████╗╚██████╗╚██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║███████║
	#* ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝

	def __check_http_header_name(func: Callable) -> bool:
		"""
		The __check_http_header_name() method of the Headers interface 
		checks if a header name is valid.
		"""

		def inner(self, *args):

			args = list(args)
			name = args[0].lower()

			if re.match('^[a-zA-Z0-9_-]+$', name):

				args[0] = name
				return func(self, *args)
			else:
				raise TypeError(f"Failed to execute '{func.__name__}' on 'Headers': Invalid name")
		
		return inner
                         
	#* ███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗
	#* ████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝
	#* ██╔████╔██║███████║██║  ███╗██║██║     
	#* ██║╚██╔╝██║██╔══██║██║   ██║██║██║     
	#* ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗
	#* ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝
             

	def __getitem__(self, name: str) -> str:
		"""
		Magic method that call "get" method.
		"""
		return self.get(name)

	def __delitem__(self, name: str) -> None:
		"""
		Magic method that call "delete" method.
		"""
		return self.delete(name)

	def __contains__(self, name: str) -> bool:
		"""
		Magic method that call "has" method.
		"""
		return self.has(name)

	def __setitem__(self, name: str, value: str) -> None:
		"""
		Magic method that call "set" method.
		"""
		return self.set(name, value)

	#* ██╗████████╗███████╗██████╗ 
	#* ██║╚══██╔══╝██╔════╝██╔══██╗
	#* ██║   ██║   █████╗  ██████╔╝
	#* ██║   ██║   ██╔══╝  ██╔══██╗
	#* ██║   ██║   ███████╗██║  ██║
	#* ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

	def entries(self) -> iter:
		"""
		The Headers.entries() method returns an iterator allowing 
		to go through all key/value pairs contained in this object. 
		The both the key and value of each pairs are String objects.
		"""
		return iter(self.__headers.items())

	def keys(self) -> iter:
		"""
		The Headers.keys() method returns an iterator allowing to go through 
		all keys contained in this object. The keys are String objects.
		"""

		return iter(self.__headers.keys())

	def values(self) -> iter:
		"""
		The Headers.values() method returns an iterator allowing to go 
		through all values contained in this object. The values are String 
		objects.
		"""

		return iter(self.__headers.values())
								
	def forEach(self, callback: Callable[[str, str], None]) -> None:
		"""
		The Headers.forEach() method executes a callback function once 
		per each key/value pair in the Headers object.
		"""


	#*  █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗
	#* ██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
	#* ███████║██║        ██║   ██║██║   ██║██╔██╗ ██║
	#* ██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║
	#* ██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
	#* ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                               
	@__check_http_header_name
	def append(self, name: str, value: str) -> None:
		"""
		The append() method of the Headers interface appends a new value 
		onto an existing header inside a Headers object, or adds the 
		header if it does not already exist.
		"""

		if name in self.__headers:
			self.__headers[name] = f"{self.__headers[name]}, {value}"
		else: self.set(name, value)

	@__check_http_header_name
	def delete(self, name: str) -> None:
		"""
		The delete() method of the Headers interface deletes a header 
		from the current Headers object.

		Parameters
		----------
		name : str
			The name of the HTTP header you want to delete from the Headers object.
		"""

		if name in self.__headers:
			del self.__headers[name]

	@__check_http_header_name
	def get(self, name: str) -> str:
		"""
		The get() method of the Headers interface returns a byte string 
		of all the values of a header within a Headers object with a 
		given name. If the requested header doesn't exist in the Headers 
		object, it returns null.

		Parameters
		----------
		name : str
			The name of the HTTP header whose values you want to retrieve 
			from the Headers object. If the given name is not the name of 
			an HTTP header, this method throws a TypeError. 
			The name is case-insensitive.

		Returns
		-------
		str
			A byte string of all the values of a header within a Headers 
			object with a given name. If the requested header doesn't exist 
			in the Headers object, it returns null.
		"""

		if name in self.__headers:
			return self.__headers[name]

		return None

	@__check_http_header_name
	def has(self, name: str) -> bool:
		"""
		The has() method of the Headers interface returns a boolean stating 
		whether a Headers object contains a certain header.

		Parameters
		----------
		name : str
			The name of the HTTP header you want to test for. If the given 
			name is not a valid HTTP header name, this method throws a TypeError.
		"""

		return name in self.__headers
	
	@__check_http_header_name
	def set(self, name: str, value: str) -> None:
		"""
		The set() method of the Headers interface sets a new value for an 
		existing header inside a Headers object, or adds the header if it 
		does not already exist.

		Parameters
		----------
		name : str
			The name of the HTTP header you want to set to a new value. 
			If the given name is not the name of an HTTP header, this method 
			throws a TypeError.

		value : str
			The new value you want to set.

		Returns
		-------
		None
		"""

		self.__headers[name] = value # <- "set" overwrites the value of an existing header.

if __name__ == "__main__":
	headers = Headers()
	headers.set("Content-Type", "application/json")
	headers.set("Content-Length", "123")
	headers.set("Content-Type", "application/json; charset=utf-8")

	del headers["content-lengthé**é*§?"]
	
	print(headers.get("content-length"))