from random import choice,randrange
from string import ascii_letters

def generatorKeyToken():
    letters = ascii_letters
    randonWord = "".join(choice(letters)for i in range(randrange(5,10)))
    return randonWord    

