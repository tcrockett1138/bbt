def numbers_to_strings(argument):
    switcher = {
        "foo": "zero",
        1: "one",
        2: "two",
    }
    return switcher.get(argument, "nothing")


print(numbers_to_strings(1))
print(numbers_to_strings(0))
print(numbers_to_strings("foo"))
