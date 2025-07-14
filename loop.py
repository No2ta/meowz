import meow

while True:
	text = input('^w^--> ')
	if text.strip() == "": continue
	result, error = meow.run('<stdin>', text)

	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))