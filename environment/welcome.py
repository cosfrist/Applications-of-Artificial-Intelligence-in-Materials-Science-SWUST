#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MICourse 环境启动横幅与自检提示
================================

由 `进入MICourse环境.bat` 调用。把中文输出放在 Python 侧，是因为 Windows 批处理
文件里的中文受代码页影响极易乱码，而 Python 能按控制台实际代码页正确编码输出。

不依赖任何第三方包（避免环境本身有问题时连提示都打不出来）。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

BANNER = r"""
================================================================
  MICourse 课程环境  |  《AI 在材料科学中的应用》
  西南科技大学 材料与化学学院      何刚  NNIP LAB @ SWUST
================================================================

  Python  {py}
  路径    {exe}
  用户包隔断  PYTHONNOUSERSITE={pnu}   （=1 表示已隔断，正确）

  常用命令
    python 你的脚本.py          运行单个脚本
    jupyter lab                 打开 Notebook（内核选 MICourse）
    python -c "import numpy; print(numpy.__version__)"

  提示
    · 脚本的输出目录不要放在坚果云 / OneDrive 同步盘里，
      同步客户端会占用目录句柄，导致脚本最后一步“发布目录”失败。
    · 本环境全部 CPU 可完成，torch.cuda.is_available() 返回 False 属正常。

  环境自检（可选，约 30 秒）
    python "{verify}"
================================================================
"""


def main() -> int:
    here = Path(__file__).resolve().parent
    exe = sys.executable
    py = sys.version.split()[0]
    pnu = os.environ.get("PYTHONNOUSERSITE", "(未设置)")

    # 中文窗口标题用 Python 设置：批处理里写中文会受代码页影响，这里没有该风险
    try:
        import ctypes

        ctypes.windll.kernel32.SetConsoleTitleW("MICourse - AI在材料科学中的应用")
    except Exception:  # noqa: BLE001
        pass

    text = BANNER.format(py=py, exe=exe, pnu=pnu, verify=here / "verify_env.py")
    # 显式按控制台代码页输出；失败则退回 replace，保证不因编码崩掉
    try:
        print(text)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(text.encode(enc, errors="replace").decode(enc, errors="replace"))

    # 快速校验三件事：解释器是不是环境内的、关键包在不在、用户包有没有漏进来
    problems: list[str] = []
    if "MICourse" not in exe:
        problems.append(f"解释器不在 MICourse 环境内：{exe}")
    try:
        import numpy
        import pandas
        import sklearn
    except Exception as exc:  # noqa: BLE001
        problems.append(f"关键包导入失败：{type(exc).__name__}: {exc}")
    else:
        print(f"  依赖自检    numpy {numpy.__version__} | pandas {pandas.__version__}"
              f" | scikit-learn {sklearn.__version__}")
    if pnu != "1":
        problems.append("PYTHONNOUSERSITE 未设为 1，用户级旧包可能遮盖环境包")

    if problems:
        print("\n  [注意] 检测到以下问题：")
        for p in problems:
            print(f"    - {p}")
        print()
    else:
        print("\n  [就绪] 环境检查通过，可以开始。\n")

    # 供批处理判断（当前不强制使用，留作以后扩展）
    return 0 if not problems else 3


if __name__ == "__main__":
    sys.exit(main())
