import string

positions = {}
alphabet = ' ' + string.ascii_letters
for index, char in enumerate(alphabet):
    positions[char] = index

message = "hi my name is caesar"
keys = list(positions.keys())


def encoding(message, key):
    final = ''
    for char in message:
        index = (positions[char] + key) % 27
        final += keys[index]
    return final


print(encoding(message, 3))
