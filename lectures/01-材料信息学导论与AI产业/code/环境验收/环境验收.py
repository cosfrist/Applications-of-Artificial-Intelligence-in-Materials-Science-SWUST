# -*- coding: utf-8 -*-
"""第 1 讲课堂实践：基础 Python 预检（15 分钟）

只依赖 Python 标准库，不安装任何包。四步分别验证：

    python 环境验收.py --step read      1) 能读取 CSV，报行列与缺失
    python 环境验收.py --step summary   2) 能核对单位换算（eV ↔ J）
    python 环境验收.py --step figure    3) 能生成并保存一张带标注的结果图（SVG）
    python 环境验收.py --step version   4) 能登记解释器与平台版本
    python 环境验收.py                  依次执行以上四步

注意：本脚本只做「Python 能读、能算、能存图、能记版本」的基础预检，
不代表 numpy / pandas / scikit-learn / matplotlib 等课程依赖已就绪；
后者按《MICourse 课前环境清单》单独验收。

输出写入本脚本同级的「输出」目录：输出/lec1_env_check.svg
"""
import argparse
import csv
import os
import platform
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, '带隙小样本.csv')
OUT_DIR = os.path.join(HERE, '输出')
J_PER_EV = 1.602176634e-19          # 1 eV 的精确定义值
NOTE = '教学取整数据，仅用于流程演示'    # 图上必须写明的说明


def read_rows():
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def step_read(rows):
    cols = list(rows[0].keys())
    print('  文件：', os.path.relpath(CSV_PATH, HERE))
    print('  行数：', len(rows), '　列数：', len(cols))
    print('  列名：', ' | '.join(cols))
    for c in cols:
        miss = sum(1 for r in rows if r[c].strip() == '')
        if miss:
            print(f'  缺失：{c} 缺 {miss} 行')


def step_summary(rows):
    pairs = [(r['id'], r['formula'], float(r['bandgap_eV']), float(r['bandgap_J']))
             for r in rows if r['bandgap_eV'].strip() and r['bandgap_J'].strip()]
    if not pairs:
        print('  没有同时含 eV 与 J 的行，跳过换算核对')
        return
    dev = [abs(j / J_PER_EV - e) for _, _, e, j in pairs]
    print(f'  同时含两单位的记录：{len(pairs)} 条')
    print(f'  最大偏差：{max(dev):.4f} eV（应远小于 0.01 eV）')
    for pid, f, e, j in pairs[:3]:
        print(f'    {pid} {f}: {e} eV ↔ {j:.4g} J → {j / J_PER_EV:.4f} eV')


def _esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def step_figure(rows):
    """画带样本名、数值刻度与说明的条形图，存为标准库生成的 SVG。"""
    data = [(r['formula'], float(r['bandgap_eV']))
            for r in rows if r['bandgap_eV'].strip()]
    W, H = 860, 460
    L, R, T, B = 78, 30, 74, 96
    ymax = 10.0
    plot_w, plot_h = W - L - R, H - T - B
    bw = plot_w / len(data)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="Microsoft YaHei, SimHei, sans-serif">',
           f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
           f'<text x="{L}" y="34" font-size="20" fill="#0E3F8C" '
           f'font-weight="bold">小样本带隙分布（{NOTE}）</text>',
           f'<text x="{L}" y="56" font-size="13" fill="#5D6E85">'
           f'样本数 n = {len(data)}；纵轴为带隙 / eV</text>']

    step, v = 2, 0.0
    while v <= ymax + 1e-9:
        y = T + plot_h - plot_h * v / ymax
        svg.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L + plot_w}" y2="{y:.1f}" '
                   f'stroke="#E3E9F2" stroke-width="1"/>')
        svg.append(f'<text x="{L - 10}" y="{y + 4:.1f}" font-size="12" '
                   f'fill="#3A4759" text-anchor="end">{v:g}</text>')
        v += step
    svg.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{T + plot_h}" '
               f'stroke="#3A4759" stroke-width="1.5"/>')
    svg.append(f'<line x1="{L}" y1="{T + plot_h}" x2="{L + plot_w}" '
               f'y2="{T + plot_h}" stroke="#3A4759" stroke-width="1.5"/>')
    svg.append(f'<text x="18" y="{T + plot_h / 2:.0f}" font-size="13" fill="#3A4759" '
               f'transform="rotate(-90 18 {T + plot_h / 2:.0f})" text-anchor="middle">'
               f'带隙 / eV</text>')

    for i, (name, val) in enumerate(data):
        x = L + bw * i + bw * 0.18
        w = bw * 0.64
        h = plot_h * val / ymax
        y = T + plot_h - h
        color = '#0E3F8C' if i % 2 == 0 else '#1E4FA8'
        svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                   f'fill="{color}" rx="2"/>')
        svg.append(f'<text x="{x + w / 2:.1f}" y="{y - 6:.1f}" font-size="11" '
                   f'fill="#0B1B33" text-anchor="middle">{val:g}</text>')
        svg.append(f'<text x="{x + w / 2:.1f}" y="{T + plot_h + 18:.0f}" font-size="11" '
                   f'fill="#3A4759" text-anchor="middle">{_esc(name)}</text>')

    svg.append(f'<text x="{L}" y="{H - 30}" font-size="12" fill="#B3261E">'
               f'{NOTE}：数值取整自常见文献量级，只用于检查「能读、能算、能存图」这条链路，'
               f'不得作为数据引用。</text>')
    svg.append(f'<text x="{L}" y="{H - 12}" font-size="11" fill="#8B97A8">'
               f'生成：环境验收.py（Python 标准库）；数据：带隙小样本.csv</text>')
    svg.append('</svg>')

    out = os.path.join(OUT_DIR, 'lec1_env_check.svg')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(svg))
    print('  已保存：', os.path.relpath(out, HERE))
    print('  查看方式：用浏览器（Edge/Chrome）双击或拖入即可打开')


def step_version():
    print('  Python：', platform.python_version(), '|', platform.architecture()[0])
    print('  平台  ：', platform.platform())
    print('  脚本  ：', os.path.basename(__file__), '（仅标准库，无第三方依赖）')


def main():
    ap = argparse.ArgumentParser(description='第 1 讲 基础 Python 预检')
    ap.add_argument('--step', default='all',
                    choices=['all', 'read', 'summary', 'figure', 'version'])
    args = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = read_rows()

    if args.step in ('all', 'read'):
        print('[1/4] 读取 CSV')
        step_read(rows)
    if args.step in ('all', 'summary'):
        print('[2/4] 单位换算核对（1 eV = 1.602176634e-19 J）')
        step_summary(rows)
    if args.step in ('all', 'figure'):
        print('[3/4] 生成结果图')
        step_figure(rows)
    if args.step in ('all', 'version'):
        print('[4/4] 登记版本')
        step_version()
    if args.step == 'all':
        print('基础预检四步已完成；课程依赖（numpy/pandas/scikit-learn/matplotlib）'
              '另按《MICourse 课前环境清单》验收。')


if __name__ == '__main__':
    main()
