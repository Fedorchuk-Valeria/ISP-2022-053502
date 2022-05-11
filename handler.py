import importlib


class Handler:

    @staticmethod
    def get_serialization(args: list):
        module = importlib.import_module(args.mod)
        obj = module.__dict__[args.n]
        obj_type = Handler.determine_type(obj)
        file_format = args.format.upper()
        serializers_module = importlib.import_module('serialization.serializers')
        current_serializer = serializers_module.__dict__[file_format + obj_type[0] + 'Serializer']
        if args.rf is not None:
            print('get', current_serializer.dump(obj_type[1], args.rf))
        else:
            print(current_serializer.dumps(obj_type[1]))

    # @staticmethod
    # def get_deserialization():

    @staticmethod
    def determine_type(obj: object) -> list:
        module = importlib.import_module('serialization.products')
        keys = list(module.__dict__.keys())
        keys.reverse()
        for key in keys:
            if key == 'Product':
                break
            if module.__dict__[key].check_type(obj):
                return [key, module.__dict__[key](obj)]
