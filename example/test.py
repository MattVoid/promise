from promise.promise import Promise

if __name__ == '__main__':
	promise = Promise() #-> create a promise
	promise.then(lambda value: print(value)) #-> set the handler