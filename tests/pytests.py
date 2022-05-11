from serialization.convertor import *
from examples.function1 import f
from examples.function2 import m
from examples.cls1 import A
from examples.cls2 import B
from examples.cls3 import C
from serialization.serializers import *
from serialization.products import *


def test_dictionary_convertor():
    d = {'1': (3, 4), '2': b'\xd0\x91\xd0\xb0\xd0\xb9\xd1\x82\xd1\x8b'}
    res_dict = {'1': [3, 4], '2': list(b'\xd0\x91\xd0\xb0\xd0\xb9\xd1\x82\xd1\x8b')}
    DictionaryConvertor.dict_element_to_file_format(d)
    assert str(d) == str(res_dict)
    d = {'1': (3, 4), '2': None}
    res_dict = '{\n\t"1": [\n\t\t3,\n\t\t4\n\t],\n\t"2": null\n}'
    str_dict = DictionaryConvertor.dict_to_json_format(d)
    assert str_dict == res_dict


def test_json_serializer_for_function():
    assert JSONFunctionSerializer.loads(JSONFunctionSerializer.dumps(Function(f)))(3) == f(3)
    assert JSONFunctionSerializer.load(JSONFunctionSerializer.dump(Function(f), 'serialization_files/test_func'))(5) == f(5)
    assert JSONFunctionSerializer.loads(JSONFunctionSerializer.dumps(Function(m)))('ple', 'ase') == m('ple', 'ase')
    assert JSONFunctionSerializer.load(JSONFunctionSerializer.dump(Function(m), 'serialization_files/test_func'))('n', 'a') == m('n', 'a')


def test_yaml_serializer_for_function():
    assert YAMLFunctionSerializer.loads(YAMLFunctionSerializer.dumps(Function(f)))(3) == f(3)
    assert YAMLFunctionSerializer.load(YAMLFunctionSerializer.dump(Function(f), 'serialization_files/test_func'))(5) == f(5)
    assert YAMLFunctionSerializer.loads(YAMLFunctionSerializer.dumps(Function(m)))('ple', 'ase') == m('ple', 'ase')
    assert YAMLFunctionSerializer.load(YAMLFunctionSerializer.dump(Function(m), 'serialization_files/test_func'))('n', 'a') == m('n', 'a')


def test_toml_serializer_for_function():
    assert TOMLFunctionSerializer.loads(TOMLFunctionSerializer.dumps(Function(m)))('n', 'a') == m('n', 'a')
    assert TOMLFunctionSerializer.load(TOMLFunctionSerializer.dump(Function(m), 'serialization_files/test_func'))('n', 'a') == m('n', 'a')


def test_json_serializer_for_class():
    new_a = JSONClassSerializer.loads(JSONClassSerializer.dumps(Class(A)))
    a = new_a()
    assert a.number == 1
    assert a.size == '3'
    assert a.name == '1'
    new_a = JSONClassSerializer.load(JSONClassSerializer.dump(Class(A), 'serialization_files/test_class'))
    a = new_a()
    assert a.number == 1
    assert a.size == '3'
    assert a.name == '1'


def test_toml_serializer_for_class():
    new_a = TOMLClassSerializer.loads(TOMLClassSerializer.dumps(Class(A)))
    a = new_a()
    assert a.number == 1
    assert a.size == '3'
    assert a.name == '1'
    new_a = TOMLClassSerializer.load(TOMLClassSerializer.dump(Class(A), 'serialization_files/test_class'))
    a = new_a()
    assert a.number == 1
    assert a.size == '3'
    assert a.name == '1'


def test_yaml_serializer_for_class():
    new_b = YAMLClassSerializer.loads(YAMLClassSerializer.dumps(Class(B)))
    b = new_b()
    assert b.n == B().n
    assert b.m == B().m
    assert b.sum() == B().sum()
    new_b = YAMLClassSerializer.load(YAMLClassSerializer.dump(Class(B), 'serialization_files/test_class'))
    b = new_b()
    assert b.n == B().n
    assert b.m == B().m
    assert b.sum() == B().sum()


def test_yaml_serializer_for_instance():
    c_ = C()
    c_.ch_a(3)
    c_.ch_t()
    new_c = YAMLClassInstanceSerializer.loads(YAMLClassInstanceSerializer.dumps(ClassInstance(c_)))
    assert c_.a == new_c.a
    assert c_.c == new_c.c
    assert c_.t == new_c.t
    new_c = YAMLClassInstanceSerializer.load(YAMLClassInstanceSerializer.dump(ClassInstance(c_),
                                             'serialization_files/test_instance'))
    assert c_.a == new_c.a
    assert c_.c == new_c.c
    assert c_.t == new_c.t


def test_json_serializer_for_instance():
    c_ = C()
    c_.ch_a(1)
    c_.c = 4
    new_c = JSONClassInstanceSerializer.loads(JSONClassInstanceSerializer.dumps(ClassInstance(c_)))
    assert c_.a == new_c.a
    assert c_.c == new_c.c
    assert c_.t == new_c.t
    new_c = JSONClassInstanceSerializer.load(JSONClassInstanceSerializer.dump(ClassInstance(c_),
                                             'serialization_files/test_instance'))
    assert c_.a == new_c.a
    assert c_.c == new_c.c
    assert c_.t == new_c.t

