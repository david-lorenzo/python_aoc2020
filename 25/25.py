
from itertools import count

def ri_transform(subject_number):
    value = 1
    divisor = 20201227
    for i in count(1):
        value = (value * subject_number) % divisor
        yield (i, value)

def transform(subject_number, loop_size):
    value = 1
    divisor = 20201227
    for _ in range(loop_size):
        value = (value * subject_number) % divisor
    return value


# assignment input
card_public_key = 12232269
door_public_key = 19452773

# demo
# card_public_key = 5764801
# door_public_key = 17807724

for card_loop_size, value in ri_transform(7):
    if value == card_public_key:
        break
print(card_loop_size)
encription_key = transform(door_public_key, card_loop_size)
print(encription_key)

encription_key = 354320
