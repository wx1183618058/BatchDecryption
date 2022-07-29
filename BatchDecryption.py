import logging
import os
import re
from argparse import ArgumentParser, FileType

VARS = {}


def parseVar(var, begin, size):
    if not var in VARS:
        VARS[var] = os.getenv(var)
    if 0 > begin:
        begin += len(VARS[var])
    return VARS[var][begin:begin+size]


def parseLine(line):
    result = re.match(r'@set (\S+?)=(.+)', line)
    if result:
        VARS[result.groups()[0]] = result.groups()[1].replace('^^^', '^')


def parseCommand(command):
    _command = ''
    _line = ''
    prog = re.compile(r'%(\S+?):~(\S+?),(\S+?)%')
    while command:
        # 解密命令字符
        char = ''
        end = command.find('%', 1) + 1
        result = prog.match(command[:end])
        if result:
            var, begin, size = result.groups()
            try:
                char = parseVar(var, int(begin), int(size))
            except Exception as e:
                char = command[:end]
                logging.error('%s %s', e, command[:end])
            command = command[result.end():]
        else:
            char = command[:1]
            command = command[1:]
        _command += char
        _line += char
        # 分析命令行
        if '&@' in _line:
            parseLine(_line[:-2])
            _line = _line[len(_line)-1:]
    return _command


if __name__ == '__main__':
    # 对命令行进行解析
    parser = ArgumentParser()
    parser.add_argument('-i', required=True, type=FileType('rb'))
    parser.add_argument('-o', required=True, type=FileType('wb'))
    args = parser.parse_args()
    print('作者：欲断魂')
    print('仅供学习交流，严禁用于商业用途，请于24小时内删除')

    flag = b'::BatchEncryption Build 201610 By gwsbhqt@163.com'
    command = args.i.read()
    if flag in command:
        command = command[command.find(flag) + len(flag):]
        command = parseCommand(command.decode(encoding='gbk'))
        args.o.write(command.encode(encoding='gbk'))
