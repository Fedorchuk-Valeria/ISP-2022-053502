from abc import ABC, abstractmethod
import pyaml
import yaml
import toml
from yaml.loader import SafeLoader
import ast
import types
from serialization.products import Product, Function, Class, ClassInstance
from serialization.convertor import DictionaryConvertor


class Serializer(ABC):

    @staticmethod
    def get_product(product: Product) -> dict:
        return product.to_dictionary()

    @classmethod
    @abstractmethod
    def dumps(cls, product: Product) -> str:
        pass

    @classmethod
    @abstractmethod
    def dump(cls, product: Product, filename: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def loads(cls, string: str):
        pass

    @classmethod
    @abstractmethod
    def load(cls, filename: str):
        pass

    @staticmethod
    @abstractmethod
    def get_object(dictionary: dict):
        pass


class JSONSerializer(Serializer):

    @classmethod
    def dumps(cls, product: Product) -> str:
        dictionary = cls.get_product(product)
        str_dict = DictionaryConvertor.dict_to_json_format(dictionary)
        return str_dict

    @classmethod
    def dump(cls, product: Product, filename) -> str:
        filename = filename + '.json'
        file = open(filename, 'w')
        file.write(cls.dumps(product))
        file.close()
        return filename

    @classmethod
    def loads(cls, string: str) -> object:
        string = string.replace('\t', '').replace('\n', ' ').replace('null', 'None')
        string = string.replace('true', 'True').replace('false', 'False')
        dictionary = dict(ast.literal_eval(string))
        new = cls.get_object(dictionary)
        return new

    @classmethod
    def load(cls, filename: str) -> object:
        obj = None
        try:
            file = open(filename, 'r')
            string = file.read()
            obj = cls.loads(string)
            file.close()
        except IOError:
            print("File don't exist")
        return obj

    @classmethod
    @abstractmethod
    def get_object(cls, dictionary: dict):
        pass


class JSONFunctionSerializer(JSONSerializer):

    @classmethod
    def get_object(cls, dictionary: dict) -> types.FunctionType:
        return Function.get(dictionary)


class JSONClassSerializer(JSONSerializer):

    @classmethod
    def get_object(cls, dictionary: dict) -> type:
        cls.get_methods(dictionary)
        return Class.get(dictionary)

    @staticmethod
    def get_methods(dictionary: dict) -> None:
        dict_cls_keys = dictionary['dict'].keys()
        for key in dict_cls_keys:
            value = dictionary['dict'][key]
            if isinstance(value, dict):
                if value.get('type', -1) != -1 and value['type'] == 'function':
                    dictionary['dict'][key] = JSONFunctionSerializer.loads(str(value))


class JSONClassInstanceSerializer(JSONSerializer):

    @classmethod
    def get_object(cls, dictionary: dict) -> object:
        dictionary['class'] = JSONClassSerializer.loads(str(dictionary['class']))
        return ClassInstance.get(dictionary)


class YAMLSerializer(Serializer):

    @classmethod
    def dumps(cls, product: Product) -> str:
        dictionary = cls.get_product(product)
        DictionaryConvertor.dict_element_to_file_format(dictionary)
        s = pyaml.dumps(dictionary, sort_keys=False)
        return s

    @classmethod
    def dump(cls, product: Product, filename: str) -> str:
        filename = filename + '.yaml'
        file = open(filename, 'w')
        dictionary = cls.get_product(product)
        DictionaryConvertor.dict_element_to_file_format(dictionary)
        pyaml.dump(dictionary, file, sort_keys=False)
        file.close()
        return filename

    @classmethod
    def loads(cls, string: str) -> object:
        dictionary = yaml.load(string, SafeLoader)
        new = cls.get_object(dictionary)
        return new

    @classmethod
    def load(cls, filename: str) -> object:
        new = None
        try:
            file = open(filename, 'r')
            dictionary = yaml.load(file, SafeLoader)
            file.close()
            new = cls.get_object(dictionary)
        except IOError:
            print("File don't exist")
        return new

    @classmethod
    @abstractmethod
    def get_object(cls, dictionary: dict):
        pass


class YAMLFunctionSerializer(YAMLSerializer):

    @classmethod
    def get_object(cls, dictionary: dict) -> types.FunctionType:
        return Function.get(dictionary)


class YAMLClassSerializer(YAMLSerializer):

    @classmethod
    def get_object(cls, dictionary: dict) -> type:
        Function.get_methods(dictionary)
        return Class.get(dictionary)


class YAMLClassInstanceSerializer(YAMLSerializer):

    @classmethod
    def get_object(cls, dictionary) -> object:
        dictionary['class'] = Class.get(dictionary['class'])
        return ClassInstance.get(dictionary)


class TOMLSerializer(Serializer):

    @classmethod
    def dumps(cls, product: Product) -> str:
        dictionary = cls.get_product(product)
        DictionaryConvertor.dict_element_to_file_format(dictionary)
        s = toml.dumps(dictionary)
        return s

    @classmethod
    def dump(cls, product: Product, filename: str) -> str:
        filename = filename + '.toml'
        file = open(filename, 'w')
        dictionary = cls.get_product(product)
        DictionaryConvertor.dict_element_to_file_format(dictionary)
        toml.dump(dictionary, file)
        file.close()
        return filename

    @classmethod
    def loads(cls, string: str) -> object:
        dictionary = toml.loads(string)
        string = str(dictionary).replace("'None'", 'None')
        dictionary = dict(ast.literal_eval(string))
        new = cls.get_object(dictionary)
        return new

    @classmethod
    def load(cls, filename: str) -> object:
        new = None
        try:
            file = open(filename, 'r')
            string = file.read()
            file.close()
            new = cls.loads(string)
        except IOError:
            print("File don't exist")
        return new

    @classmethod
    @abstractmethod
    def get_object(cls, dictionary: dict):
        pass


class TOMLFunctionSerializer(TOMLSerializer):

    @classmethod
    def get_object(cls, dictionary) -> types.FunctionType:
        return Function.get(dictionary)


class TOMLClassSerializer(TOMLSerializer):

    @classmethod
    def get_object(cls, dictionary) -> type:
        Function.get_methods(dictionary)
        return Class.get(dictionary)


class TOMLClassInstanceSerializer(TOMLSerializer):

    @classmethod
    def get_object(cls, dictionary) -> object:
        dictionary['class'] = Class.get(dictionary['class'])
        return ClassInstance.get(dictionary)
