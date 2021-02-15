#!Python3.8.5
import random
import xmltodict
import urllib.request


def get_new_number() -> str:
    ##
    # @brief Get new winning number
    #
    # @return str   Winning number (Space delimited)
    #
    URL = 'https://miniloto.jp.net/databases/xml?data=new&info=no'

    req = urllib.request.Request(URL)
    with urllib.request.urlopen(req) as res:
        # Pick winning number
        xml = res.read()
        dic = xmltodict.parse(xml)
        main_num = dic['results']['times']['main_number']
        bonus_num = dic['results']['times']['bonus_number']
        win_num = "{} {}".format(main_num, bonus_num)
        return win_num

    return ''


def pick_number(min_num: int = 1, max_num: int = 31, count: int = 6) -> str:
    ##
    # @brief Pick loto number
    #
    # @param [in] min_num   Min number
    # @param [in] max_num   Max number
    # @param [in] count     Pick count
    #
    # @return str   Pick number (Space delimited)
    num_list = []

    new_num = get_new_number()
    if new_num == '':
        # Return random number
        c = 0
        while c < count:
            r = random.randint(min_num, max_num)
            if r not in num_list:
                num_list.append(r)
                c = c + 1
    else:
        # Return numerical value based on the law
        new_nums = map(int, new_num.split())
        c = 0
        for n in new_nums:
            if random.randint(0, 1):
                num_list.append(n)
                c = c + 1
        while c < count:
            r = random.randint(min_num, max_num)
            if r not in num_list:
                num_list.append(r)
                c = c + 1

    # Convert num array to string (Space delimited)
    num_list.sort()
    str_list = []
    for n in num_list:
        str_list.append(str(n).zfill(2))
    pick_num = ' '.join(str_list)

    return pick_num


def is_duplicate(pick_num: str) -> int:
    ##
    # @brief Check duplicate pick
    #
    # @param [in] pick_num    Pick number (Space delimited)
    #
    # @retval  0    Not duplicated
    # @retval  1    Duplicated
    # @retval -1    Error

    # Update LotResult.xml
    URL = 'https://miniloto.jp.net/databases/xml?data=all&info=no'

    req = urllib.request.Request(URL)
    with urllib.request.urlopen(req) as res:
        # Pick winning number
        xml = res.read()
        dic = xmltodict.parse(xml)
        for result in dic['results']['times']:
            num_list = result['main_number'].split()
            num_list.append(result['bonus_number'])
            num_list.sort()
            res_num = ' '.join(num_list)
            if res_num == pick_num:
                return 1
        return 0

    return -1


##
# @brief Main
#
if __name__ == "__main__":
    while True:
        num = pick_number()
        if is_duplicate(num) == 0:
            break

    print(num)
