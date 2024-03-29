def greet(name):
    return f"Hello, {name}!"

class Greeter:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hi, {self.name}!"

if __name__ == "__main__":
    greeter = Greeter("World")
    print(greeter.greet())
