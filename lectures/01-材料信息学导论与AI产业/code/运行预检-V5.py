# -*- coding: utf-8 -*-
"""第 1 讲 学生运行预检（保护入口，V5）。

用法（在第 1 讲包根执行，普通 python，单行即可）：
    python "code/运行预检-V5.py" --out "学生运行/首次预检"
    python "code/运行预检-V5.py" --out "学生运行/1-读取"   --step read
    python "code/运行预检-V5.py" --out "学生运行/2-换算"   --step summary
    python "code/运行预检-V5.py" --out "学生运行/3-结果图" --step figure
    python "code/运行预检-V5.py" --out "学生运行/4-版本"   --step version

边界（写入前检查，不靠删除重试）：
  * 允许：包根下全新目录，例如 学生运行/首次预检（父目录可不存在）；
  * 拒绝：已存在目录（含空目录）、包根本身、包外路径、code/ 内任何位置、
    以及 课程导论/、assets/、学生分发-V5/、.cache/ 等受保护材料目录内的目标。

行为：
  1) 复制冻结核心 `环境验收.py` 与 `带隙小样本.csv` 到目标目录下的 `work/`；
  2) 在副本目录内执行 all（四步）或指定单步；
  3) 只写本次目标目录；不改源、不覆盖既有输出；
  4) 兼容 Windows 默认 GBK 控制台：子进程统一 UTF-8 捕获，日志以 UTF-8 落盘，
     屏幕只打安全摘要，用户无需 -X utf8；
  5) 校验冻结文件 SHA；不符即拒绝，不执行。

单步语义：`--step read/summary/version` 只核该步真实输出（不要求 SVG）；
`--step figure` 与默认 all 额外核对新生成的 SVG 与冻结示例逐字节一致。

退出码：0 成功；2 参数/目标/校验错误；3 运行或写盘失败。
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

VERSION = 'lec1-preflight-runner-v2'
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / '环境验收'
CORE = SRC / '环境验收.py'
CSV = SRC / '带隙小样本.csv'
SVG = SRC / '输出' / 'lec1_env_check.svg'
SELF = Path(__file__).resolve()
EXPECT = {
    'core': '1e47550633f8742ab21e2a530beff7ce746b626988e551b3483586d1e70a05c0',
    'csv': 'b089f06ebde74ee9257c8a4b2d99d519407ea7ef18d727d4c5a1a315b71b74e0',
    'svg': '7685277e46c85811199a6e1b579db8d537c9545bb3f9cfc007ff053dee7f11d8',
}
STEPS = ['read', 'summary', 'figure', 'version']
NEED_SVG = ('all', 'figure')
PROTECTED_DIRS = {'code', '课程导论', 'assets', '学生分发-V5', '.cache'}


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def say(msg):
    """GBK 控制台安全输出：编码失败时降级为可用字符。"""
    try:
        print(msg)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or 'gbk'
        print(msg.encode(enc, 'replace').decode(enc, 'replace'))


def fail(msg, code=2):
    say('[预检入口] ' + msg)
    return code


def protected(path: Path):
    """受保护目标：包外、包根本身、code/ 内、受保护材料目录内。"""
    p = path.resolve()
    root = ROOT.resolve()
    try:
        rel = p.relative_to(root)
    except ValueError:
        return '目标应在第1讲包根之内'
    if p == root:
        return '不能用包根本身作为输出目录'
    if rel.parts and rel.parts[0].lower() in {x.lower() for x in PROTECTED_DIRS}:
        return '目标不能写进受保护目录：%s/' % rel.parts[0]
    return ''


def main(argv=None):
    ap = argparse.ArgumentParser(description='第1讲 学生运行预检（保护入口）')
    ap.add_argument('--out', required=True, help='全新输出目录，例如 学生运行/首次预检')
    ap.add_argument('--step', default='all', choices=['all'] + STEPS)
    args = ap.parse_args(argv)

    out = Path(args.out)
    why = protected(out)
    if why:
        return fail('%s：%s' % (why, out.resolve()))
    if out.exists():
        return fail('目标已存在（含空目录），请换新目录：%s' % out)

    for key, p in (('core', CORE), ('csv', CSV), ('svg', SVG)):
        if not p.exists():
            return fail('缺冻结文件：%s' % p)
        if sha(p) != EXPECT[key]:
            return fail('冻结文件 SHA 不符，拒绝执行：%s' % p)

    try:
        out.mkdir(parents=True)
    except OSError as exc:
        return fail('无法创建目标目录：%s' % exc, 3)
    work = out / 'work'
    logs = out / 'logs'
    try:
        work.mkdir()
        logs.mkdir()
        shutil.copyfile(CORE, work / '环境验收.py')
        shutil.copyfile(CSV, work / '带隙小样本.csv')
    except OSError as exc:
        return fail('复制冻结核心失败：%s' % exc, 3)

    steps = STEPS if args.step == 'all' else [args.step]
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONUTF8'] = '1'
    records = []
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S')
    for step in steps:
        cmd = [sys.executable, '环境验收.py', '--step', step]
        p = subprocess.run(cmd, cwd=str(work), capture_output=True, env=env)
        out_txt = p.stdout.decode('utf-8', 'replace')
        err_txt = p.stderr.decode('utf-8', 'replace')
        (logs / ('%s.log' % step)).write_text(
            '$ ' + ' '.join(cmd) + '\n[exit] %d\n--- stdout ---\n%s\n--- stderr ---\n%s'
            % (p.returncode, out_txt, err_txt), encoding='utf-8')
        say('[%s] exit=%d' % (step, p.returncode))
        rec = {'step': step, 'command': ' '.join(cmd), 'exit': p.returncode,
               'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
               'log': 'logs/%s.log' % step}
        records.append(rec)
        if p.returncode != 0:
            return fail('步骤失败：%s（详见 %s）' % (step, logs / ('%s.log' % step)), 3)
        # 单步只核该步真实输出；不额外跑其它步、不伪造 SVG
        need = {'read': ('行数：', '列数：'), 'summary': ('最大偏差',),
                'version': ('Python：', '平台  ：')}.get(step, ())
        for key in need:
            if key not in out_txt:
                return fail('步骤 %s 输出缺少预期字段：%s' % (step, key), 3)
        rec['checked'] = list(need) or (['输出/lec1_env_check.svg'] if step in NEED_SVG else [])

    svg_run = work / '输出' / 'lec1_env_check.svg'
    if args.step in NEED_SVG:
        if not svg_run.exists():
            return fail('未生成输出/lec1_env_check.svg', 3)
        if sha(svg_run) != EXPECT['svg']:
            return fail('生成 SVG 与冻结示例 SHA 不符：%s' % svg_run, 3)

    wf = {
        'runner': VERSION,
        'entry': {'path': str(SELF), 'sha256': sha(SELF), 'bytes': SELF.stat().st_size},
        'task': '第1讲 学生独立预检：读 CSV / 换算复核 / 看 SVG / 记录版本',
        'interpreter': sys.version.split()[0],
        'platform': platform.platform(),
        'started': t0,
        'finished': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'out_dir': str(out.resolve()),
        'mode': 'all' if args.step == 'all' else ('single:' + args.step),
        'source': {'core': {'path': str(CORE), 'sha256': sha(CORE), 'bytes': CORE.stat().st_size},
                   'csv': {'path': str(CSV), 'sha256': sha(CSV), 'bytes': CSV.stat().st_size},
                   'svg_example': {'path': str(SVG), 'sha256': sha(SVG), 'bytes': SVG.stat().st_size}},
        'copies': {'core': sha(work / '环境验收.py'), 'csv': sha(work / '带隙小样本.csv')},
        'steps': records,
        'output_svg': ({'path': str(svg_run), 'sha256': sha(svg_run), 'bytes': svg_run.stat().st_size}
                       if svg_run.exists() else None),
        'network': 'none', 'third_party': 'none',
    }
    (out / 'workflow.json').write_text(json.dumps(wf, ensure_ascii=False, indent=1) + '\n',
                                      encoding='utf-8')
    say('完成：%d 步；输出目录 %s' % (len(steps), out.resolve()))
    say('记录：%s' % (out / 'workflow.json'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
