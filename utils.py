import random
import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # strftime 把 unix time 转换为日常看到的格式
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)


def random_string():
    """
    生成一个长度16的随机字符串
    """
    seed = 'Rk3N8DNhuhIN2dfbT4rw'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 1)
        s += seed[random_index]
    return s
