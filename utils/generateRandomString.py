from random import random
import math


def generateRandomString(length: int) -> str:
    random_string = ""
    alphabet = list("abcdefghijklmnopqrstuvwxyz")

    for _num in range(length):
        random_string += alphabet[math.floor(random() * (len(alphabet) - 1))]

    return random_string
