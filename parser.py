import sys
import collections.abc
import json


def cast_array(array_string):

    elements = array_string.split('],')
    casted_list = []
    for e in elements:
        elem = e.replace("]", "").replace("[", "").split(",")
        casted_elem = []
        for a in elem:
            casted_elem.append(a.replace(",", "").replace(" ", "").replace("\"", ""))
        casted_list.append(casted_elem)
    return casted_list


def array_json(array):

    heads = array[0]
    array.pop(0)
    data = {}
    for index, h in enumerate(heads):
        data_arr = []
        for a in array:
            if a[index] == "":
                data_arr.append(None)
            else:
                data_arr.append(int(a[index]))
        data[h] = data_arr
    json_data = json.dumps(data)
    return json_data


def merge_json(json1, json2):
    keys = []
    for key in json1.keys():
        keys.append(key)
    for key in json2.keys():
        keys.append(key)
    keys = list(set(keys))

    data = {}
    for key in keys:
        data[key] = []
        if key in json1:
            if isinstance(json1[key], collections.abc.Iterable):
                for e in json1[key]:
                    data[key].append(e)
            else:
                data[key].append(json1[key])
        else:
            data[key].append(None)
        if key in json2:
            data[key].append(json2[key])
        else:
            data[key].append(None)
    json_data = json.dumps(data)
    return json.loads(json_data)


def parser(json_obj):
    try:
        json_object = json.loads(json_obj)
        while len(json_object) > 1:
            json_object[1] = merge_json(json_object[0], json_object[1])
            json_object.pop(0)
    except ValueError as e:
        return array_json(cast_array(json_obj))
    return json_object[0]


print(parser(sys.argv[1]))
