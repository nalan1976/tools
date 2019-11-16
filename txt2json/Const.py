class Const:
    # class ConstError(TypeError):
    #     pass
    #
    # class ConstCaseError(ConstError):
    #     pass

    def __setattr__(self, name, value):
            if name in self.__dict__:
                raise RuntimeError("Can't change const value!")
            if not name.isupper():
                raise RuntimeError("not all letters are capitalized")
            self.__dict__[name] = value
