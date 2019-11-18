import Const
import re
import json

class StrTools(object):

    @staticmethod
    def is_line_empty(input_line):
        input_line = input_line.strip()
        # if input_line in ['\n', '\r\n'] or input_line.strip() == "":
        if input_line in ['\n', '\r\n'] or input_line.strip() == "":
            return True
        else:
            return False


Const.TITLE = "[ailink-content]"
Const.TEXT = "[ailink-text]"
Const.EOF = "[ailink-end]"

def dump_json(dtitle, dtext):
    # json = "{"
    # for k, v in dtitle.items():
    #     for key in dtext.keys():
    #
    # json += "}"
    # return json

    # build the data structure
    dict1 = {}
    for t1 in title:
        dict1[t1] = list1

    # correct format
    data = {"title": [{"title2": [{"title3": [{"type1": 1}, {"type2": 2}, {"type3": 3}]}]}]}




    print(json.dumps(data))
    with open("output\output.json", 'w') as json_file:
        json.dump(data, json_file)

def read_json():
    with open("output\output.json", "r") as json_file:
        data = json.load(json_file)
        print(data)
# dump_json(1,1)
# read_json()


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
    dump_json(dict_title, dict_text)





    pass





            




