import Const
import re


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

with open("data/input.txt", "r", encoding="utf8") as reader:
    # list title is the top list which save the top level title
    title = []
    title2 = []
    title3 = []
    text4 = []
    dict_text = {}

    is_top_title = False
    is_text = False

    for line in reader:
        line = line.strip('\n')
        # whether current line is the top level title

        # print(line)
        print(line, end="")

        # check data state and setup the important flag
        if StrTools.is_line_empty(line):
            continue

        if line == Const.TITLE:
            is_top_title = True
            continue

        if line == Const.TEXT:
            is_top_title = False
            is_text = True
            continue

        # process data
        if is_top_title:
            # if the first character is not digit then it belong to the top level title
            if not line[:1].isdigit():
                title.append(line)
                continue

            # this judge(title3) has to come first, or the logic will be broken
            if re.match('^\d\.\d', line[:3]):
                title3.append(line)
                continue
            # how to append title2 to title?
            # if the first 2 characters are structure like "1." , they should be the second level title
            if re.match('^\d\.', line[:2]):
                title2.append(line)
                continue

        if is_text:
            # only match structure like "1.x"
            if re.match('^\d\.\d', line[:3]):
                # if text4 is not empty, append text4 to dict, whether need deep copy?
                if text4:
                    # use the line as key, need the data match exactly!
                    dict_text[line] = text4.copy()
                # put the current line into the cur_title3, useful?
                cur_title3 = line
                # clear text[], prepare the next fill in data
                text4.clear()
                continue
            # the last text4 data is not put into dict_text!
            text4.append(line)






    pass





            




