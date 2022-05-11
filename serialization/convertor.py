import types
from serialization.products import Function, Class


class DictionaryConvertor:

    @classmethod
    def dict_element_to_file_format(cls, dictionary: dict) -> None:
        keys = dictionary.keys()
        for item in keys:
            if isinstance(dictionary[item], dict):
                cls.dict_element_to_file_format(dictionary[item])
            elif isinstance(dictionary[item], int) or isinstance(dictionary[item], str):
                continue
            elif isinstance(dictionary[item], bytes):
                dictionary[item] = list(dictionary[item])
            elif isinstance(dictionary[item], tuple):
                dictionary[item] = list(dictionary[item])
            elif isinstance(dictionary[item], types.ModuleType):
                dictionary[item] = 'module'
            elif isinstance(dictionary[item], types.FunctionType):
                func = Function(dictionary[item])
                func_dict = func.to_dictionary()
                cls.dict_element_to_file_format(func_dict)
                dictionary[item] = func_dict
            elif Class.check_type(dictionary[item]):
                cls_ = Class(dictionary[item])
                cls_dict = cls_.to_dictionary()
                cls.dict_element_to_file_format(cls_dict)
                dictionary[item] = cls_dict

    @classmethod
    def dict_to_json_format(cls, dictionary: dict) -> str:
        cls.dict_element_to_file_format(dictionary)
        str_dict = str(dictionary)
        str_dict = str_dict.replace("'", '"').replace('None', 'null')
        str_dict = str_dict.replace('True', 'true').replace('False', 'false')
        tab, i = '', 0
        length = len(str_dict)
        while i < length:
            if str_dict[i] == '{' or str_dict[i] == '[':
                tab = tab + '\t'
                str_dict = str_dict[:i + 1] + '\n' + tab + str_dict[i + 1:]
                length += len('\n') + len(tab)
            elif str_dict[i] == '}' or str_dict[i] == ']':
                tab = tab[:len(tab)-1]
                str_dict = str_dict[:i] + '\n' + tab + str_dict[i:]
                length += len('\n') + len(tab)
                i += len('\n') + len(tab) + 1
                continue
            if str_dict[i] == ',' and str_dict[i+1] == ' ':
                str_dict = str_dict[:i+1] + '\n' + tab + str_dict[i+2:]
                length += len('\n') + len(tab) - 1
            i += 1
        return str_dict
