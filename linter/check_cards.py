"""Arcanum lint plugin: validate tarot card names against game data."""

import ast
import json
from pathlib import Path

from bardic.cli.lint import LintReport, extract_python_code


def check_card_names(story_data: dict, report: LintReport, project_root: Path):
    """AW001: Card names in Deck() calls must match tarot-images.json."""
    # Load canonical card names
    images_file = project_root / "assets" / "images" / "tarot-images.json"
    if not images_file.exists():
        return

    with open(images_file, encoding="utf-8") as f:
        data = json.load(f)

    valid_names = {card["name"] for card in data.get("cards", [])}
    if not valid_names:
        return

    # Find card names in Deck(cards=[...]) calls
    code_snippets = extract_python_code(story_data)
    found_names: dict[str, list[str]] = {}  # {card_name: [contexts]}

    for code, ctx in code_snippets:
        import textwrap

        code = textwrap.dedent(code)
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            # Match Deck(...) calls
            func = node.func
            if not (isinstance(func, ast.Name) and func.id == "Deck"):
                continue

            # Find the cards argument (first positional or cards= keyword)
            cards_arg = None
            if node.args and isinstance(node.args[0], ast.List):
                cards_arg = node.args[0]
            for kw in node.keywords:
                if kw.arg == "cards" and isinstance(kw.value, ast.List):
                    cards_arg = kw.value

            if cards_arg is None:
                continue

            for elt in cards_arg.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    name = elt.value
                    if name not in valid_names:
                        found_names.setdefault(name, []).append(ctx)

    # Also check string comparisons: card.name == "..." or ... == "Card Name"
    for code, ctx in code_snippets:
        import textwrap

        code = textwrap.dedent(code)
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError:
            try:
                tree = ast.parse(code, mode="eval")
            except SyntaxError:
                continue

        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare):
                continue
            # Check for .name == "string" pattern
            for comparator in node.comparators:
                if isinstance(comparator, ast.Constant) and isinstance(
                    comparator.value, str
                ):
                    _check_card_compare(node.left, comparator.value, ctx, valid_names, found_names)
            # Check left side too
            if isinstance(node.left, ast.Constant) and isinstance(
                node.left.value, str
            ):
                for comparator in node.comparators:
                    _check_card_compare(comparator, node.left.value, ctx, valid_names, found_names)

    # Report findings
    import difflib

    for name, contexts in sorted(found_names.items()):
        close = difflib.get_close_matches(name, valid_names, n=1, cutoff=0.7)
        hint = f"Did you mean '{close[0]}'?" if close else "Check tarot-images.json for valid names"
        ctx_str = contexts[0]
        if len(contexts) > 1:
            ctx_str += f" (+{len(contexts) - 1} more)"
        report.warning(
            "AW001",
            f"Unknown card name '{name}' (in {ctx_str})",
            hint=hint,
        )


def _check_card_compare(node, string_value, ctx, valid_names, found_names):
    """Check if a comparison node looks like a card name check."""
    # Match patterns like: card.name == "string" or session.cards[0].name == "string"
    if isinstance(node, ast.Attribute) and node.attr == "name":
        if string_value not in valid_names and len(string_value) > 2:
            # Only flag strings that look like card names (capitalized, not too short)
            if string_value[0].isupper() or string_value.startswith("The "):
                found_names.setdefault(string_value, []).append(ctx)
