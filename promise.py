# promise state
from typing import Any, Callable, List
import threading

class Promise:

	PENDING = 0
	FULFILLED = 1
	REJECTED = -1

	def __init__(self, executor: Callable):
		"""
		The Promise constructor is primarily used to wrap functions that do not already support promises.
		
		Parameters
		----------
		executor : Callable
			A function to be executed by the constructor. It receives 
			two functions as parameters: resolutionFunc and rejectionFunc. 
			Any errors thrown in the executor will cause the promise to be 
			rejected, and the return value will be neglected. The semantics 
			of executor are detailed below.

		Returns
		-------
			When called via new, the Promise constructor returns a promise object. 
			The promise object will become resolved when either of the functions 
			resolutionFunc or rejectionFunc are invoked. Note that if you call 
			resolutionFunc or rejectionFunc and pass another Promise object as 
			an argument, it can be said to be "resolved", but still not "settled". 
			See the Promise description for more explanation.
		"""
		self.__state = self.PENDING

		self.__handleFulfilled = None
		self.__handleRejected = None

		self.__execution_value = None
		self.__execution_reason = None
		self.__execution_thread = None

		self._rejection_value = None

		if executor:

			self.__execution_thread = threading.Thread(target=self.__resolve_executor, args=(executor,))
			self.__execution_thread.start()

	# * ██████╗ ██████╗ ██╗██╗   ██╗ █████╗ ████████╗███████╗
	# * ██╔══██╗██╔══██╗██║██║   ██║██╔══██╗╚══██╔══╝██╔════╝
	# * ██████╔╝██████╔╝██║██║   ██║███████║   ██║   █████╗  
	# * ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝██╔══██║   ██║   ██╔══╝  
	# * ██║     ██║  ██║██║ ╚████╔╝ ██║  ██║   ██║   ███████╗
	# * ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                     
	def __resolutionFunc(self, value: Any):
		"""
		Parameters
		----------
		value : Any
			Any value, including undefined, that is passed to the function. 
			If the value is a Promise object, then the associated Promise 
			will be "resolved" before the resolutionFunc is called. 
			This can be useful when combining multiple Promises together.

		Returns
		-------
			Nothing.
		"""

		# Only the first call to resolutionFunc or rejectionFunc affects the promise's 
		# state, and subsequent calls to either function can neither change the fulfillment 
		# value/rejection reason nor toggle the state from "fulfilled" to "rejected" or opposite
		if self.__state == self.PENDING: self.__state = self.FULFILLED

		self.__execution_value = value

		if self.__handleFulfilled:
			self.__execution_value = self.__handleFulfilled(self.__execution_value)

	def __rejectionFunc(self, reason: Any):
		"""
		Parameters
		----------
		reason : Any
			A value that indicates why the Promise was rejected. 
			This value will be passed to the rejectionFunc when/if it is called.
		
		Returns
		-------
			Nothing.
		"""

		# Only the first call to resolutionFunc or rejectionFunc affects the promise's 
		# state, and subsequent calls to either function can neither change the fulfillment 
		# value/rejection reason nor toggle the state from "fulfilled" to "rejected" or opposite
		if self.__state == self.PENDING: self.__state = self.REJECTED

		if self.__handleRejected:
			self.__execution_value = self.__handleRejected(reason)

	def __resolve_executor(self, executor: Callable):
		try:
			executor(self.__resolutionFunc, self.__rejectionFunc) 
		except Exception as reason:
			self.__execution_reason = reason
			self.__rejectionFunc(reason)

	# * ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗
	# * ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝
	# * ██████╔╝██║   ██║██████╔╝██║     ██║██║     
	# * ██╔═══╝ ██║   ██║██╔══██╗██║     ██║██║     
	# * ██║     ╚██████╔╝██████╔╝███████╗██║╚██████╗
	# * ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝

	def then(self, handleFulfilled: Callable|None = None, handleRejected: Callable|None = None):
		"""
		Parameters
		----------
		handleFulfilled : Callable|None
			A function to be called when the Promise is resolved. 
			This function has one argument, the fulfillment value. 
			If the promise is already resolved, this function will be called 
			immediately. This function will not be called if the promise is rejected.
		
		handleRejected : Callable|None
			A function to be called when the Promise is rejected. 
			This function has one argument, the rejection reason. 
			If the promise is already rejected, this function will be called 
			immediately. This function will not be called if the promise is resolved.

		Returns
		-------
			A Promise. If handleFulfilled is a function, it will be called after 
			this Promise is fulfilled, with the fulfillment value as its first argument. 
			The return value of handleFulfilled will be used as the fulfillment value 
			of the returned Promise. If handleFulfilled is not a function, it will be 
			ignored. If handleRejected is a function, it will be called after this Promise 
			is rejected, with the rejection reason as its first argument. The return value 
			of handleRejected will be used as the fulfillment value of the returned Promise. 
			If handleRejected is not a function, it will be ignored.
		"""

		# set the handlers
		self.__handleFulfilled = handleFulfilled # <- call in __resolutionFunc
		self.__handleRejected = handleRejected # <- call in __rejectionFunc

		def executor(resolve, _):

			# await promise to be resolved
			if self.__state == self.PENDING:
				self.__execution_thread.join() # <- wait for the promise to be resolved
			elif self.__state == self.FULFILLED and self.__handleFulfilled:
				self.__execution_value = self.__handleFulfilled(self.__execution_value)
			elif self.__state == self.REJECTED and self.__handleRejected:
				self.__execution_value = self.__handleRejected(self.__execution_reason)

			if self.__state == self.FULFILLED: resolve(self.__execution_value)
			elif self.__state == self.REJECTED: resolve(self.__execution_reason)

		return Promise(executor)

	def catch(self, handleRejected):
		self.then(None, handleRejected)

	@staticmethod
	def all(iterable: List[Any]):
		"""
		The Promise.all() method takes an iterable of promises as an input, and returns a 
		single Promise that resolves to an array of the results of the input promises. 
		This returned promise will fulfill when all of the input's promises have fulfilled, 
		or if the input iterable contains no promises. It rejects immediately upon any of 
		the input promises rejecting or non-promises throwing an error, and will reject with 
		this first rejection message / error.
		
		Parameters
		----------
		iterable : List[Promise]
            An iterable object such as an Array.

		Returns
		-------
			- An already fulfilled Promise if the iterable passed is empty.

			- An asynchronously fulfilled Promise if the iterable passed contains no promises. 
			  Note, Google Chrome 58 returns an already fulfilled promise in this case.

			- A pending Promise in all other cases. This returned promise is then 
			  fulfilled/rejected asynchronously (as soon as the queue is empty) when all 
			  the promises in the given iterable have fulfilled, or if any of the promises reject. 
			  See the example about "Asynchronicity or synchronicity of Promise.all" below. 
			  Returned values will be in order of the Promises passed, regardless of completion order.
		"""
		
		for item in iterable:

			# ignore if item is not a Promise
			if isinstance(item, Promise):
				promise = item