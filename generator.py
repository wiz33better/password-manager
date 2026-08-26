import string
import secrets
def generate(case,no,sym):

    if case == "u" or case == "upper":
        pool = string.ascii_uppercase
    elif case == "l" or case == "lower":
        pool = string.ascii_lowercase
    elif case == "m" or case == "mix":
        pool = string.ascii_uppercase + string.ascii_lowercase
    else:
        print("Plese input valid choice: ")

    if no.lower() == "y" or no.lower() == "yes":
        pool += string.digits
    else:
        print("continue without numbers")

    if sym.lower() == "y" or sym.lower() == "yes":
        pool += string.punctuation
    else:
        print("continue without symbols")

    chars = [secrets.choice(pool) for i in range(10)]
    gen_pass = "".join(chars)
    return gen_pass
