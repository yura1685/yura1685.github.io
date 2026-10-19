class XorBasis:
    def __init__(self):
        self.basis = []  # どの 2 つも最上位ビットが異なる

    def add(self, x):
        # x を加える。x が今の基底の XOR で作れなかったら True
        for b in self.basis:
            x = min(x, x ^ b)
        if x == 0:
            return False
        self.basis.append(x)
        return True

    def can_make(self, x):
        # x が基底のいくつかの XOR で作れるか（何も選ばないと 0）
        return self.min_xor(x) == 0

    def min_xor(self, x):
        # x に基底のいくつかを XOR してできる最小値
        for b in self.basis:
            x = min(x, x ^ b)
        return x

    def max_xor(self, x=0):
        # x に基底のいくつかを XOR してできる最大値
        for b in sorted(self.basis, reverse=True):
            x = max(x, x ^ b)
        return x

    def __len__(self):
        return len(self.basis)
