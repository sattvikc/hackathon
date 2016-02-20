class RegisterMetaClass(type):

    def __init__(cls, name, bases, nmspc):
        super(RegisterMetaClass, cls).__init__(name, bases, nmspc)
        if hasattr(cls, 'REGISTER_BASE'):
            cls._REGISTRY = {}

        for base in bases:
            if hasattr(base, '_REGISTRY'):
                base.register(cls)

    def __iter__(cls):
        return iter(cls._REGISTRY.items())


class Register(object, metaclass=RegisterMetaClass):
    @classmethod
    def register(cls, new_class):
        cls._REGISTRY[new_class.ID] = new_class

    @classmethod
    def get_class(cls, _id):
        return cls._REGISTRY.get(_id)
