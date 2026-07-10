#!/usr/bin/env python3
"""Simple reader and summarizer for CODE_OF_CONDUCT.md.

Usage:
  python code_of_conduct.py --summary   # print JSON summary
  python code_of_conduct.py --print     # print raw markdown
"""
import argparse
import json
from pathlib import Path


def parse_md(text: str) -> dict:
    lines = text.splitlines()
    headings = [l for l in lines if l.strip().startswith("#")]
    bullets = [l for l in lines if l.strip().startswith("-") or l.strip().startswith("*")]
    first_paragraph = ""
    for i, l in enumerate(lines):
        if l.strip() == "":
            continue
        # take the first non-heading, non-empty block as first paragraph
        if not l.strip().startswith("#") and not l.strip().startswith("-"):
            first_paragraph = l.strip()
            break

    return {
        "total_lines": len(lines),
        "headings_count": len(headings),
        "bullets_count": len(bullets),
        "first_paragraph": first_paragraph,
        "contains_links": "http" in text or "www." in text,
    }


def extract_bullets(text: str) -> list:
    lines = text.splitlines()
    out = []
    for l in lines:
        s = l.strip()
        if s.startswith("-") or s.startswith("*"):
            # remove leading - or * and any following space
            item = s[1:].lstrip()
            out.append(item)
    return out


def main():
    parser = argparse.ArgumentParser(description="Read and summarize CODE_OF_CONDUCT.md")
    parser.add_argument("--summary", action="store_true", help="Print JSON summary")
    parser.add_argument("--print", dest="raw", action="store_true", help="Print raw markdown")
    parser.add_argument("--bullets", action="store_true", help="Print extracted bullet points as JSON array")
    args = parser.parse_args()

    md_path = Path(__file__).with_name("CODE_OF_CONDUCT.md")
    if not md_path.exists():
        print(f"ERROR: {md_path} not found")
        raise SystemExit(1)

    text = md_path.read_text(encoding="utf-8")

    if args.raw:
        print(text)
        return

    summary = parse_md(text)
    bullets = extract_bullets(text)
    if args.summary:
        print(json.dumps(summary, indent=2))
        return

    if args.bullets:
        print(json.dumps(bullets, indent=2))
        return

    # default: print short human summary
    print("Code of Conduct summary:")
    print(f"  Total lines: {summary['total_lines']}")
    print(f"  Headings: {summary['headings_count']}")
    print(f"  Bullet points: {summary['bullets_count']}")
    if summary["contains_links"]:
        print("  Contains external links")


if __name__ == "__main__":
    main()
