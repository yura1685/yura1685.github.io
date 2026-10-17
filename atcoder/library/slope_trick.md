---
title: Slope Trick
category: DP
description: 区分線形な凸関数を 2 つのヒープで持ち、$\max(0, x - a)$ や $\lvert x - a \rvert$ を足す・累積 min をとる・平行移動するといった操作を $O(\log N)$ で行う
order: 7
---

傾きが整数で、整数の点でだけ折れ曲がる凸関数 $f(x)$ を、「最小値」「最小値をとる区間より左で、傾きが 1 ずつ変わる点の集合 $L$」「右で傾きが 1 ずつ変わる点の集合 $R$」で表します。 $L$ と $R$ をヒープで持つと、DP の遷移でよく出る操作がそれぞれ $O(\log N)$ でできます（ $N$ は足した関数の個数）。最初は $f(x) = 0$ です。

- `add_all(a)`: $f(x) \gets f(x) + a$。 $O(1)$
- `add_x_minus_a(a)`: $f(x) \gets f(x) + \max(0, x - a)$
- `add_a_minus_x(a)`: $f(x) \gets f(x) + \max(0, a - x)$
- `add_abs(a)`: $f(x) \gets f(x) + \lvert x - a \rvert$
- `clear_right()`: $f(x) \gets \min_{y \le x} f(y)$（右側を平らにする）。 $O(1)$
- `clear_left()`: $f(x) \gets \min_{y \ge x} f(y)$（左側を平らにする）。 $O(1)$
- `shift(a, b)`: $f(x) \gets \min_{x - b \le y \le x - a} f(y)$（ $a \le b$）。`shift(a)` は $f(x) \gets f(x - a)$ の平行移動。 $O(1)$
- `min_f`: $f$ の最小値
- `top_l()`, `top_r()`: $f$ が最小になる $x$ の区間の左端と右端（端がなければ $\mp \mathrm{INF}$）。 $O(1)$
- `get(x)`: $f(x)$。ヒープの中身を全部見るので $O(N)$

例（数列 $a$ の各項を変えて広義単調増加にするときの、変化量 $\sum \lvert a_i - b_i \rvert$ の最小値）: $f_i(x)$ を「 $b_i = x$ のときの最小値」とすると、 $f_i(x) = \min_{y \le x} f_{i - 1}(y) + \lvert x - a_i \rvert$ です。

```python
st = SlopeTrick()
for x in a:
    st.clear_right()
    st.add_abs(x)
print(st.min_f)
```
