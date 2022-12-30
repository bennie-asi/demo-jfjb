# -*- coding:UTF-8 -*-

class MyFile:

    def __int__(self):
        pass

    def readYaml(self, path, fields=''):
        import yaml
        with open(path, 'r', encoding="UTF-8") as file:
            data = file.read()
            r = yaml.load(data, Loader=yaml.FullLoader)
            res = self.__paring_fields(r, fields)
        return res

    @staticmethod
    def __paring_fields(res, fields):
        if fields:
            f = fields.split('.')
            for field in f:
                res = res[field]
        return res


if __name__ == '__main__':
    myFile = MyFile()
    result = myFile.readYaml('test.yaml')
    print(result)
