#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
第 1—10 讲课程代码批量检查器
=============================

做什么
------
把每一讲的 `code/`、`code_v5/` **复制到非同步盘的临时目录**后，按各讲 README 规定的
命令行逐条实跑，收集退出码、耗时、关键输出与产物清单，生成一份可直接贴进验收记录的
Markdown 报告 + 机器可读 JSON。

为什么这样设计
--------------
1. **先复制再跑**：多数脚本会往 `outputs/` 或 `数据目录` 写文件，直接在课件里跑会覆盖
   随包的验收产物（第 6、7 讲 README 明确禁止）。复制后原件零风险。
2. **不从系统 TEMP 跑**：本机沙箱不允许写 `%LOCALAPPDATA%\\Temp`；而且项目目录在坚果云
   同步盘上，脚本「发布目录」一步的 rename 会报 `WinError 5`（同步客户端持有句柄）。
   因此统一用 `D:/tmp_micourse_check`（与项目同盘、非同步目录）。
3. **显式给输出参数**：不依赖脚本默认值，避免误写随包 `outputs/`。
4. **区分「预期受限」与「真失败」**：第 3 讲示例 1 需要 Materials Project API Key，
   没有 Key 必然失败，这是设计如此，不算回归。用 `expect_fail` 标记，单独归类。

用法
----
    python check_lecture_code.py                       # 检查全部十讲
    python check_lecture_code.py --lectures 1-5        # 只查第 1—5 讲
    python check_lecture_code.py --lectures 6,7,9      # 只查指定几讲
    python check_lecture_code.py --keep                # 保留上次的源码副本，不重新复制
    python check_lecture_code.py --report 路径.md      # 指定报告位置

退出码
------
    0  全部通过（含预期受限项）
    1  存在真失败或「预期失败却成功了」的异常项

作者：何刚  NNIP LAB @ SWUST
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ----------------------------------------------------------------------------- 路径
WORK = Path("D:/tmp_micourse_check")
SRC = WORK / "src"          # 课件代码副本
RUN = WORK / "run"          # 各组输出
PY = Path(r"C:\Users\gang\.conda\envs\MICourse\python.exe")
DEFAULT_COURSE = Path(r"D:/我的坚果云/SWUST/Courses/AI在材料科学中的应用/课件")

L1 = "第1讲 材料信息学导论与AI产业/code"
L2 = "第2讲 机器学习任务类型与材料数据生态/code"
L3C = "第3讲 数据获取处理与剖析/code"
L3V = "第3讲 数据获取处理与剖析/code_v5"
L4C = "第4讲 成分特征化/code"
L4V = "第4讲 成分特征化/code_v5"
L5C = "第5讲 结构与图表示/code"
L5V = "第5讲 结构与图表示/code_v5"
L6C = "第6讲 回归正则化与材料基线/code"
L6V = "第6讲 回归正则化与材料基线/code_v5"
L7C = "第7讲 分类不平衡数据与决策阈值/code"
L7V = "第7讲 分类不平衡数据与决策阈值/code_v5"
L8C = "第8讲 可信评估数据划分与外推/code"
L9C = "第9讲 集成学习核方法与模型解释/code"
L10C = "第10讲 无监督学习与研究方案中期检查/code"

# ----------------------------------------------------------------------------- 用例
# 每个 group 共享一个 run/<gid> 目录；steps 顺序执行，后一步可用前一步产物。
# expect_fail=True 表示「设计上就会失败」，例如缺 API Key / 需要外网凭据。
GROUPS: list[dict] = [
    # ── 第 1 讲 ────────────────────────────────────────────────────────────────
    dict(gid="L1-01", lec=1, cwd=L1, title="示例1 材料数据的真实形态",
         steps=[dict(cmd=["示例1-材料数据的真实形态.py"],
                     note="无参数；图表写入 __file__ 同级「输出/」（副本内）")]),
    dict(gid="L1-02", lec=1, cwd=L1, title="示例2 材料发现范式与化学空间",
         steps=[dict(cmd=["示例2-材料发现范式与化学空间.py"],
                     note="无参数；README 声明课堂不要求运行")]),

    # ── 第 2 讲 ────────────────────────────────────────────────────────────────
    dict(gid="L2-01", lec=2, cwd=L2, title="示例1 任务类型与数据稀疏性",
         steps=[dict(cmd=["示例1-任务类型与数据稀疏性.py"], note="无参数")]),
    dict(gid="L2-02", lec=2, cwd=L2, title="示例2 数据仓库与结构对象",
         steps=[dict(cmd=["示例2-数据仓库与结构对象.py"], note="无参数；需 pymatgen")]),

    # ── 第 3 讲 ────────────────────────────────────────────────────────────────
    dict(gid="L3-01", lec=3, cwd=L3C, title="示例1 MP-API 取数与去重",
         steps=[dict(cmd=["示例1-MP-API取数与去重.py"],
                     note="无 API Key 时自动回退本地快照（实测走的是回退路径，379 条→14 成分）")]),
    dict(gid="L3-02", lec=3, cwd=L3C, title="示例2 数据剖析与泄漏识别",
         steps=[dict(cmd=["示例2-数据剖析与泄漏识别.py"], note="读随包 CSV，不联网")]),
    dict(gid="L3-03", lec=3, cwd=L3C, title="示例3 NOMAD 访问与多源对照",
         steps=[dict(cmd=["示例3-NOMAD访问与多源对照.py"],
                     note="真实联网 NOMAD API；课堂无网络环境会失败，需提前确认")]),
    dict(gid="L3-04", lec=3, cwd=L3V, title="code_v5 快照审计（V5 正式入口）",
         steps=[dict(cmd=["audit_snapshot.py", "--input", "data/mp_be_snapshot.csv",
                          "--output", "{RUN}/out",
                          "--projection", "data/nomad_eg_gap.csv"],
                     note="7 列快照审计 + 4 列投影对照")]),

    # ── 第 4 讲 ────────────────────────────────────────────────────────────────
    dict(gid="L4-01", lec=4, cwd=L4C, title="CBFV 从零实现（历史材料）",
         steps=[dict(cmd=["cbfv_from_scratch.py"], note="无参数，仅打印")]),
    dict(gid="L4-02", lec=4, cwd=L4C, title="特征器对比（历史材料）",
         steps=[dict(cmd=["compare_featurizers.py"], note="无参数；依赖 matminer/CBFV")]),
    dict(gid="L4-03", lec=4, cwd=L4V, title="code_v5 成分特征化（V5 正式入口）",
         steps=[dict(cmd=["featurize_composition.py", "--input", "data/examples.csv",
                          "--elements", "data/element_properties.csv", "--out", "{RUN}/out"],
                     note="8 条示例 → 4 列特征；验收值 Al2O3=10.000/6.000/2.708/1.830")]),

    # ── 第 5 讲 ────────────────────────────────────────────────────────────────
    dict(gid="L5-01", lec=5, cwd=L5C, title="结构特征（历史材料）",
         steps=[dict(cmd=["structure_features.py"], note="无参数，仅打印")]),
    dict(gid="L5-02", lec=5, cwd=L5C, title="分子特征（历史材料）",
         steps=[dict(cmd=["mol_features.py"], note="无参数；依赖 rdkit")]),
    dict(gid="L5-03", lec=5, cwd=L5V, title="code_v5 图核心：默认链",
         steps=[dict(cmd=["graph_core.py", "--input", "data/chain_1d.json", "--out", "{RUN}/run01"],
                     note="2 节点 4 有向边")]),
    dict(gid="L5-04", lec=5, cwd=L5V, title="code_v5 图核心：r=3.1 截断",
         steps=[dict(cmd=["graph_core.py", "--input", "data/chain_1d_r3p1.json", "--out", "{RUN}/run_r3p1"],
                     note="近邻数超限应显式失败或按规则处理")]),
    dict(gid="L5-05", lec=5, cwd=L5V, title="code_v5 图核心：元素置换双射",
         steps=[dict(cmd=["graph_core.py", "--input", "data/chain_1d.json",
                          "--out", "{RUN}/run_perm", "--perm", "A:B,B:A"],
                     note="等变性与特征映射")]),
    dict(gid="L5-06", lec=5, cwd=L5V, title="code_v5 分子图",
         steps=[dict(cmd=["molecule_core.py", "--input", "data/molecules.json", "--out", "{RUN}/run_mol"],
                     note="分子图构建与指纹")]),

    # ── 第 6 讲 ────────────────────────────────────────────────────────────────
    # 注意：不跑 code/lec6_baselines.py —— README 明确说它会写进随包 outputs/
    dict(gid="L6-01", lec=6, cwd=L6V, title="code_v5 基线主流程（V5 正式入口）",
         steps=[dict(cmd=["run_v5.py", "--out", "{RUN}/out"],
                     note="4 模型对比 + 12 个输出文件")]),
    dict(gid="L6-02", lec=6, cwd=L6V, title="code_v5 扰动标签泄漏自检",
         steps=[dict(cmd=["run_v5.py", "--out", "{RUN}/out_perturb", "--perturb-test"],
                     note="扰动 test 标签后指标应显著恶化")]),
    dict(gid="L6-03", lec=6, cwd=L6V, title="sklearn 等价实现核对",
         steps=[dict(cmd=["sklearn_equivalent.py"], note="无参数；与手写实现对照")]),

    # ── 第 7 讲 ────────────────────────────────────────────────────────────────
    # 三步必须在一组内串行：gen_data 产出数据 → 主流程消费 → 自查消费主流程产物
    dict(gid="L7-01", lec=7, cwd=L7C, title="历史材料：建数据→分类→自查",
         steps=[
             dict(cmd=["gen_data.py", "--out", "{RUN}/data/photovoltaic_synthetic.csv"],
                  note="固定 seed，可复现 SHA256"),
             dict(cmd=["lec7_classification.py", "--data", "{RUN}/data/photovoltaic_synthetic.csv",
                       "--output-dir", "{RUN}/run"],
                  note="阈值与代价敏感；不写随包 outputs/"),
             dict(cmd=["student_check.py", "--pred", "{RUN}/run/val_predictions.csv",
                       "--ref", "{RUN}/run/val_threshold_cost.csv", "--out-dir", "{RUN}/run"],
                  note="用 val 逐条概率重算并核对"),
         ]),
    dict(gid="L7-02", lec=7, cwd=L7V, title="code_v5 分类主流程 + 独立复算（V5 正式入口）",
         steps=[
             dict(cmd=["run_v5.py", "--out", "{RUN}/out"], note="16 个输出文件"),
             dict(cmd=["check_v5.py", "--pred", "{RUN}/out/val_predictions.csv",
                       "--ref", "{RUN}/out/val_threshold_cost.csv", "--out", "{RUN}/recheck"],
                  note="按 pred 重算阈值代价并比对 ref"),
         ]),

    # ── 第 8 讲 ────────────────────────────────────────────────────────────────
    dict(gid="L8-01", lec=8, cwd=L8C, title="嵌套交叉验证 + 学生自查",
         steps=[
             dict(cmd=["lec8_nested_cv.py", "--output-dir", "{RUN}/out"],
                  note="random/group 双协议嵌套 CV，OOF 表"),
             dict(cmd=["student_check.py", "--oof", "{RUN}/out/oof_predictions.csv",
                       "--out-dir", "{RUN}/out"],
                  note="从 OOF 表独立复算指标"),
         ]),
    dict(gid="L8-02", lec=8, cwd=L8C, title="单折扰动自检",
         steps=[dict(cmd=["qa_perturb.py", "--qa-dir", "{RUN}/qa"], note="扰动后指标应恶化")]),
    dict(gid="L8-03", lec=8, cwd=L8C, title="泄漏对照演示",
         steps=[dict(cmd=["qa_leak_demo.py", "--qa-dir", "{RUN}/qa"], note="random vs group 泄漏对照")]),
    dict(gid="L8-04", lec=8, cwd=L8C, title="自查脚本的 8 个负例",
         steps=[dict(cmd=["qa_student_check.py", "--qa-dir", "{RUN}/qa"],
                     note="确认自查脚本能识别错误输入")]),

    # ── 第 9 讲 ────────────────────────────────────────────────────────────────
    dict(gid="L9-01", lec=9, cwd=L9C, title="集成学习主流程 + 学生自查",
         steps=[
             dict(cmd=["lec9_models.py", "--output-dir", "{RUN}/out"],
                  note="树/RF/核方法 + 置换重要性 + PDP"),
             dict(cmd=["student_check.py", "--oof", "{RUN}/out/oof_predictions.csv",
                       "--out", "{RUN}/out/student_table.csv"],
                  note="核对 OOF 与折叠指标一致性"),
         ]),

    # ── 第 10 讲 ───────────────────────────────────────────────────────────────
    # 三尺度对比必须在一组内跑，student_check 的 --compare 要读上一尺度的结果目录
    dict(gid="L10-01", lec=10, cwd=L10C, title="无监督 raw→标准化 + 双尺度自查",
         steps=[
             dict(cmd=["lec10_unsupervised.py", "--mode", "records", "--scale", "raw",
                       "--output-dir", "{RUN}/raw"],
                  note="原始尺度 KMeans + PCA"),
             dict(cmd=["lec10_unsupervised.py", "--mode", "records", "--scale", "standardized",
                       "--output-dir", "{RUN}/std"],
                  note="标准化后对比"),
             dict(cmd=["student_check.py", "--results", "{RUN}/std", "--compare", "{RUN}/raw",
                       "--data", "data/nomad_snapshot.csv",
                       "--elements", "data/element_properties.csv"],
                  note="两侧都完整核验"),
         ]),
]


# ----------------------------------------------------------------------------- 工具
def parse_lectures(spec: str | None) -> set[int] | None:
    if not spec:
        return None
    if "-" in spec:
        a, b = spec.split("-", 1)
        return set(range(int(a), int(b) + 1))
    return {int(x) for x in spec.split(",") if x.strip()}


def prepare(course: Path, lectures: set[int] | None, keep: bool) -> None:
    if keep and SRC.exists():
        print(f"[i] 复用已有副本：{SRC}")
        return
    if WORK.exists():
        shutil.rmtree(WORK, ignore_errors=True)
    SRC.mkdir(parents=True, exist_ok=True)
    RUN.mkdir(parents=True, exist_ok=True)
    n = 0
    for d in sorted(course.iterdir()):
        if not d.is_dir() or not d.name.startswith("第"):
            continue
        try:
            lec = int(d.name.split("讲")[0].replace("第", ""))
        except ValueError:
            continue
        if lectures and lec not in lectures:
            continue
        for sub in ("code", "code_v5"):
            s = d / sub
            if s.is_dir():
                shutil.copytree(s, SRC / d.name / sub)
                n += 1
    print(f"[i] 已复制 {n} 个代码目录 → {SRC}")


def dir_stats(p: Path) -> tuple[int, int]:
    if not p.exists():
        return 0, 0
    files = [f for f in p.rglob("*") if f.is_file() and not f.name.startswith("_checker_")]
    return len(files), sum(f.stat().st_size for f in files)


def tail(text: str, n: int = 4, width: int = 200) -> str:
    lines = [ln.rstrip() for ln in (text or "").splitlines() if ln.strip()]
    out = lines[-n:]
    return " ⏎ ".join(ln[:width] for ln in out)


def run_group(g: dict) -> dict:
    cwd = SRC / g["cwd"]
    out_root = RUN / g["gid"]
    # 每组开跑前清空自己的输出目录，保证多次运行结果可比
    if out_root.exists():
        shutil.rmtree(out_root, ignore_errors=True)
    out_root.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ, PYTHONNOUSERSITE="1", PYTHONIOENCODING="utf-8",
               MPLBACKEND="Agg", CONDA_DEFAULT_ENV="MICourse")

    res = dict(gid=g["gid"], lec=g["lec"], title=g["title"], cwd=g["cwd"],
               steps=[], status="PASS", reason="", files=0, bytes=0, dur=0.0)

    for step in g["steps"]:
        cmd = [str(PY)] + [s.replace("{RUN}", out_root.as_posix()) for s in step["cmd"]]
        t0 = time.time()
        try:
            p = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=1800)
            rc, so, se = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired:
            rc, so, se = -9, "", "TIMEOUT > 1800s"
        dur = time.time() - t0

        expect_fail = step.get("expect_fail", False)
        if rc == 0:
            st = "UNEXPECTED_PASS" if expect_fail else "PASS"
        else:
            st = "EXPECTED_FAIL" if expect_fail else "FAIL"

        res["steps"].append(dict(cmd=" ".join(step["cmd"]), note=step.get("note", ""),
                                 rc=rc, status=st, dur=round(dur, 2),
                                 stdout=tail(so, 6), stderr=tail(se, 6)))
        res["dur"] += dur

        # 失败时留完整日志：有些脚本把错误写 stdout，只看 stderr 会误判为"无信息失败"
        if st in ("FAIL", "UNEXPECTED_PASS"):
            log = out_root / f"_checker_{step['cmd'][0]}.log"
            log.write_text(
                f"cmd: {' '.join(step['cmd'])}\nrc: {rc}\n\n"
                f"===== stdout =====\n{so}\n\n===== stderr =====\n{se}\n",
                encoding="utf-8", errors="replace")
            res.setdefault("logs", []).append(log.as_posix())
            if not se.strip():
                # stderr 空时，报告里改用 stdout 尾部，否则看不出原因
                res["steps"][-1]["stderr"] = "[stdout] " + tail(so, 6)

        if st == "FAIL":
            res["status"] = "FAIL"
            res["reason"] = f"{step['cmd'][0]} → rc={rc}"
            break
        if st == "UNEXPECTED_PASS":
            res["status"] = "ANOMALY"
            res["reason"] = f"{step['cmd'][0]} 按设计应失败，却成功了"

    f1, b1 = dir_stats(out_root)
    f2, b2 = dir_stats(cwd / "输出")   # 第 1—3 讲把图表写到脚本同级的「输出」
    res["files"], res["bytes"] = f1 + f2, b1 + b2
    res["dur"] = round(res["dur"], 2)
    return res


# ----------------------------------------------------------------------------- 报告
def write_report(results: list[dict], path: Path) -> None:
    bad = [r for r in results if r["status"] == "FAIL"]
    anomaly = [r for r in results if r["status"] == "ANOMALY"]
    ok = [r for r in results if r["status"] == "PASS"]

    lines = [
        "# 第 1—10 讲课程代码实跑检查报告",
        "",
        f"- 执行时间：{time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 解释器：`{PY}`",
        f"- 运行根目录：`{WORK}`（非同步盘；课件原件未被修改）",
        f"- **结论：通过 {len(ok)} / 失败 {len(bad)} / 异常 {len(anomaly)}，共 {len(results)} 组**",
        "",
        "> 判定口径：`PASS` = 退出码 0 且产物生成；`FAIL` = 非预期非零退出；",
        "> `EXPECTED_FAIL` = 设计上需要外网凭据（如 Materials Project API Key），不算回归；",
        "> `ANOMALY` = 按设计应失败却成功，需人工确认。",
        "",
        "## 一、总览",
        "",
        "| 组 | 讲 | 内容 | 状态 | 步骤 | 耗时 s | 产物 | 说明 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in sorted(results, key=lambda x: (x["lec"], x["gid"])):
        n_pass = sum(1 for s in r["steps"] if s["status"] in ("PASS", "EXPECTED_FAIL"))
        mark = {"PASS": "通过", "FAIL": "**失败**", "ANOMALY": "**异常**"}[r["status"]]
        note = r["reason"] or ""
        lines.append(
            f"| {r['gid']} | {r['lec']} | {r['title']} | {mark} | "
            f"{n_pass}/{len(r['steps'])} | {r['dur']} | {r['files']} 个 / "
            f"{r['bytes'] / 1024:.0f} KB | {note} |"
        )

    lines += ["", "## 二、逐组明细", ""]
    for r in sorted(results, key=lambda x: (x["lec"], x["gid"])):
        lines.append(f"### {r['gid']}　第 {r['lec']} 讲　{r['title']}")
        lines.append("")
        lines.append(f"- 目录：`{r['cwd']}`")
        for s in r["steps"]:
            icon = {"PASS": "通过", "FAIL": "失败",
                    "EXPECTED_FAIL": "预期受限", "UNEXPECTED_PASS": "异常通过"}[s["status"]]
            lines.append(f"- **{icon}**（rc={s['rc']}，{s['dur']}s）`{s['cmd']}`")
            if s["note"]:
                lines.append(f"  - 说明：{s['note']}")
            if s["stdout"]:
                lines.append(f"  - 输出：{s['stdout']}")
            if s["stderr"] and s["status"] in ("FAIL", "UNEXPECTED_PASS"):
                lines.append(f"  - 错误：{s['stderr']}")
        lines.append("")

    if bad:
        lines += ["## 三、需要处理的失败", ""]
        for r in bad:
            lines.append(f"### {r['gid']}　第 {r['lec']} 讲　{r['title']}")
            for s in r["steps"]:
                if s["status"] == "FAIL":
                    lines.append(f"- 命令：`{s['cmd']}`")
                    lines.append(f"- 退出码：{s['rc']}")
                    lines.append(f"- 错误：{s['stderr']}")
            lines.append("")

    if anomaly:
        lines += ["## 四、异常通过（需人工确认）", ""]
        for r in anomaly:
            lines.append(f"- {r['gid']}　{r['title']}：{r['reason']}")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[i] 报告已写入：{path}")


def main() -> int:
    ap = argparse.ArgumentParser(description="第 1—10 讲课程代码实跑检查")
    ap.add_argument("--course", default=str(DEFAULT_COURSE), help="课件根目录")
    ap.add_argument("--lectures", default=None, help="只查指定讲，如 1-5 或 6,7,9")
    ap.add_argument("--keep", action="store_true", help="复用已有源码副本")
    ap.add_argument("--report", default=None, help="报告输出路径")
    ap.add_argument("--json", default=None, help="JSON 结果输出路径")
    args = ap.parse_args()

    lectures = parse_lectures(args.lectures)
    course = Path(args.course)
    if not course.is_dir():
        print(f"[x] 课件目录不存在：{course}")
        return 1
    if not PY.exists():
        print(f"[x] 找不到解释器：{PY}")
        return 1

    print("=" * 74)
    print("  第 1—10 讲课程代码实跑检查")
    print("=" * 74)
    prepare(course, lectures, args.keep)

    groups = [g for g in GROUPS if not lectures or g["lec"] in lectures]
    print(f"[i] 待检查 {len(groups)} 组\n")

    results = []
    for i, g in enumerate(groups, 1):
        print(f"[{i:02d}/{len(groups)}] {g['gid']:<8s} 第{g['lec']:>2d}讲 {g['title']} ... ",
              end="", flush=True)
        r = run_group(g)
        results.append(r)
        icon = {"PASS": "ok", "FAIL": "FAIL", "ANOMALY": "ANOM"}[r["status"]]
        print(f"{icon}  {r['dur']:.2f}s  {r['files']} 个产物", flush=True)
        if r["status"] != "PASS":
            for s in r["steps"]:
                if s["status"] in ("FAIL", "UNEXPECTED_PASS"):
                    print(f"        └─ rc={s['rc']} {s['stderr'][:160]}")

    report = Path(args.report) if args.report else DEFAULT_COURSE / "00-课程环境" / "代码检查报告-第1-10讲.md"
    write_report(results, report)
    if args.json:
        Path(args.json).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[i] JSON 已写入：{args.json}")

    bad = [r for r in results if r["status"] != "PASS"]
    print("\n" + "=" * 74)
    print(f"  通过 {len(results) - len(bad)} / {len(results)} 组")
    print("=" * 74)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
