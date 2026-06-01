class A:
    x: int
    y: int = 1
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        print("namespace keys:", list(namespace.keys()))
        return super().__new__(mcs, name, bases, namespace)
class B(metaclass=Meta):
    z: str = "hello"
