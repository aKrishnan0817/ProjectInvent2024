x = 0

def func():
    global x
    x=1
def otherFunc():
    global x
    print(x)
if __name__ == "__main__":
    print(x)
    func()
    print(x)
    otherFunc()
