"""Arcanum lint plugin: validate spread IDs against spreads-config.json."""

import ast
import json
import textwrap
from pathlib import Path

from bardic.cli.lint import LintReport, extract_python_code


def check_spread_ids(story_data: dict, report: LintReport, project_root: Path):
    """AW002: Spread IDs in Reading() calls must match spreads-config.json."""
    # Load valid spread IDs
    config_file = project_root / "game_logic" / "spreads-config.json"
    if not config_file.exists():
        return

    with open(config_file, encoding="utf-8") as f:
        data = json.load(f)

    valid_ids = set()
    spreads = data.get("spreads", [])
    if isinstance(spreads, list):
        valid_ids = {s.get("id", "") for s in spreads} - {""}
    elif isinstance(spreads, dict):
        valid_ids = set(spreads.keys())

    if not valid_ids:
        return

    # Find spread_id values in Reading(spread_id="...") calls
    code_snippets = extract_python_code(story_data)
    bad_ids: dict[str, list[str]] = {}  # {spread_id: [contexts]}

    for code, ctx in code_snippets:
        code = textwrap.dedent(code)
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            # Match Reading(...) calls
            func = node.func
            if not (isinstance(func, ast.Name) and func.id == "Reading"):
                continue

            # Find spread_id keyword argument
            for kw in node.keywords:
                if kw.arg == "spread_id" and isinstance(kw.value, ast.Constant):
                    spread_id = kw.value.value
                    if isinstance(spread_id, str) and spread_id not in valid_ids:
                        bad_ids.setdefault(spread_id, []).append(ctx)

    # Report findings
    import difflib

    for spread_id, contexts in sorted(bad_ids.items()):
        close = difflib.get_close_matches(spread_id, valid_ids, n=1, cutoff=0.6)
        hint = (
            f"Did you mean '{close[0]}'?"
            if close
            else f"Valid IDs: {', '.join(sorted(valid_ids)[:8])}..."
        )
        ctx_str = contexts[0]
        if len(contexts) > 1:
            ctx_str += f" (+{len(contexts) - 1} more)"
        report.warning(
            "AW002",
            f"Unknown spread ID '{spread_id}' (in {ctx_str})",
            hint=hint,
        )
