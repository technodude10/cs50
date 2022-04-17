def announce(f):
    def wrapper():
        print("1")
        f()
        print("2")
    return wrapper

@announce
def hello():
    print("hello")

hello()