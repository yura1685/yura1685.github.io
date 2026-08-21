# Pythonでラグランジュ補間を実装する

多項式補間とは，いくつかの点 $(x_0,y_0),(x_1,y_1),\ldots,(x_d,y_d)$ が与えられたとき，それらをすべて通る多項式を求める問題です．$x_0,x_1,\ldots,x_d$ が互いに異なるならば，これら $d+1$ 点を通る $d$ 次以下の多項式は一意に定まります．

もちろん，$$f(x)=a_dx^d+a_{d-1}x^{d-1}+\cdots+a_1x+a_0$$ と置いて連立方程式を解くこともできますが，ラグランジュ補間を使えば係数 $a_0,a_1,\ldots,a_d$ を求めなくても，与えられた $x$ における $f(x)$ の値を求めることができます．

## 連立方程式で求めてみる

例えば，$(0,1),(1,3),(2,7)$ の $3$ 点を通る $2$ 次以下の多項式について考えます．$f(x)=ax^2+bx+c$ と置くと，$$f(0)=c=1,\quad f(1)=a+b+c=3,\quad f(2)=4a+2b+c=7$$ という連立方程式が得られます．これを解けば，$$f(x)=x^2+x+1$$ と求められます．$3$ 点程度ならこれでも十分ですが，点の数が増えるたびに連立方程式を解くのは面倒です．そこで，ラグランジュ補間を使います．

## ラグランジュ基底

$i=0,1,\ldots,d$ に対して，$$L_i(x)=\prod_{\substack{0\le j\le d\\ j\ne i}}\frac{x-x_j}{x_i-x_j}$$ を考えます．この $L_i(x)$ は，$x=x_k$ を代入したときに非常に単純な値になります．

まず $k=i$ のとき，$$L_i(x_i)=\prod_{\substack{0\le j\le d\\ j\ne i}}\frac{x_i-x_j}{x_i-x_j}=1$$ です．一方，$k\ne i$ のときは積の中に $j=k$ の項が含まれるため，その分子が $x_k-x_k=0$ となり，$$L_i(x_k)=0$$ です．したがって，$$L_i(x_j)=\begin{cases}1 & (i=j) \\0 & (i\ne j)\end{cases}$$ を満たします．

## ラグランジュ補間

この $L_i(x)$ を使って，$$f(x)=\sum_{i=0}^{d}y_iL_i(x)$$ と定めます．$x=x_k$ を代入すると，$$f(x_k)=\sum_{i=0}^{d}y_iL_i(x_k)$$ となりますが，$L_i(x_k)$ は $i=k$ のときだけ $1$ で，それ以外では $0$ です．そのため，$$f(x_k)=y_k$$ となります．
よって，$$f(x)=\sum_{i=0}^{d}y_i\prod_{\substack{0\le j\le d\\ j\ne i}}\frac{x-x_j}{x_i-x_j}$$ とすれば，与えられたすべての点 $(x_0,y_0),(x_1,y_1),\ldots,(x_d,y_d)$ を通る $d$ 次以下の多項式が得られます．これがラグランジュ補間です．

## 具体例

先ほどの $(0,1),(1,3),(2,7)$ について実際に計算してみます．

$i=0$ のとき，$$L_0(x)=\frac{x-1}{0-1}\frac{x-2}{0-2}=\frac{(x-1)(x-2)}{2}$$

$i=1$ のとき，$$L_1(x)=\frac{x-0}{1-0}\frac{x-2}{1-2}=-x(x-2)$$

$i=2$ のとき，$$L_2(x)=\frac{x-0}{2-0}\frac{x-1}{2-1}=\frac{x(x-1)}{2}$$

です．したがって，$$f(x)=L_0(x)+3L_1(x)+7L_2(x)=x^2+x+1$$ となり，先ほど連立方程式から求めたものと一致します．

## 式をそのままPythonで実装する

まずはラグランジュ補間の式をそのまま実装してみます．

```python
def lagrange(xs, ys, x):
    n = len(xs)
    res = 0
    for i in range(n):
        t = ys[i]
        for j in range(n):
            if i == j:
                continue
            t *= (x - xs[j]) / (xs[i] - xs[j])
        res += t
    return res
```

例えば，

```python
xs = [0, 1, 2]
ys = [1, 3, 7]

print(lagrange(xs, ys, 3))
```

とすると，`13.0` が得られます．実際，先ほど求めた $f(x)=x^2+x+1$ に $x=3$ を代入すると $13$ になります．

点の個数を $N$ とすると，それぞれの $i$ に対して残りの $N-1$ 点を調べるため，時間計算量は $O(N^2)$ です．

ただし，この実装では `/` を使っているため，計算の途中から浮動小数点数になります．そのため，値が大きい場合などには丸め誤差が発生する可能性があります．（厳密に計算したい場合は`Fraction`を用いると良いです．）

## mod上で計算する

競技プログラミングでは，答えをある整数 $\mathrm{mod}$ で割った余りとして求めることがよくあります．この場合，割り算の代わりに逆元を使います．

以下では，$x_0,x_1,\ldots,x_d$ が $\mathrm{mod}$ 上で互いに異なり，各分母 $x_i-x_j$ が $\mathrm{mod}$ 上で逆元を持つものとします．特に $\mathrm{mod}$ が素数ならば，$x_i\not\equiv x_j\pmod{\mathrm{mod}}$ であれば問題ありません．

```python
def lagrange(xs, ys, x, mod):
    n = len(xs)
    res = 0
    for i in range(n):
        num = 1
        den = 1
        for j in range(n):
            if i == j:
                continue
            num = num * (x - xs[j]) % mod
            den = den * (xs[i] - xs[j]) % mod
        res += ys[i] * num * pow(den, -1, mod)
        res %= mod
    return res
```

基本的には先ほどの式と同じで，$$\frac{\displaystyle\prod_{j\ne i}(x-x_j)}{\displaystyle\prod_{j\ne i}(x_i-x_j)}$$ の分母を逆元に置き換えているだけです．この実装も時間計算量は $O(N^2\log\mathrm{mod})$ 程度になります．`pow` による逆元計算を各 $i$ について行っているためです．

## $x_i=i$ の場合

ここまでの実装は $x_0,x_1,\ldots,x_d$ がどのような値でも使える一般的なものです．一方，競技プログラミングでは，$$(0,y_0),(1,y_1),\ldots,(d,y_d)$$ のように $x_i=i$ となっているケースがよく出てきます．この場合はラグランジュ補間の式を整理することで，$f(x)$ を $O(d)$ 程度で求めることができます．

以下では $\mathrm{mod}$ は素数で，$d<\mathrm{mod}$ とします．

### 分母

$x_i=i$ なので，ラグランジュ補間の分母は，$$\prod_{0\le j\le d,\ j\ne i}(i-j)$$ です．これを $j<i$ と $j>i$ に分けると，$$\prod_{j=0}^{i-1}(i-j)=i!$$ であり，$$\prod_{j=i+1}^{d}(i-j)=(-1)(-2)\cdots(-(d-i))=(-1)^{d-i}(d-i)!$$ です．したがって，$$\prod_{0\le j\le d,\ j\ne i}(i-j)=i!(d-i)!(-1)^{d-i}$$ となります．つまり，階乗と逆階乗を前計算しておけば，分母の逆元に相当する部分を $O(1)$ で求められます．

### 分子

分子は，$$\prod_{0\le j\le d,\ j\ne i}(x-j)$$ です．これを毎回計算すると $O(d^2)$ かかってしまいます．そこで，$$P_i=\prod_{j=0}^{i-1}(x-j)$$ と，$$Q_i=\prod_{j=i+1}^{d}(x-j)$$ をあらかじめ求めます．すると，$$ \prod_{0\le j\le d,\ j\ne i}(x-j)=P_iQ_i$$ となります．$P_i$ は左から，$Q_i$ は右から累積積を取れば，それぞれ全体で $O(d)$ で計算できます．

以上より，ラグランジュ補間の式は，$$f(x)=\sum_{i=0}^{d}y_iP_iQ_i\frac{(-1)^{d-i}}{i!(d-i)!}$$ と書けます．

## $O(d)$ での実装

これをそのまま実装すると次のようになります．

```python
def lagrange(ys, x, mod):
    d = len(ys) - 1
    x %= mod

    if x <= d:
        return ys[x] % mod

    pre = [1] * (d + 2)
    for i in range(d + 1):
        pre[i + 1] = pre[i] * (x - i) % mod

    suf = [1] * (d + 2)
    for i in range(d, -1, -1):
        suf[i] = suf[i + 1] * (x - i) % mod

    fact = [1] * (d + 1)
    for i in range(1, d + 1):
        fact[i] = fact[i - 1] * i % mod

    invfact = [1] * (d + 1)
    invfact[d] = pow(fact[d], mod - 2, mod)
    for i in range(d, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    ans = 0
    for i in range(d + 1):
        num = pre[i] * suf[i + 1] % mod
        term = ys[i] * num % mod
        term = term * invfact[i] % mod
        term = term * invfact[d - i] % mod
        if (d - i) & 1:
            term = -term
        ans += term

    return ans % mod
```

`pre[i]` が，$$\prod_{j=0}^{i-1}(x-j)$$ を表し，`suf[i + 1]` が，$$\prod_{j=i+1}^{d}(x-j)$$ を表しています．そのため，

```python
num = pre[i] * suf[i + 1] % mod
```

によって，ラグランジュ補間の分子を $O(1)$ で求めることができます．また，

```python
term = term * invfact[i] % mod
term = term * invfact[d - i] % mod
```

が，$$\frac{1}{i!(d-i)!}$$ に対応しています．最後に，$(-1)^{d-i}$ を，

```python
if (d - i) & 1:
    term = -term
```

で処理しています．

`pre`，`suf`，階乗，逆階乗はいずれも $O(d)$ で計算でき，逆階乗を求めるための `pow` が $O(\log\mathrm{mod})$ なので，全体の時間計算量は，$$O(d+\log\mathrm{mod})$$ です．空間計算量は $O(d)$ です．