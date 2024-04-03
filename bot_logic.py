import random
import time
import string

# =========== OPIS FUNKCJI na jednej linii ==================

def gen_pass(pass_length):
    elements = string.ascii_letters  + string.digits + string.punctuation
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password

'''
Opis funkcji
na wielu liniach
'''

def podaj_czas():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    return current_time
