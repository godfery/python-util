# -*- coding: UTF-8 -*-
import time
import sys
# import terminalcomman
import terminalsize

class RunBar:
    term_size = terminalsize.get_terminal_size()[1]

    def __init__(self, total_size, total_pieces=1):
        self.displayed = False
        self.total_size = total_size
        self.total_pieces = total_pieces
        self.current_piece = 1
        self.received = 0
        self.speed = ''
        self.last_updated = time.time()

        total_pieces_len = len(str(total_pieces))
        # 38 is the size of all statically known size in self.bar
        total_str = '%5s' % round(self.total_size / 1048576, 1)
        total_str_width = max(len(total_str), 5)
        self.bar_size = self.term_size - 28 - 2 * total_pieces_len \
            - 2 * total_str_width
        # self.bar = '{0:>4}%% ({1:>%s}/%sMB) ├{2:─<%s}┤[{3:>%s}/{4:>%s}] {5}' % (
        #     total_str_width, total_str, self.bar_size, total_pieces_len,
        #     total_pieces_len
        # )
        self.bar = '{0:>4}%% ({1:>%s}/%sMB) ├{2:<%s}┤[{3:>%s}/{4:>%s}] {5}' % (
            total_str_width, total_str, self.bar_size, total_pieces_len,
            total_pieces_len
        )
        # self.bar = '{0}% ({1}/953.0MB) ├{2}┤[{3}/{4}] {5}'
        # print self.bar
        # print total_str_width, total_str, self.bar_size, total_pieces_len,total_pieces_len

    def update(self):
        self.displayed = True
        bar_size = self.bar_size
        percent = round(self.received * 100 / self.total_size, 1)
        if percent >= 100:
            percent = 100
        dots = bar_size * int(percent) // 100
        plus = int(percent) - dots // bar_size * 100
        if plus > 0.8:
            plus = '█'
        elif plus > 0.4:
            plus = '>'
        else:
            plus = ''
        bar = '█' * dots + plus
        # print percent , round(self.received / 1048576, 1), bar,self.current_piece, self.total_pieces, self.speed
        bar = self.bar.format(
            percent, round(self.received / 1048576, 1), bar,
            self.current_piece, self.total_pieces, self.speed
        )
        sys.stdout.write('\r' + bar)
        sys.stdout.flush()

    def update_received(self, n):
        self.received += n
        time_diff = time.time() - self.last_updated
        bytes_ps = n / time_diff if time_diff else 0
        if bytes_ps >= 1024 ** 3:
            self.speed = '{:4.0f} GB/s'.format(bytes_ps / 1024 ** 3)
        elif bytes_ps >= 1024 ** 2:
            self.speed = '{:4.0f} MB/s'.format(bytes_ps / 1024 ** 2)
        elif bytes_ps >= 1024:
            self.speed = '{:4.0f} kB/s'.format(bytes_ps / 1024)
        else:
            self.speed = '{:4.0f}  B/s'.format(bytes_ps)
        self.last_updated = time.time()
        self.update()

    def update_piece(self, n):
        self.current_piece = n

    def done(self):
        if self.displayed:
            print()
            self.displayed = False


if __name__ == "__main__":
    bar = RunBar(10000000)
    from time import  sleep
    from random import randint

    for i in range(1000):
        bar.update_received(randint(10000,100000))
        sleep(0.3)
