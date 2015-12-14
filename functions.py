
def get_company(tokens):
    toyota = ["toyota"]
    volkswagen = ["volkswagen", "vw"]
    gm = ["general motors"]

    error = -1
    for t in tokens:
        if t in toyota:
            return 1
        elif t in volkswagen:
            return 2
        elif t in gm:
            return 3

    return

def is_RT(tokens):
    first_word = tokens[0].lower()
    if first_word == "rt":
        return 1
    else:
        return 0


tokens = ["RT", "great", "general motors"]
company = get_company(tokens)
RT = is_RT(tokens)

print(company)
print(RT)


