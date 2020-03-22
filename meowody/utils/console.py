class FontColor(object):
    Black = 30   # 黑
    Red = 31     # 红
    Green = 32   # 绿
    Yellow = 33  # 黄
    Blue = 34    # 蓝色
    Purple = 35     # 紫色
    DarkGreen = 36  # 深绿
    White = 37      # 白色


class BackgroundColor(object):
    Black = 40  # 黑色背景
    Red = 41    # 红色背景
    Green = 42  # 绿色背景
    Brown = 43  # 棕色背景
    Blue = 44   # 蓝色背景
    Pink = 45   # 品红背景
    Blue2 = 46  # 孔雀蓝背景
    White = 47  # 白色背景


class ConsoleLine(object):
    def __init__(self):
        self.line = ''

    def append(self, msg, fc=None, bc=None):
        prefix = ''
        if fc is not None:
            prefix += '\033[{}m'.format(fc)
        if bc is not None:
            prefix += '\033[{}m'.format(bc)

        suffix = '\033[0m' if prefix != '' else ''
        self.line += prefix + msg + suffix

    def flush(self, end='\n'):
        print(self.line, end=end)
