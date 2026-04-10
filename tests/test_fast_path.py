from __future__ import annotations

import pytest

from wiki_api.app import (
    _CHEMMON_RULE_TO_SLICES,
    _try_deterministic_selection,
)


# -------------------------------------------------------------------------
# Rule-ID lookup path
# -------------------------------------------------------------------------


def test_chemmon_rule_id_cross_cutting() -> None:
    result = _try_deterministic_selection("What does CHEMMON01 require?")
    assert result is not None
    assert "business-rules-cross-cutting.md" in result


def test_chemmon_rule_id_vmpr_adds_cross_cutting() -> None:
    result = _try_deterministic_selection("What does CHEMMON76 say about species?")
    assert result is not None
    assert "business-rules-vmpr.md" in result
    # Cross-cutting is always appended as a companion
    assert "business-rules-cross-cutting.md" in result


def test_chemmon_rule_id_pesticide_adds_cross_cutting() -> None:
    result = _try_deterministic_selection("CHEMMON95 origin country rule")
    assert result is not None
    assert "business-rules-pesticide.md" in result
    assert "business-rules-cross-cutting.md" in result


def test_chemmon_rule_id_contaminant_adds_cross_cutting() -> None:
    result = _try_deterministic_selection("Explain CHEMMON12 for acrylamide")
    assert result is not None
    assert "business-rules-contaminant.md" in result
    assert "business-rules-cross-cutting.md" in result


def test_chemmon_rule_id_additives_adds_cross_cutting() -> None:
    result = _try_deterministic_selection("What does CHEMMON36 require?")
    assert result is not None
    assert "business-rules-additives.md" in result
    assert "business-rules-cross-cutting.md" in result


def test_chemmon_rule_id_baby_food() -> None:
    result = _try_deterministic_selection("CHEMMON55 baby food exclusion")
    assert result is not None
    assert "business-rules-baby-food.md" in result


def test_chemmon_rule_id_duplicate_chemmon03_returns_both() -> None:
    """CHEMMON03 is defined in both cross-cutting and pesticide slices
    (pre-existing source guidance duplication). Both must be returned."""
    result = _try_deterministic_selection("What does CHEMMON03 cover?")
    assert result is not None
    assert "business-rules-cross-cutting.md" in result
    assert "business-rules-pesticide.md" in result


def test_chemmon_rule_id_ambiguous_chemmon43_returns_both() -> None:
    """CHEMMON43 (cross-cutting, PPP/VMPR) and CHEMMON43_b (additives)
    share a numeric root. Ambiguous IDs must return all possible slices."""
    result = _try_deterministic_selection("Is CHEMMON43 applicable?")
    assert result is not None
    assert "business-rules-cross-cutting.md" in result
    assert "business-rules-additives.md" in result


def test_chemmon_rule_id_leading_zeros_accepted() -> None:
    result = _try_deterministic_selection("What is CHEMMON001?")
    assert result is not None
    assert "business-rules-cross-cutting.md" in result


def test_chemmon_rule_id_case_insensitive() -> None:
    result = _try_deterministic_selection("what is chemmon76?")
    assert result is not None
    assert "business-rules-vmpr.md" in result


def test_chemmon_rule_id_result_dedupes_and_preserves_order() -> None:
    """Cross-cutting should appear exactly once even when the rule ID
    naturally maps to it plus the companion injection."""
    result = _try_deterministic_selection("CHEMMON08 and CHEMMON30")
    assert result is not None
    assert result.count("business-rules-cross-cutting.md") == 1


def test_unknown_chemmon_rule_id_falls_through_to_keyword_or_none() -> None:
    # CHEMMON999 is not in the mapping; with no other keywords, fall through
    result = _try_deterministic_selection("What is CHEMMON999?")
    assert result is None


# -------------------------------------------------------------------------
# Keyword patterns
# -------------------------------------------------------------------------


def test_keyword_vmpr() -> None:
    result = _try_deterministic_selection("What are the VMPR rules for wild game?")
    assert result == [
        "business-rules-vmpr.md",
        "business-rules-cross-cutting.md",
        "vmpr-reporting.md",
    ]


def test_keyword_pesticide() -> None:
    result = _try_deterministic_selection("How do I report MRL data for copper?")
    assert result == [
        "business-rules-pesticide.md",
        "business-rules-cross-cutting.md",
        "pesticide-reporting.md",
    ]


def test_keyword_baby_food() -> None:
    result = _try_deterministic_selection("Can I report baby food under VMPR?")
    # VMPR is scanned first in the pattern list, so VMPR wins on this question
    assert result is not None
    assert "business-rules-vmpr.md" in result


def test_keyword_baby_food_alone() -> None:
    result = _try_deterministic_selection("What counts as infant formula?")
    assert result == [
        "business-rules-baby-food.md",
        "baby-food-reporting.md",
    ]


def test_keyword_food_additive() -> None:
    result = _try_deterministic_selection("How do I code a sweetener?")
    assert result == [
        "business-rules-additives.md",
        "business-rules-cross-cutting.md",
        "food-additives-reporting.md",
    ]


def test_keyword_contaminant() -> None:
    result = _try_deterministic_selection("How do I report dioxin results?")
    assert result == [
        "business-rules-contaminant.md",
        "business-rules-cross-cutting.md",
        "contaminant-reporting.md",
    ]


def test_keyword_legal_limit() -> None:
    result = _try_deterministic_selection("What is the maximum permitted level for lead?")
    # "lead" is not a pattern; "maximum permitted level" triggers the legal limits slice
    assert result == ["business-rules-legal-limits.md"]


def test_keyword_case_insensitive() -> None:
    result = _try_deterministic_selection("VMPR RULES FOR INSECTS")
    assert result is not None
    assert "business-rules-vmpr.md" in result


# -------------------------------------------------------------------------
# Fall-through / non-matches
# -------------------------------------------------------------------------


def test_off_pattern_question_returns_none() -> None:
    """Questions that don't match any pattern must fall through to the LLM selector."""
    result = _try_deterministic_selection("Explain SSD2 sample event consistency validation.")
    assert result is None


def test_empty_question_returns_none() -> None:
    assert _try_deterministic_selection("") is None


def test_generic_schema_question_returns_none() -> None:
    result = _try_deterministic_selection("What is the purpose of the frontmatter schema?")
    assert result is None


# -------------------------------------------------------------------------
# Rule-to-slice mapping sanity
# -------------------------------------------------------------------------


def test_rule_to_slices_mapping_nonempty() -> None:
    assert len(_CHEMMON_RULE_TO_SLICES) > 50


@pytest.mark.parametrize(
    "rule_id,expected_slice",
    [
        (1, "business-rules-cross-cutting.md"),
        (28, "business-rules-vmpr.md"),
        (2, "business-rules-pesticide.md"),
        (9, "business-rules-contaminant.md"),
        (36, "business-rules-additives.md"),
        (55, "business-rules-baby-food.md"),
    ],
)
def test_rule_to_slices_coverage(rule_id: int, expected_slice: str) -> None:
    slices = _CHEMMON_RULE_TO_SLICES.get(rule_id)
    assert slices is not None
    assert expected_slice in slices
