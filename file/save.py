# -*- coding:UTF-8 -*-
import yaml


def readYaml(path, fields=''):
    with open(path, 'r', encoding="UTF-8") as file:
        data = file.read()
        r = yaml.load(data, Loader=yaml.FullLoader)
        res = paring_fields(r, fields)
        return res


def paring_fields(res, fields):
    if fields:
        f = fields.split('.')
        for field in f:
            res = res[field]
        return res


if __name__ == '__main__':
    result = readYaml('test.yaml')
    print(result)
