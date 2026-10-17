---
title: 点と直線・線分の距離
category: 幾何
description: 点と直線、点と線分、線分と線分の距離を、内積と外積を使って求める
order: 4
---

点 $p$ と直線 $ab$ の距離は、外積を使って $\lvert \overrightarrow{ab} \times \overrightarrow{ap} \rvert / \lvert \overrightarrow{ab} \rvert$ で求まります。線分の場合は、 $p$ から下ろした垂線の足が線分の外に出るとき（内積の符号で判定）は、近い方の端点までの距離になります。

- `cross(a, b, c)`, `dot(a, b, c)`: ベクトル $\overrightarrow{ab}$ と $\overrightarrow{ac}$ の外積と内積
- `dist_point_line(p, a, b)`: 点 $p$ と直線 $ab$（ $a \ne b$）の距離
- `dist_point_segment(p, a, b)`: 点 $p$ と線分 $ab$ の距離
- `dist_segment_segment(a, b, c, d)`: 線分 $ab$ と線分 $cd$ の距離（交わるなら $0$）

点はタプル `(x, y)` で表します。距離は浮動小数点数で返し、計算量はどれも $O(1)$ です。
