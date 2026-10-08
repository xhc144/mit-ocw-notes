#!/usr/bin/env python3
"""Freeze the actual 6.253 questions, review findings, and reproducible checks.

Run from any directory. This writes only review/convex-assessment-audit.json.
Counts distinguish original top-level numbers, original first-layer response
blocks, and requested outputs inside those blocks. Equivalent statements in
HW3 Q3(a) remain one equivalence task.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import itertools
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = {
    "hw1": [
        {"a": ["凸集缩放和等式及非凸反例"], "b": ["锥交"], "c": ["线性像", "线性逆像"], "d": ["锥向量和"], "e": ["凸锥刻画"]},
        {"whole": ["复合函数凸性", "标量严格凸性"]},
        {"a": ["log-sum-exp凸性"], "b": ["范数幂凸性"], "c": ["指数二次式凸性"], "d": ["仿射复合凸性"]},
        {"whole": ["闭凸包等式", "紧集凸包紧"]},
        {"whole": ["延长性质与非相对内点反例"]},
    ],
    "hw2": [
        {"a": ["闭包凸锥", "相对内部凸锥"], "b": ["有限生成锥相对内部"]},
        {"whole": ["相对内部交非空等价性"]},
        {"a": ["局部凸时直线检验等价性"], "b": ["每条直线局部极小", "抛物线下降反例"]},
        {"a": ["欧氏投影二次规划"], "b": ["正定坐标变换及最优解"], "c": ["非齐次等式二次规划最优解"]},
        {"a": ["目标接近蕴含距离接近"], "b": ["距离接近蕴含目标接近"], "c": ["极小化序列有界", "聚点最优"]},
    ],
    "hw3": [
        {"a": ["二阶锥非回缩反例"], "b": ["无限半空间表示及无限交反例"]},
        {"whole": ["包含仿射集的严格相对内部分离刻画"]},
        {"a": ["强分离的三个条件等价"], "b": ["五个充分条件分别保证差集闭并强分离"]},
        {"a": ["拟凸局部极小全局性"], "b": ["共同衰退锥等于共同线性空间时取到", "多面体与共同衰退方向条件时取到"]},
        {"a": ["所有纤维紧极小点集"], "b": ["纤维渐近斜率相同"]},
    ],
    "hw4": [
        {"whole": ["幂函数共轭"]},
        {"a": ["共轭反序等价"], "b": ["支持函数与集合包含等价", "去闭性反例"]},
        {"whole": ["向量和支持函数", "凸包向量和支持函数", "有限并支持函数", "有限并凸包支持函数"]},
        {"whole": ["连续唯一响应蕴含鞍点", "平方和实例全部鞍点"]},
        {"whole": ["Fenchel扰动对偶公式"]},
    ],
    "hw5": [
        {"whole": ["扩展表示强对偶与最优乘子转移"]},
        {"whole": ["两个参数的最优值变动界"]},
        {"whole": ["严格不可行与归一化乘子等价"]},
        {"whole": ["有限对偶值、真扰动函数、无竖线等价"]},
        {"a": ["联合与偏次微分包含", "严格包含反例"], "b": ["可分离加光滑项时等号"]},
        {"whole": ["对偶间隙蕴含最优乘子处不可微"]},
        {"a": ["约束费用四点图"], "b": ["MC/MC几何框架"], "c": ["全部原最优解", "全部对偶最优解和间隙", "与支持线图关系"]},
    ],
    "exam2010": [
        {str(i): [title] for i, title in enumerate([
            "开集分离不交", "全空间有界凸函数取到", "菱形边界支持函数", "次梯度蕴含下半连续", "绝对值上图对偶函数", "正交次梯度最优性"
        ], 1)},
        {"1": ["透视二次函数凸性"], "2": ["扰动上闭集合图"], "3": ["原最优值"], "4": ["对偶值", "对偶间隙"], "5": ["正扰动是否存在间隙"]},
    ],
    "exam2012": [
        {str(i): [title] for i, title in enumerate([
            "闭上图是否蕴含连续", "闭上图是否蕴含闭定义域", "相对内部与内部", "衰退锥与相对内部", "X与-X分离", "平方和是否coercive", "紧定义域共轭实值", "开X等式约束强对偶", "实值部分与指示函数次梯度", "线性目标最优点法锥"
        ], 1)},
        {"a": ["不同约束费用点及重数图", "扰动阶梯函数图", "下半连续性"],
         "b": ["可行有间隙参数", "可行无间隙参数", "可行唯一对偶解参数"],
         "c": ["最大截距问题", "全部原最优解", "全部对偶最优解"],
         "d": ["严格约束费用点", "严格扰动函数图", "严格扰动下半连续性", "严格可行有间隙参数", "严格可行无间隙参数", "严格可行唯一对偶解参数"]},
    ],
}

ISSUES = [
    ("hw1-q3-a", "official_algebra_error", "官方双重求和Hessian等式遗漏1/2", "按diag(p)-pp^T独立推导修正, 原PDF第3页实视确认"),
    ("hw2-q5-c", "official_proof_omission", "官方仅证明聚点最优, 未明确证明序列有界", "补尾序列在紧水平集及有限首项有界"),
    ("hw3-q3-b", "external_reference_resolved", "原题只引用教材命题1.5.3的五条件", "实际读取课程summary.pdf第18页命题1.5.3, 完整列条件并以闭线性像证明"),
    ("hw3-q4-a", "finite_local_minimum_convention", "原题未显写局部最优点目标有限", "明确通常有限目标值定义; 给允许无穷局部值时的反例"),
    ("hw4-q2-a", "official_typographical_error", "官方正向共轭证明第二sup错写f1", "改成f2"),
    ("hw4-q2-b", "assumption_precision", "两集合闭性分别必要的表述过强", "说明反向只需目标集合C2闭; 提供C1闭C2开的反例"),
    ("hw4-q5", "properness_convention", "原题闭凸未显写真, 不真退化函数会给未定义无穷差", "标AI条件说明; f1恒无穷、f2恒0、A=0、非零乘子为反例, 真函数条件下公式正确"),
    ("hw5-q1", "official_multiplier_error", "官方误将等式乘子写非负且混入原抽象集问题乘子", "等式乘子取R, 只截取原r个不等式乘子"),
    ("hw5-q4", "official_proof_error", "官方声称epi(p)=cl(M), 这在p不闭时不成立", "用p(u)=-infinity当且仅当M在固定u含完整竖线直接证明"),
    ("hw5-q4", "finite_feasibility_convention", "原题仅写可行, 依Section5.3实值约定推出p(0)有限", "正文明确这项约定; 扩展值目标indicator_[1,infinity)、g(x)=x给有限有效可行性缺失时的反例"),
    ("exam2010-q2-2", "official_algebra_typo", "原解平方根表达不准确且遗漏负x1可能值", "直接按任意u>0,w>0构造x1与x2, 得精确M"),
    ("exam2012-q1-8", "official_answer_conditions_insufficient", "官方True缺少涉及dom(f)的资格条件", "字面False; 给真凸f(0)=1,f(x>0)=0与x=0的间隙1反例"),
    ("exam2012-q1-9", "official_implicit_assumption", "real-valued function未写凸, 全局f凸真仍不足", "字面False; -sqrt(x)+indicator_[0,infinity)在0无次梯度; 补h全空间实值凸才True"),
    ("exam2012-q2-a", "official_missing_answer", "官方标To be added", "AI独立枚举三不同点及中间重数, 全部p阶梯与TikZ, 证明下半连续"),
    ("exam2012-q2-d", "official_proof_omission", "严格约束版本只给结论, 缺完整阶梯与说明", "AI补完整阶梯TikZ、开闭端点、对偶函数及参数边界"),
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enumerate_integer_checks():
    pairs = list(itertools.product([0, 1], repeat=2))
    assert [(4 - 5*x - y, 10*x + 3*y) for x, y in pairs] == [(4, 0), (3, 3), (-1, 10), (-2, 13)]
    assert min(10*x+3*y for x, y in pairs if 5*x+y >= 4) == 10
    assert min(10*x+3*y+2*(4-5*x-y) for x, y in pairs) == 8
    samples = [Fraction(-1), Fraction(0), Fraction(1,2), Fraction(1), Fraction(3,2), Fraction(2), Fraction(3)]
    rows = []
    for a in samples:
        feasible = [x*x+y*y for x,y in pairs if a-x-y <= 0]
        strict = [x*x+y*y for x,y in pairs if a-x-y < 0]
        if a <= 2:
            mu = 0 if a < 0 else 1
            dual = min(x*x+y*y+mu*(a-x-y) for x,y in pairs)
            assert dual == max(Fraction(0), a)
            assert min(feasible) == (0 if a <= 0 else 1 if a <= 1 else 2)
            if strict:
                assert min(strict) == (0 if a < 0 else 1 if a < 1 else 2)
        else:
            dual = "unbounded"
        rows.append({"a": str(a), "primal_nonstrict": min(feasible) if feasible else "infeasible", "primal_strict": min(strict) if strict else "infeasible", "dual": str(dual)})
    return rows


def source_question_pages(source_text, original_number):
    """Use actual form-feed page boundaries, excluding the OCW notice page."""
    source_text = source_text.split("MIT OpenCourseWare", 1)[0]
    matches = list(re.finditer(r"Problem\s+(\d+)\b", source_text))
    target = next(m for m in matches if int(m.group(1)) == original_number)
    later = [m for m in matches if m.start() > target.start()]
    end = later[0].start() if later else len(source_text.rstrip())
    start_page = source_text[:target.start()].count("\f") + 1
    # A form-feed followed only by whitespace marks the previous content page.
    meaningful = source_text[target.start():end].rstrip().rstrip("\f").rstrip()
    end_page = start_page + meaningful.count("\f")
    return list(range(start_page, end_page + 1))


def main():
    source_root = ROOT / "sources/6.253/assessments"
    assessments = []
    problems = []
    first_count = leaf_count = 0
    for assessment, questions in DATA.items():
        year = 2012 if assessment == "exam2012" else 2010
        qrows = []
        for number, blocks in enumerate(questions, 1):
            label = f"ass:6253-{assessment}-q{number}"
            blockrows = []
            for original, tasks in blocks.items():
                block_id = f"{assessment}-q{number}" + (f"-{original}" if original != "whole" else "")
                blockrows.append({"id": block_id, "original_subquestion": None if original == "whole" else original, "tex_label": label,
                    "leaf_tasks": [{"id": f"{block_id}-task{i}", "task": task, "coverage": "full_chinese_statement_and_solution", "math_review": "checked"} for i, task in enumerate(tasks, 1)]})
                first_count += 1
                leaf_count += len(tasks)
            qrows.append({"original_question": number, "tex_label": label, "first_layer_blocks": blockrows})
        filenames = ([f"MIT6_253S12_hw{assessment[-1].zfill(2)}.pdf", f"MIT6_253S12_hw{assessment[-1].zfill(2)}_sol.pdf"]
                     if assessment.startswith("hw") else ["MIT6_253S12_mid_S10_sol.pdf" if year == 2010 else "MIT6_253S12_midterm_sol.pdf"])
        assessments.append({"id": assessment, "actual_year": year, "ocw_course_publication_year": 2012,
            "original_sources": [{"path": str((source_root / name).relative_to(ROOT)), "sha256": sha256(source_root/name)} for name in filenames],
            "main_problem_count": len(questions), "first_layer_block_count": sum(len(x) for x in questions),
            "semantic_leaf_task_count": sum(len(t) for q in questions for t in q.values()), "questions": qrows})
        source_file = source_root / filenames[0]
        source_text = source_file.with_suffix(".txt").read_text()
        for q in qrows:
            corrections = [item[2] for item in ISSUES if item[0].startswith(f"{assessment}-q{q['original_question']}")]
            provenance = "official_solution_reconstructed_with_AI_proof_details"
            if corrections:
                provenance += "; explicit_AI_corrections_or_conditions"
            if assessment == "exam2012" and q["original_question"] == 2:
                provenance = "official_b_c_interval_answers; AI_independent_missing_a_and_completed_d; no_claim_of_complete_official_solution"
            problems.append({
                "label": q["tex_label"], "course": "6.253",
                "collection": f"Homework {assessment[-1]} (Spring {year})" if assessment.startswith("hw") else f"Midterm (Spring {year})",
                "original_question": q["original_question"],
                "first_level_subquestions": [b["id"] for b in q["first_layer_blocks"]],
                "first_level_count": len(q["first_layer_blocks"]),
                "source_file": str(source_file.relative_to(ROOT)),
                "source_pages": source_question_pages(source_text, q["original_question"]),
                "answer_provenance": provenance,
                "notes": corrections,
                "nested_tasks": [task for block in q["first_layer_blocks"] for task in block["leaf_tasks"]],
            })
    files = [ROOT / "assessments/convex-homework.tex", ROOT / "assessments/convex-exams.tex"]
    text = "\n".join(p.read_text() for p in files)
    labels = re.findall(r"\\label\{(ass:6253-[^}]+)\}", text)
    wanted = [q["tex_label"] for assessment in assessments for q in assessment["questions"]]
    assert len(labels) == len(set(labels)) == 31
    assert set(labels) == set(wanted)
    assert text.count(r"\begin{exercise}") == text.count(r"\end{exercise}") == 31
    assert text.count(r"\begin{solution}") == text.count(r"\end{solution}") == 31
    assert first_count == 73
    assert text.count(r"\begin{tikzpicture}") == text.count(r"\end{tikzpicture}") == 4
    payload = {
        "reviewer_role": "delegated independent 6.253 mathematical reader; same-model agent review, not external expert certification",
        "scope": "five Spring 2010 homework sets and Spring 2010/2012 midterms in the official source inventory",
        "count_rules": {"main_problem": "original Problem N; not a file count", "first_layer_block": "original a/b or 1/2 response block; an unsplit original problem counts once", "semantic_leaf": "separately requested output in a block; equivalence proof is one task, not one task per equivalent statement; five conditions in HW3Q3(b) are one uniformly quantified task"},
        "counts": {"main_problems": 31, "homework_main_problems": 27, "exam_main_problems": 4, "first_layer_blocks": first_count, "homework_first_layer_blocks": 48, "exam_first_layer_blocks": 25, "semantic_leaf_tasks": leaf_count},
        "coverage": {"main_problems_drafted": 31, "first_layer_blocks_drafted": first_count, "semantic_leaf_tasks_drafted": leaf_count, "omitted_tasks": [], "unresolved_mathematical_tasks": []},
        "assessments": assessments,
        "problems": problems,
        "findings": [{"task": task, "category": category, "finding": finding, "resolution": resolution, "status": "resolved_and_explicitly_marked"} for task, category, finding, resolution in ISSUES],
        "sources_of_external_conditions": [{"path": "sources/6.253/assessments/MIT6_253S12_summary.pdf", "sha256": sha256(source_root/"MIT6_253S12_summary.pdf"), "location": "printed page 18, Proposition 1.5.3", "archive_policy": "source remains local/link-only; no publisher-permission PDF redistribution authorized by this review"}],
        "reuse": [{"task": "hw1-q4", "tex_reference": "thm:caratheodory"}, {"task": "hw3-q3-b", "tex_reference": "thm:closed-image"}, {"task": "hw3-q4-b", "tex_reference": "thm:retractive-intersection"}, {"task": "hw3-q5-a", "tex_reference": "thm:partial-min"}, {"task": "hw4-q1", "tex_reference": "ex:conjugate-models"}],
        "verification": {"question_label_uniqueness": "passed", "exercise_solution_balance": "passed", "tikz_environment_balance": "passed", "binary_enumeration": "passed", "binary_enumeration_cases": enumerate_integer_checks(), "compile": "wrapper compile attempted and failed because ctex.sty is missing; parent is preparing the unified toolchain", "visual": "source PDF hw1 solution page3 and 2012 exam page1 inspected; final rendered pages pending parent unified build"},
        "deliverables": [{"path": str(p.relative_to(ROOT)), "sha256": sha256(p)} for p in files],
        "remaining_source_gaps": ["Original exam files do not state exact dates or duration; not invented."]
    }
    out = ROOT / "review/convex-assessment-audit.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(payload["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
