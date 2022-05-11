from abc import ABC, abstractmethod
import types
import importlib


class Product(ABC):

    def __init__(self, obj: object):
        self.product = obj

    @abstractmethod
    def to_dictionary(self) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get(dictionary: dict):
        pass

    @staticmethod
    @abstractmethod
    def check_type(obj: object) -> bool:
        pass


class Function(Product):

    def to_dictionary(self) -> dict:
        dictionary = {'type': 'function'}
        keys = ['code_arg', 'globals', 'name']
        func_code = self.product.__code__
        code_args = [
            "argcount", "posonlyargcount", "kwonlyargcount", "nlocals", "stacksize", "flags", "code",
            "consts", "names", "varnames", "filename", "name",
            "firstlineno", "lnotab", "freevars", "cellvars"]
        code_dict = dict([(arg, getattr(func_code, "co_" + arg)) for arg in code_args])
        values = [code_dict, self.product.__globals__.copy(), self.product.__name__]
        dictionary.update(dict(zip(keys, values)))
        globals_dict_keys = list(dictionary['globals'].keys())
        for item in globals_dict_keys:
            if item[0] == '_':
                del dictionary['globals'][item]
        if dictionary['name'] in dictionary['globals'] and dictionary['globals'][dictionary['name']] is self.product:
            del dictionary['globals'][dictionary['name']]
        class_name = self.find_class_in_fullname()
        if class_name != '':
            del dictionary['globals'][class_name]
        return dictionary

    def find_class_in_fullname(self) -> str:
        class_name = ''
        type_func = str(self.product)
        space_index = type_func.find(' ')
        index = type_func.find(self.product.__name__)
        # print(index)
        if type_func[index-1] == '.':
            class_name = type_func[space_index+1:index-1]
        return class_name

    @staticmethod
    def get(dictionary: dict) -> types.FunctionType:
        code_dict = dictionary['code_arg']
        args = list(code_dict.keys())
        func_code = types.CodeType(code_dict[args[0]], code_dict[args[1]], code_dict[args[2]],
                                   code_dict[args[3]], code_dict[args[4]], code_dict[args[5]],
                                   bytes(code_dict[args[6]]), tuple(code_dict[args[7]]),
                                   tuple(code_dict[args[8]]), tuple(code_dict[args[9]]), code_dict[args[10]],
                                   code_dict[args[11]], int(code_dict[args[12]]), bytes(code_dict[args[13]]),
                                   tuple(code_dict[args[14]]), tuple(code_dict[args[15]]))
        for item in dictionary['globals'].keys():
            if dictionary['globals'][item] == 'module':
                module = importlib.import_module(item)
                dictionary['globals'][item] = module
        new_f = types.FunctionType(func_code, dictionary['globals'], dictionary['name'])
        return new_f

    @classmethod
    def get_methods(cls, dictionary: dict) -> None:
        dict_cls_keys = dictionary['dict'].keys()
        for key in dict_cls_keys:
            value = dictionary['dict'][key]
            if isinstance(value, dict):
                if value.get('type', -1) != -1 and value['type'] == 'function':
                    dictionary['dict'][key] = cls.get(value)

    @staticmethod
    def check_type(obj: object) -> bool:
        if isinstance(obj, types.FunctionType):
            return True
        return False


class Class(Product):

    def to_dictionary(self) -> dict:
        dictionary = {'type': 'class'}
        keys = ['name', 'bases', 'dict']
        dictionary.update({key: getattr(self.product, '__' + key + '__') for key in keys})
        dictionary['dict'] = dict(dictionary['dict'])
        del dictionary['dict']['__dict__']
        del dictionary['dict']['__weakref__']
        del dictionary['dict']['__doc__']
        del dictionary['dict']['__module__']
        dictionary['bases'] = dictionary['bases'][1:]
        return dictionary

    @staticmethod
    def get(dictionary) -> type:
        new_cls = type(dictionary['name'], tuple(dictionary['bases']), dictionary['dict'])
        return new_cls

    @staticmethod
    def check_type(obj: object) -> bool:
        string = str(obj)
        if string.find('class') != -1:
            return True
        return False


class ClassInstance(Product):

    def to_dictionary(self) -> dict:
        dictionary = {'type': 'instance'}
        keys = ['class', 'dict']
        dictionary.update({key: getattr(self.product, '__' + key + '__') for key in keys})
        return dictionary

    @staticmethod
    def get(dictionary) -> object:
        new_obj = dictionary['class']()
        for key, val in dictionary['dict'].items():
            setattr(new_obj, key, val)
        return new_obj

    @staticmethod
    def check_type(obj: object) -> bool:
        string = str(obj)
        if string.find('object') != -1:
            return True
        return False
