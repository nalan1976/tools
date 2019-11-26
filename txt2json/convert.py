import Const
import re
import json
# from copy import deepcopy
from goto import with_goto


class StrTools(object):

    @staticmethod
    def is_line_empty(input_line):
        input_line = input_line.strip()
        # if input_line in ['\n', '\r\n'] or input_line.strip() == "":
        if input_line in ['\n', '\r\n'] or input_line.strip() == "":
            return True
        else:
            return False


class ContainerTools(object):

    @staticmethod
    def dict_slice(adict, condition):
        """
            dictionary slice
        """
        dict_slice = {key: value for key, value in adict.items() if key[:1] == condition}
        return dict_slice

    @staticmethod
    def list_slice(alist, condition):
        """
            list slice
        """
        list_slice = []
        [list_slice for value in alist if value[:1] == condition]
        return list_slice


Const.TITLE = "[ailink-content]"
Const.TEXT = "[ailink-text]"
Const.EOF = "[ailink-end]"


@with_goto
def dump_json(ltitle, dtitle, dtext):
    # build the data structure
    dict1 = {}
    dict2 = {}
    dict3 = {}
    dict4 = {}

    list1 = []
    list2 = []
    list3 = []
    list4 = []
    # put the dtitle.key into the list_title
    list_title = []
    list_title_index = 0
    for k in dtitle.keys():
        list_title.append(k)

    # populating dict4, list4, dict3 and list3
    """
        k like "1. Engaging in interaction"
        v like "1.1 Responds positively to familiar adult"
        l is the lowest node like "• Responds positively to physical contact"
    """
    for lt in ltitle:
        cur_k = ""
        for k, v in dtext.items():
            for l in v:
                dict4["text"] = l
                dict4["level"] = 3
                list4.append(dict4.copy())
                dict4.clear()
            dict3["children"] = list4.copy()
            list4.clear()
            dict3["level"] = 2
            dict3["text"] = k

            # populating dict2 which save like "1. Engaging in interaction"
            if cur_k != "" and cur_k[:1] != k[:1]:
                if list_title_index < len(list_title):
                    dict2["text"] = list_title[list_title_index]
                    list_title_index += 1
                dict2["level"] = 1
                dict2["children"] = list3.copy()
                list3.clear()
                list2.append(dict2.copy())
                dict2.clear()

            list3.append(dict3.copy())
            dict3.clear()
            cur_k = k
        # repeat code : Bad code smell
        if list_title_index < len(list_title):
            dict2["text"] = list_title[list_title_index]
            list_title_index += 1
        dict2["level"] = 1
        dict2["children"] = list3.copy()
        list3.clear()
        list2.append(dict2.copy())
        dict2.clear()
        # put list2 into dict1
        dict1["children"] = list2.copy()
        list2.clear()
        dict1["text"] = lt
        dict1["level"] = 0
        list1.append(dict1.copy())
        dict1.clear()
    """
    # build the data structure
    dict1 = {}
    dict2 = {}
    dict3 = {}

    list1 = []
    list2 = []
    # the first character of the dict_text's key
    first = ""
    # dtext_start = 0
    # dtext_end = 0
    # ctool = ContainerTools()
    for dtext_k, dtext_v in dtext.items():
        # if the first character has changed, that means the dict3 should end
        if first != "" and first != dtext_k[:1]:
            list2.append(ContainerTools.dict_slice(dtext, first[:1]))
            # dtext_start = dtext_end

        first = dtext_k[:1]
        # dtext_end += 1
    # put the last data into list2
    list2.append(ContainerTools.dict_slice(dtext, first[:1]))

    # populating dict2
    list2_idx = 0
    for dtitle_k in dtitle.keys():
        if list2_idx < len(list2):
            dict2[dtitle_k] = list2[list2_idx]
            list2_idx += 1
        else:
            break

    # populating list1
    list1.append(dict2)

    # populating dict1
    dict1[title[0]] = list1
    """
    # correct format
    data = {"title": [{"title2": [{"title3": [{"type1": 1}, {"type2": 2}, {"type3": 3}]}]}]}


    # data = dict1

    print(json.dumps(data))
    with open("output\output.json", 'w', encoding="utf8") as json_file:
        json.dump(data, json_file)

def read_json():
    with open("output\output.json", "r", encoding="utf8") as json_file:
        data = json.load(json_file)
        print(data)
# dump_json(1,1)



with open("data/input.txt", "r", encoding="utf8") as reader:
    # list title is the top list which save the top level title
    title = []
    title2 = []
    title3 = []
    text4 = []

    dict_text = {}
    dict_title = {}

    is_top_title = False
    is_title2_not_empty = False
    is_text = False

    cur_title2 = ""


    for line in reader:
        line = line.strip('\n')
        # whether current line is the top level title

        print(line)
        # print(line, end="")

        # check data state and setup the important flag
        if StrTools.is_line_empty(line):
            continue

        if line == Const.TITLE:
            is_top_title = True
            continue

        if line == Const.TEXT:
            # fill in the last dict_title
            if title2 and title3:
                dict_title[cur_title2] = title3.copy()
                title3.clear()
            is_top_title = False
            is_text = True
            continue

        # process data
        if is_top_title:
            # if the first character is not digit then it belong to the top level title
            if not line[:1].isdigit():
                title.append(line)
                if title2 and title3:
                    dict_title[cur_title2] = title3.copy()
                    title3.clear()
                continue

            # this judge(title3) has to come first, or the logic will be broken, judge title2 need match $
            if re.match('^\d\.\d', line[:3]):
                title3.append(line)
                continue

            # if the first 2 characters are structure like "1." , they should be the second level title
            if re.match('^\d\.', line[:2]):
                # find out the second structure like "1." and title2 is not empty
                # if line[:1] == "1" and title2:
                # if line[:1] == "1":
                if cur_title2 and int(line[:1]) == int(cur_title2[:1]) + 1:
                    dict_title[cur_title2] = title3.copy()
                    title3.clear()
                # else:
                #     continue
                    # if is_title2_not_empty and title2:
                    #     dict_title[cur_title2] = title3.copy()
                    #     is_title2_not_empty = False
                    # else:
                    #     is_title2_not_empty = True
                    #     continue

                cur_title2 = line

                title2.append(line)
                continue

        if is_text:
            # only match structure like "1.x"
            if re.match('^\d\.\d', line[:3]):
                # if text4 is not empty, append text4 to dict, whether need deep copy?
                if text4:
                    # use the line as key, need the data match exactly!
                    dict_text[cur_title3] = text4.copy() #should be cur_title3?
                # put the current line into the cur_title3, useful?
                cur_title3 = line
                # clear text[], prepare the next fill in data
                text4.clear()
                continue
            # the last text4 data is not put into dict_text!
            text4.append(line)
        if line == Const.EOF:
            dict_text[cur_title3] = text4[:-1].copy()

    # all the data are ready, prepare to output json
    dump_json(title, dict_title, dict_text)

    read_json()



    pass





            




