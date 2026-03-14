long_string=lambda my_string: 'true' if len(my_string)>12 else 'false'
print(long_string('how are you?'))
print(long_string('qwerty123456789'))