# promise state
import asyncio
from time import sleep
from typing import Any, Callable, List
import threading

PENDING = 0
FULFILLED = 1
REJECTED = -1

class Promise:

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
		self._state = PENDING

		self._handleFulfilled = None
		self._handleRejected = None

		self._execution_value = None
		self._execution_reason = None
		self._execution_thread = None

		self._rejection_value = None

		if executor:

			self._execution_thread = threading.Thread(target=self._resolve_executor, args=(executor,))
			self._execution_thread.start()

	# * ██████╗ ██████╗ ██╗██╗   ██╗ █████╗ ████████╗███████╗
	# * ██╔══██╗██╔══██╗██║██║   ██║██╔══██╗╚══██╔══╝██╔════╝
	# * ██████╔╝██████╔╝██║██║   ██║███████║   ██║   █████╗  
	# * ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝██╔══██║   ██║   ██╔══╝  
	# * ██║     ██║  ██║██║ ╚████╔╝ ██║  ██║   ██║   ███████╗
	# * ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                     
	def _resolutionFunc(self, value: Any):
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
		if self._state == PENDING: self._state = FULFILLED

		self._execution_value = value

		if self._handleFulfilled:
			self._execution_value = self._handleFulfilled(self._execution_value)

	def _rejectionFunc(self, reason: Any):
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
		if self._state == PENDING: self._state = REJECTED

		if self._handleRejected:
			self._execution_value = self._handleRejected(reason)

	def _resolve_executor(self, executor: Callable):
		try:
			executor(self._resolutionFunc, self._rejectionFunc) 
		except Exception as reason:
			self._execution_reason = reason
			self._rejectionFunc(reason)

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
		self._handleFulfilled = handleFulfilled # <- call in _resolutionFunc
		self._handleRejected = handleRejected # <- call in _rejectionFunc

		def executor(resolve, _):

			# await promise to be resolved
			if self._state == PENDING:
				self._execution_thread.join()
			elif self._state == FULFILLED and self._handleFulfilled:
				self._execution_value = self._handleFulfilled(self._execution_value)
			elif self._state == REJECTED and self._handleRejected:
				self._execution_value = self._handleRejected(self._execution_reason)

			resolve(self._execution_value)

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

				

if __name__ == "__main__":
	
	def callback(resolve, reject):
		print('init callback')

		# raise Exception('error')

		sleep(1)
		resolve("ressasasaolve")

	print('init promise')
	promise = Promise(callback)

	print('init then')
	# promise.catch(lambda reason: print("Error: " + reason.__str__()))
	promise.then(lambda value: print(value)).then(lambda value: print(value))

	print('end')
