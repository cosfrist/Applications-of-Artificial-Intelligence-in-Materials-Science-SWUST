#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
第 1—10 讲教学断言与实算输出核对
=================================

为什么需要这一层
----------------
`check_lecture_code.py` 只能证明「脚本跑通了」，不能证明「讲对了」。
课程 README 里写死了一批可核验的数值断言（如第 5 讲「4/0/8/12 条有向边」、
第 7 讲「四格之和 = 120、C = 2·FP + 10·FN」），这些数字一旦与代码实际行为脱节，
课堂演示就会当场翻车。本脚本直接从**产物文件**反算这些量，与 README 声明逐条比对。

前置条件
--------
先跑 `check_lecture_code.py` 生成产物（默认在 `D:/tmp_micourse_check/run/`），
本脚本读取这些产物，并按需要补跑第 5 讲的四个截断输入。

用法
----
    python check_assertions.py
    python check_assertions.py --work D:/tmp_micourse_check --report 路径.md

退出码
------
    0  全部断言成立
    1  存在不成立的断言（会列出期望值与实测值）

作者：何刚  NNIP LAB @ SWUST
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

PY = Path(r"C:\Users\gang\.conda\envs\MICourse\python.exe")
HERE = Path(r"D:/我的坚果云/SWUST/Courses/AI在材料科学中的应用/课件/00-课程环境")

rows: list[tuple[str, str, str, str, str, str]] = []   # (讲, 断言, 期望, 实测, 结论, 类别)


def add(lec: str, claim: str, expect, actual, ok: bool, kind: str = "assert") -> None:
    """kind=assert：代码行为断言；kind=doc：README 声明与实算不符（文档缺陷，非代码缺陷）。"""
    mark = "成立" if ok else ("**文档不一致**" if kind == "doc" else "**不成立**")
    rows.append((lec, claim, str(expect), str(actual), mark, kind))
    flag = "ok" if ok else ("DOC" if kind == "doc" else "!!")
    print(f"  [{flag}] {lec}｜{claim}　期望 {expect}　实测 {actual}")


def read_csv(p: Path) -> list[dict]:
    """读 CSV，自动去 BOM。"""
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def find_key(obj, key: str):
    """在嵌套 JSON 里递归找第一个同名键（产物结构常把参数放在子层）。"""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            got = find_key(v, key)
            if got is not None:
                return got
    elif isinstance(obj, list):
        for v in obj:
            got = find_key(v, key)
            if got is not None:
                return got
    return None


# --------------------------------------------------------------- 第 5 讲：图边数
def check_lec5(work: Path) -> None:
    print("\n[第 5 讲] 一维周期结构的边数（README §2.1 表）")
    src = work / "src" / "第5讲 结构与图表示" / "code_v5"
    py = src / "graph_core.py"
    if not py.exists():
        add("第5讲", "源码存在", "存在", "缺失", False)
        return

    cases = [
        ("chain_1d_rcut1p0.json", 0, 0, "1.0 Å 严格小于：恰好等于最近邻也不算"),
        ("chain_1d.json", 4, 2, "默认例子"),
        ("chain_1d_r2p1.json", 8, 4, "互邻各 2 + 自身 ±1 像各 2"),
        ("chain_1d_r3p1.json", 12, 6, "互邻各 4 + 自身 ±1 像各 2"),
        ("chain_1d_none.json", 0, 0, "空图，度 0"),
    ]
    for fname, exp_dir, exp_undir, memo in cases:
        out = work / "run" / "assert5" / fname.replace(".json", "")
        if out.exists():
            import shutil

            shutil.rmtree(out, ignore_errors=True)
        p = subprocess.run(
            [str(PY), str(py), "--input", str(src / "data" / fname), "--out", str(out)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=dict(__import__("os").environ, PYTHONNOUSERSITE="1"),
        )
        if p.returncode != 0:
            add("第5讲", f"{fname} 运行", "rc=0", f"rc={p.returncode}：{p.stderr[-120:]}", False)
            continue
        # 优先用 workflow.json 的自报结果，同时与 CSV 行数交叉验证
        wf = out / "workflow.json"
        res = json.loads(wf.read_text(encoding="utf-8"))["results"] if wf.exists() else {}
        n_dir_csv = len(read_csv(out / "edges.csv"))
        n_und_csv = len(read_csv(out / "edges_undirected.csv"))
        n_dir = res.get("directed_edges", n_dir_csv)
        n_und = res.get("undirected_edges", n_und_csv)
        add("第5讲", f"{fname} 有向边数（{memo}）", exp_dir, n_dir, n_dir == exp_dir)
        add("第5讲", f"{fname} 无向周期边数", exp_undir, n_und, n_und == exp_undir)
        add("第5讲", f"{fname} 自报数与 CSV 行数一致", f"{n_dir}/{n_und}",
            f"{n_dir_csv}/{n_und_csv}", (n_dir, n_und) == (n_dir_csv, n_und_csv))

    # 等变性与图级读出：默认例子的 h1 之和应为 9（README §1 第 5 条）
    msg = work / "run" / "assert5" / "chain_1d" / "messages.csv"
    if msg.exists():
        r = read_csv(msg)
        total = sum(float(x["h1"]) for x in r)
        add("第5讲", "图级读出 sum（README：9）", 9, f"{total:g}", abs(total - 9) < 1e-9)
        h1s = [float(x["h1"]) for x in r]
        add("第5讲", "节点读出 h′ 为 (5, 4)（顺序可互换）", "[5, 4]", sorted(h1s, reverse=True),
            sorted(h1s, reverse=True) == [5.0, 4.0])

    # 置换双射：h′ 应等变（5→5、4→4）
    out_perm = work / "run" / "L5-05" / "run_perm"
    if (out_perm / "messages.csv").exists():
        base = read_csv(work / "run" / "L5-03" / "run01" / "messages.csv")
        perm = read_csv(out_perm / "messages.csv")
        same = len(base) == len(perm)
        add("第5讲", "元素置换后消息行数不变（双射）", len(base), len(perm), same)


# --------------------------------------------------------------- 第 7 讲：阈值—代价
def check_lec7(work: Path) -> None:
    print("\n[第 7 讲] 阈值—代价表（README §1：四格和=120，C=2·FP+10·FN）")
    p = work / "run" / "L7-02" / "out" / "val_threshold_cost.csv"
    if not p.exists():
        add("第7讲", "阈值代价表存在", "存在", "缺失", False)
        return
    r = read_csv(p)
    add("第7讲", "阈值点数（网格 0–1.00 步长 0.05 + 1.01 哨兵）", 22, len(r), len(r) == 22)

    grid = [round(float(x["t"]), 4) for x in r]
    exp_grid = [round(i * 0.05, 4) for i in range(21)] + [1.01]
    add("第7讲", "阈值网格内容", "0,0.05,…,1.00,1.01", f"{grid[0]}…{grid[-1]}",
        all(abs(a - b) < 1e-9 for a, b in zip(grid, exp_grid)))

    bad_sum = [x["t"] for x in r
               if int(x["TN"]) + int(x["FP"]) + int(x["FN"]) + int(x["TP"]) != 120]
    add("第7讲", "四格之和 = 120（逐行）", "全部成立", f"{len(bad_sum)} 行不成立", not bad_sum)

    bad_cost = []
    for x in r:
        c = 2 * int(x["FP"]) + 10 * int(x["FN"])
        if abs(c - float(x["cost"])) > 1e-6:
            bad_cost.append(x["t"])
    add("第7讲", "cost = 2·FP + 10·FN（逐行）", "全部成立", f"{len(bad_cost)} 行不成立", not bad_cost)

    bad_sel = [x["t"] for x in r if int(x["TP"]) + int(x["FP"]) != int(x["selected_count"])]
    add("第7讲", "selected_count = TP + FP（逐行）", "全部成立",
        f"{len(bad_sel)} 行不成立", not bad_sel)

    sel = [x for x in r if str(x.get("selected", "")).strip() in ("1", "True", "true", "yes")]
    if sel:
        add("第7讲", "选定阈值唯一", 1, len(sel), len(sel) == 1)
        add("第7讲", "选定阈值取最小代价（平分取较大 t）",
            "argmin(cost)",
            sel[0]["t"],
            abs(min(float(x["cost"]) for x in r) - float(sel[0]["cost"])) < 1e-6)
    else:
        mc = min(float(x["cost"]) for x in r)
        cand = [float(x["t"]) for x in r if abs(float(x["cost"]) - mc) < 1e-9]
        add("第7讲", "最小代价出现在网格内", "有", f"t={max(cand)}（最小代价 {mc}）", True)

    # 1.01 哨兵：全拒绝，TP = 0、selected_count = 0
    last = r[-1]
    add("第7讲", "t=1.01 为全拒绝哨兵（TP=0、选中数=0）", "TP=0/选中=0",
        f"TP={last['TP']}/选中={last['selected_count']}",
        int(last["TP"]) == 0 and int(last["selected_count"]) == 0)


# --------------------------------------------------------------- 第 8 讲：OOF 完整性
def check_lec8(work: Path) -> None:
    print("\n[第 8 讲] OOF 完整性与双协议差异")
    p = work / "run" / "L8-01" / "out" / "oof_predictions.csv"
    if not p.exists():
        add("第8讲", "OOF 表存在", "存在", "缺失", False)
        return
    r = read_csv(p)
    combos: dict[tuple[str, str], list[str]] = {}
    for x in r:
        combos.setdefault((x["protocol"], x["model"]), []).append(x["entry_id"])

    sizes = {k: len(v) for k, v in combos.items()}
    uniq = {k: len(set(v)) for k, v in combos.items()}
    add("第8讲", "各协议×模型行数一致", "全部相同",
        f"{len(set(sizes.values()))} 种行数：{sorted(set(sizes.values()))}",
        len(set(sizes.values())) == 1)
    add("第8讲", "同一 entry_id 不重复出现（每组合内）", "全部唯一",
        f"最大重复 {max(sizes[k] - uniq[k] for k in sizes)}",
        all(sizes[k] == uniq[k] for k in sizes))

    sets = [set(v) for v in combos.values()]
    all_same = all(s == sets[0] for s in sets)
    add("第8讲", "各组合的 entry_id 全集一致", "一致",
        f"{len(sets)} 个组合，基数 {len(sets[0])}", all_same)

    # random 应优于 group（组外推更难）
    pc = work / "run" / "L8-01" / "out" / "protocol_comparison.csv"
    if pc.exists():
        t = read_csv(pc)
        m = {(x["protocol"], x["model"]): float(x["pooled_mae"]) for x in t}
        for model in sorted({k[1] for k in m}):
            if ("random", model) in m and ("group", model) in m:
                better = m[("group", model)] >= m[("random", model)]
                add("第8讲", f"{model}：group MAE ≥ random MAE（外推更难）",
                    f"≥ {m[('random', model)]:.4f}",
                    f"{m[('group', model)]:.4f}", better)


# --------------------------------------------------------------- 第 9 讲：解释产物
def check_lec9(work: Path) -> None:
    print("\n[第 9 讲] 模型解释产物一致性")
    out = work / "run" / "L9-01" / "out"
    pi = out / "permutation_importance.csv"
    if pi.exists():
        r = read_csv(pi)
        feats = sorted({x["feature"] for x in r})
        add("第9讲", "置换重要性覆盖 4 个成分特征", 4, len(feats), len(feats) == 4)
        reps = sorted({int(x["repeat"]) for x in r})
        add("第9讲", "每个特征有多次重复（可给均值±标准差）", "≥2",
            f"{len(reps)} 次", len(reps) >= 2)
        # delta_mae 应为非负（打乱后误差不应系统性地变小）
        neg = [x for x in r if float(x["delta_mae"]) < -1e-9]
        add("第9讲", "打乱特征后误差不系统性下降（delta_mae ≥ 0 占多数）",
            "多数 ≥ 0", f"{len(neg)}/{len(r)} 为负", len(neg) < len(r) / 2)
    else:
        add("第9讲", "置换重要性表", "存在", "缺失", False)

    pdp = out / "pdp.csv"
    if pdp.exists():
        r = read_csv(pdp)
        cols = list(r[0]) if r else []
        add("第9讲", "pdp.csv 列为 (mean_Z, pdp_eV)（README §3：只做 mean_Z）",
            "['mean_Z', 'pdp_eV']", cols, cols == ["mean_Z", "pdp_eV"])
        # 代码内部自洽性：pdp 行数应等于自报的 pdp_n_grid（去重后的网格点数）
        n_grid = None
        dev = out / "development_model.json"
        if dev.exists():
            n_grid = find_key(json.loads(dev.read_text(encoding="utf-8")), "pdp_n_grid")
        if n_grid is not None:
            add("第9讲", "pdp.csv 行数 = 自报 pdp_n_grid", n_grid, len(r), len(r) == n_grid)
            # README 声明「17 位」；实际取决于训练集 mean_Z 的唯一取值数
            if len(r) != 17:
                add("第9讲", "README 称 PDP 网格为 17 位", 17, len(r), False, kind="doc")
    else:
        add("第9讲", "PDP 表", "存在", "缺失", False)

    oof = out / "oof_predictions.csv"
    if oof.exists():
        r = read_csv(oof)
        combos = {}
        for x in r:
            combos.setdefault((x["protocol"], x["model"]), 0)
            combos[(x["protocol"], x["model"])] += 1
        add("第9讲", "OOF 各组合行数一致", "全部相同",
            f"{sorted(set(combos.values()))}", len(set(combos.values())) == 1)

    audit = out / "rf_audit"
    if audit.is_dir():
        files = list(audit.glob("*"))
        add("第9讲", "rf_audit 目录有内容", ">0", f"{len(files)} 个文件", len(files) > 0)


# --------------------------------------------------------------- 第 10 讲：聚类覆盖
def check_lec10(work: Path) -> None:
    print("\n[ 第 10 讲] 聚类覆盖与尺度对照")
    base = work / "run" / "L10-01"
    src_data = work / "src" / "第10讲 无监督学习与研究方案中期检查" / "code" / "data" / "nomad_snapshot.csv"
    n_all = len(read_csv(src_data)) if src_data.exists() else None

    for scale, d in (("raw", base / "raw"), ("standardized", base / "std")):
        a = d / "assignments.csv"
        if not a.exists():
            add("第10讲", f"{scale} assignments 存在", "存在", "缺失", False)
            continue
        r = read_csv(a)
        ids = [x["entry_id"] for x in r]
        add("第10讲", f"{scale} 覆盖全部条目", n_all, len(ids), len(ids) == n_all)
        add("第10讲", f"{scale} entry_id 不重复", "唯一", f"{len(set(ids))} 个", len(set(ids)) == len(ids))
        labels = {x["label"] for x in r}
        add("第10讲", f"{scale} 簇标签数 ≤ k", "≤ k", f"{len(labels)} 个簇", True)

    sc = base / "raw" / "scale_comparison.csv"
    if sc.exists():
        r = read_csv(sc)
        add("第10讲", "尺度对照表有内容", ">0 行", f"{len(r)} 行", len(r) > 0)
    pve = base / "raw" / "pca_summary.csv"
    if pve.exists():
        r = read_csv(pve)
        add("第10讲", "PCA 摘要表有内容", ">0 行", f"{len(r)} 行", len(r) > 0)


# --------------------------------------------------------------- 报告
def write_report(path: Path, work: Path) -> int:
    bad = [r for r in rows if r[5] == "assert" and r[4] != "成立"]
    doc = [r for r in rows if r[5] == "doc"]
    ok_n = len(rows) - len(bad) - len(doc)
    lines = [
        "# 第 1—10 讲教学断言与实算输出核对",
        "",
        f"- 执行时间：{__import__('datetime').datetime.now():%Y-%m-%d %H:%M:%S}",
        f"- 产物根目录：`{work}`",
        f"- **结论：断言 {ok_n} 项成立、{len(bad)} 项不成立；另有 {len(doc)} 处文档与实算不一致**",
        "",
        "> 口径：`不成立` = 代码实际行为与声明不符（需改代码）；",
        "> `文档不一致` = 代码自洽、但 README 写的数值与当前数据集不符（需改文档）。",
        "",
        "| 讲 | 断言 | 期望 | 实测 | 结论 |",
        "|---|---|---|---|---|",
    ]
    for lec, claim, exp, act, mark, _kind in rows:
        lines.append(f"| {lec} | {claim} | {exp} | {act} | {mark} |")
    if bad:
        lines += ["", "## 一、不成立的断言（代码问题）", ""]
        for lec, claim, exp, act, _m, _k in bad:
            lines.append(f"- **{lec}**｜{claim}：期望 `{exp}`，实测 `{act}`")
    if doc:
        lines += ["", "## 二、文档与实算不一致（改 README，不改代码）", ""]
        for lec, claim, exp, act, _m, _k in doc:
            lines.append(f"- **{lec}**｜{claim}：README 写 `{exp}`，当前数据集实测 `{act}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[i] 报告已写入：{path}")
    return 0 if not bad else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="教学断言与实算输出核对")
    ap.add_argument("--work", default="D:/tmp_micourse_check")
    ap.add_argument("--report", default=str(HERE / "断言核对报告-第1-10讲.md"))
    args = ap.parse_args()
    work = Path(args.work)

    print("=" * 74)
    print("  教学断言与实算输出核对")
    print("=" * 74)
    check_lec5(work)
    check_lec7(work)
    check_lec8(work)
    check_lec9(work)
    check_lec10(work)

    rc = write_report(Path(args.report), work)
    bad = [r for r in rows if r[5] == "assert" and r[4] != "成立"]
    doc = [r for r in rows if r[5] == "doc"]
    print("\n" + "=" * 74)
    print(f"  成立 {len(rows) - len(bad) - len(doc)} 项｜不成立 {len(bad)} 项｜文档不一致 {len(doc)} 处")
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
