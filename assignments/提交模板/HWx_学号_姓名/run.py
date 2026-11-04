# -*- coding: utf-8 -*-
"""HW_ 运行入口（骨架，按需改写）

保留三件事，其余随便改：
  1. 固定随机种子
  2. 日志同时写控制台与 outputs/run.log
  3. 图与表一律存 outputs/

用法：python run.py
"""
import logging
import random
import sys
from pathlib import Path

import numpy as np

SEED = 20261104          # 用教师公布的统一种子，不要自行更换
OUT = Path(__file__).parent / "outputs"
OUT.mkdir(exist_ok=True)


def setup_log():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(OUT / "run.log", mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("hw")


def main():
    log = setup_log()
    random.seed(SEED)
    np.random.seed(SEED)
    log.info("seed=%d", SEED)

    # ---- 你的分析写在这里 ----------------------------------------------
    # 读 data/ 下的数据 → 处理 → 建模 → 评估
    # 关键中间量都用 log.info 打出来，这些就是复现证据
    log.info("数据条目数=%d", 0)

    # 图：存 outputs/，图注写清单位与条件
    # import matplotlib
    # matplotlib.use("Agg")
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    # ...
    # fig.savefig(OUT / "fig_xxx.png", bbox_inches="tight")
    # log.info("已保存 fig_xxx.png")

    # 表：CSV 存 outputs/
    # pd.DataFrame(...).to_csv(OUT / "tbl_xxx.csv", index=False, encoding="utf-8-sig")

    log.info("完成")


if __name__ == "__main__":
    main()
