#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pre-create giscus discussions for each blog post.

Eliminates the giscus "Discussion not found" 404 by ensuring every published
post has a discussion whose title equals the giscus term (yyyy/mm/dd/slug),
which is the format giscus itself uses when it lazily creates a discussion on
the first comment.

Default mode is dry-run (read-only). Pass --execute to create missing
discussions.

Auth: uses the gh CLI. Locally it reads the keyring login; in CI set the
GH_TOKEN env var (e.g. to a PAT). Run from the repository root.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

CONFIG_PATH = "_config.yml"
POSTS_DIR = "_posts"

# Known existing discussions (term form, no leading/trailing slash), derived
# from the repo at design time. Used as a self-check that term computation is
# correct: each must be reproducible from its post file and present in the repo.
SELF_CHECK_TERMS = [
    "2015/07/27/first-blog",
    "2016/09/27/tools-classify-op-systems",
    "2019/02/20/sre-stability",
    "2021/02/03/mgt-pem",
    "2021/06/30/infra-cn",
    "2023/08/26/se-ddd",
    "2026/01/10/second-decade",
]

FILENAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)$")


def unquote(s):
    s = s.strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        return s[1:-1]
    return s


def read_config(path):
    """Minimal _config.yml parser: url, baseurl, giscus.{repo,repo_id,category_id}."""
    cfg = {"url": "", "baseurl": "", "giscus": {}}
    in_giscus = False
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if not (line.startswith(" ") or line.startswith("\t")):
                # top-level key
                in_giscus = False
                key, _, val = stripped.partition(":")
                key = key.strip()
                if key == "url":
                    cfg["url"] = unquote(val)
                elif key == "baseurl":
                    cfg["baseurl"] = unquote(val)
                elif key == "giscus":
                    in_giscus = True
            elif in_giscus:
                key, _, val = stripped.partition(":")
                key = key.strip()
                if key in ("repo", "repo_id", "category_id"):
                    cfg["giscus"][key] = unquote(val)
    return cfg


def parse_front_matter(text):
    """Parse simple key: value fields from YAML front matter."""
    fm = {}
    if not text.startswith("---"):
        return fm
    parts = text.split("---", 2)
    if len(parts) < 3:
        return fm
    for raw in parts[1].splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        if key:
            fm[key] = unquote(val)
    return fm


def norm_term(s):
    return s.strip().strip("/")


def compute_term(post_path):
    """Return (term, front_matter) for a post; term is None if not derivable."""
    stem = post_path.stem
    text = post_path.read_text(encoding="utf-8")
    fm = parse_front_matter(text)

    if fm.get("permalink"):
        return norm_term(fm["permalink"]), fm

    y = m = d = slug = None
    mt = FILENAME_RE.match(stem)
    if mt:
        y, m, d, slug = mt.group(1), mt.group(2), mt.group(3), mt.group(4)
    fm_date = fm.get("date")
    if fm_date:
        md = re.match(r"(\d{4})-(\d{2})-(\d{2})", fm_date)
        if md:
            y, m, d = md.group(1), md.group(2), md.group(3)
    if fm.get("slug"):
        slug = fm["slug"]
    if not (y and m and d and slug):
        return None, fm
    return norm_term(f"/{y}/{m}/{d}/{slug}"), fm


def gql_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def gh_graphql(query):
    """Run gh api graphql with an inlined query; return parsed data dict."""
    proc = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gh api 调用失败 (exit {proc.returncode}):\n{proc.stderr.strip()}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"gh 返回非 JSON: {exc}\n{proc.stdout[:500]}")
    if payload.get("errors"):
        raise RuntimeError(f"GraphQL 错误: {json.dumps(payload['errors'], ensure_ascii=False)}")
    return payload.get("data") or {}


def list_existing_terms(owner, name, category_id):
    """Return {normalized_title: number} for discussions in the configured category."""
    q = (
        "{ repository(owner: \"%s\", name: \"%s\") {"
        " discussions(first: 100) { nodes { number title category { id } } } } }"
    ) % (owner, name)
    data = gh_graphql(q)
    terms = {}
    for d in data.get("repository", {}).get("discussions", {}).get("nodes", []):
        cat_id = (d.get("category") or {}).get("id")
        if cat_id != category_id:
            continue
        terms[norm_term(d.get("title", ""))] = d.get("number")
    return terms


def create_discussion(repo_id, category_id, title, body):
    q = (
        "mutation { createDiscussion(input: {"
        "repositoryId: \"%s\", categoryId: \"%s\", "
        "title: \"%s\", body: \"%s\"}) { discussion { number title url } } }"
    ) % (repo_id, category_id, gql_escape(title), gql_escape(body))
    data = gh_graphql(q)
    return data.get("createDiscussion", {}).get("discussion", {})


def build_body(fm, term, url, baseurl):
    title = fm.get("title") or term
    canonical = f"{url}{baseurl}/{term}"
    return (
        f"# {title}\n\n"
        f"{canonical}\n\n"
        "> 本 discussion 由 giscus 预创建脚本自动生成，用于承载该文章的 giscus 评论。"
    )


def self_check(posts, existing_terms):
    """Validate term computation against known discussions.

    For each known term, locate its post file, recompute the term, and assert it
    matches and is present in the repo. A missing post file is an orphan
    discussion (post likely deleted) -> warning, not failure. Returns
    (failures, warnings).
    """
    failures = []
    warnings = []
    by_stem = {p.stem: p for p in posts}
    for kt in SELF_CHECK_TERMS:
        parts = kt.split("/")
        if len(parts) < 4:
            failures.append(f"自检项格式异常: {kt}")
            continue
        expected_stem = "-".join(parts[:3]) + "-" + "/".join(parts[3:]).replace("/", "-")
        post = by_stem.get(expected_stem)
        if post is None:
            warnings.append(f"已知 discussion {kt} 无对应文章（孤儿 discussion，文章可能已删除）")
            continue
        term, _ = compute_term(post)
        if term != kt:
            failures.append(f"自检: term 计算不一致，期望 {kt}，实际 {term}（文件 {post.name}）")
            continue
        if term not in existing_terms:
            failures.append(f"自检: {kt} 在仓库中未找到对应 discussion")
    return failures, warnings


def main():
    ap = argparse.ArgumentParser(description="Pre-create giscus discussions for posts.")
    ap.add_argument("--execute", action="store_true", help="写入 GitHub（默认 dry-run）")
    ap.add_argument("--posts-dir", default=POSTS_DIR)
    ap.add_argument("--config", default=CONFIG_PATH)
    ap.add_argument("--report", help="报告输出文件路径（默认 stdout）")
    ap.add_argument("--only", help="只处理文件名 stem 含该子串的文章（选择性回填/测试）")
    args = ap.parse_args()

    cfg = read_config(args.config)
    g = cfg.get("giscus", {})
    repo = g.get("repo")
    repo_id = g.get("repo_id")
    category_id = g.get("category_id")
    url = cfg.get("url", "")
    baseurl = cfg.get("baseurl", "")
    if not (repo and repo_id and category_id):
        print(f"错误: _config.yml 缺少 giscus.repo/repo_id/category_id", file=sys.stderr)
        return 2
    if "/" not in repo:
        print(f"错误: giscus.repo 格式应为 owner/name: {repo}", file=sys.stderr)
        return 2
    owner, name = repo.split("/", 1)

    posts_dir = Path(args.posts_dir)
    all_posts = sorted(
        [p for p in posts_dir.glob("*") if p.suffix in (".markdown", ".md") and p.is_file()]
    )
    if args.only:
        posts = [p for p in all_posts if args.only in p.stem]
    else:
        posts = all_posts

    print(f"模式: {'EXECUTE（写入）' if args.execute else 'DRY-RUN（只读）'}")
    if args.only:
        print(f"过滤: --only {args.only}（匹配 {len(posts)}/{len(all_posts)} 篇）")
    print(f"仓库: {repo}  分类ID: {category_id}")
    print(f"文章数: {len(posts)}")
    print("查询已有 discussion ...")
    try:
        existing_terms = list_existing_terms(owner, name, category_id)
    except RuntimeError as exc:
        print(f"错误: 查询已有 discussion 失败: {exc}", file=sys.stderr)
        return 3
    print(f"已有 discussion: {len(existing_terms)} 条")

    # Self-check: term computation must reproduce the known discussions.
    failures, warnings = self_check(all_posts, existing_terms)
    for w in warnings:
        print(f"  警告: {w}", file=sys.stderr)
    if failures:
        print("\n自检失败 — term 计算可能有问题，已中止（未写入任何数据）:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 4
    validated = len(SELF_CHECK_TERMS) - len(warnings)
    print(f"自检通过: term 计算一致（{validated} 篇已验证，{len(warnings)} 篇孤儿 discussion）。")

    rows = []
    counts = {"exists": 0, "to_create": 0, "created": 0, "failed": 0, "skipped": 0}
    for post in posts:
        term, fm = compute_term(post)
        if term is None:
            counts["skipped"] += 1
            rows.append((post.name, "-", "skipped", "无法计算 term"))
            continue
        if term in existing_terms:
            counts["exists"] += 1
            rows.append((post.name, term, "exists", f"#{existing_terms[term]}"))
            continue
        # missing
        if not args.execute:
            counts["to_create"] += 1
            rows.append((post.name, term, "to-create", ""))
            continue
        body = build_body(fm, term, url, baseurl)
        try:
            d = create_discussion(repo_id, category_id, term, body)
            if d and d.get("number"):
                counts["created"] += 1
                existing_terms[term] = d["number"]
                rows.append((post.name, term, "created", f"#{d['number']}"))
            else:
                counts["failed"] += 1
                rows.append((post.name, term, "failed", "createDiscussion 返回为空"))
                print(f"警告: 创建失败，停止后续写入以避免部分重复: {post.name}", file=sys.stderr)
                break
        except RuntimeError as exc:
            counts["failed"] += 1
            rows.append((post.name, term, "failed", str(exc)))
            print(f"警告: 创建异常，停止后续写入: {post.name}: {exc}", file=sys.stderr)
            break

    # Report
    lines = []
    lines.append("=" * 60)
    lines.append(f"{'文件':40} {'term':24} 状态  备注")
    lines.append("-" * 60)
    for name, term, status, note in rows:
        lines.append(f"{name:40} {term:24} {status:8} {note}")
    lines.append("-" * 60)
    summary = (
        f"exists={counts['exists']} to_create={counts['to_create']} "
        f"created={counts['created']} failed={counts['failed']} skipped={counts['skipped']}"
    )
    lines.append(summary)
    report = "\n".join(lines)
    print("\n" + report)
    if args.report:
        Path(args.report).write_text(report + "\n", encoding="utf-8")
        print(f"\n报告已写入: {args.report}")

    if counts["failed"]:
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
