class Meta(type):
    def __new__(mcs, name, bases, namespace):
        print("namespace keys:", list(namespace.keys()))
        print("annotations:", namespace.get("__annotations__"))
        return super().__new__(mcs, name, bases, namespace)
class B(metaclass=Meta):
    __annotations__ = {"z": str}
    z: str = "hello"
