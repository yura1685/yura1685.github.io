import sys, atexit, builtins

class FastIO:
    __slots__ = ('_nt', '_out')

    def __init__(self):
        self._nt = iter(sys.stdin.buffer.read().split()).__next__
        self._out = []
        atexit.register(self.flush)

    # ---- 入力 ----
    def input(self):
        try:
            return self._nt().decode()
        except StopIteration:
            raise EOFError from None

    def II(self): return int(self._nt())
    def LI(self, n):
        nt = self._nt
        return [int(nt()) for _ in range(n)]
    def LLI(self, h, w): return [self.LI(w) for _ in range(h)]
    SI = input

    # ---- 出力 ----
    def print(self, *args, sep=' ', end='\n', file=None, flush=False):
        if file is not None and file is not sys.stdout:
            builtins.print(*args, sep=sep, end=end, file=file, flush=flush)
            return
        self._out.append((str(args[0]) if len(args) == 1 else sep.join(map(str, args))) + end)
        if flush:
            self.flush()

    def flush(self):
        if self._out:
            sys.stdout.write(''.join(self._out))
            self._out.clear()
        sys.stdout.flush()

io = FastIO()
input, print = io.input, io.print
II, LI, LLI, SI = io.II, io.LI, io.LLI, io.SI

#--yura1685--yura1685--yura1685--yura1685--yura1685--yura1685--yura1685--yura1685--yura1685--yura1685--#
