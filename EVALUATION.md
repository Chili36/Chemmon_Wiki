# Measuring answer quality

The branch includes 16 draft evaluation cases: 10 development and 6 held-out.
They cover SSD2, VMPR, pesticides, contaminants, baby food, all three FA/FF paths,
ambiguity and missing evidence. The review queue is `evals/REVIEW.md`; machine
labels are in `evals/cases.json`. These are assistant-authored candidate labels,
not human-reviewed gold answers. No demonstrated model-quality improvement is
claimed until labels and answer outputs have been independently reviewed.

Independent human review is unavailable for this work, as confirmed on 5 October
2026. It is deferred; the source review can proceed without it. Evaluation labels
remain draft, and no live model comparison or human-approved quality score is
claimed. The grading instructions below are retained for future availability.

## Offline validation

```sh
python tools/evaluate.py --mode select --output /tmp/chemmon-select-dry.json
python tools/evaluate.py --mode answer --split held-out --output /tmp/chemmon-answer-dry.json
```

Dry runs validate case structure and evidence paths, freeze corpus/catalogue/
prompt fingerprints and prepare the exact answer evidence. They make zero model
calls and leave quality, latency and cost metrics unmeasured. Unknown pricing is
`null`, never a claim of free usage.

## Model and catalogue comparisons

For a live run, add `--live`, set the desired `--models provider/model ...`, and
provide credentials in the environment or an explicit `--env-file .env`. Existing
credentials are never written or included in reports. Live calls incur provider
usage. Always use a new output path. Selection and answer comparisons are separate:

```sh
python tools/evaluate.py --live --env-file .env --mode select --models "$SELECTOR_A" "$SELECTOR_B" --output /tmp/select-models.json
python tools/evaluate.py --live --env-file .env --mode answer --models "$ANSWERER_A" "$ANSWERER_B" --output /tmp/answer-models.json
```

Answer mode sends identical frozen pages to every answer model; it does not let
selector differences contaminate the answer comparison. Select mode records
required-page recall across accepted alternatives and wrong-domain/path selections.
For the same model, compare `--catalog-mode summary` with `--catalog-mode hints`
to measure the contribution of `select_when`. Keep questions, corpus, prompts,
budgets and provider settings fixed. The report records fingerprints and refuses
a corpus that changes during a run. Provider-default sampling may vary between runs.
Held-out cases must remain excluded from prompt/content tuning; use
`--split held-out` only for the final assessment.

Optionally supply `--prices path.json` with a dated record containing
`{"models":{"provider/model":{"input_per_million":0,"output_per_million":0}}}`.
Replace the example zeroes with verified prices; the file hash and rates are
recorded. These are estimates, and do not model caching discounts or provider fees.

## Human answer grading

Citation membership is automatic: a citation must name a loaded full page. It
cannot prove that the page supports the claim. A reviewer must assess every
answer against the case rubric and source context, including exceptions and
recommendation strength.

Save grades as JSON with `report_sha256` for the exact original report and
`models` mapping each model to case-ID grades:

```json
{
  "report_sha256": "SHA256_OF_THE_ORIGINAL_REPORT",
  "models": {
    "provider/model": {
      "units-bin": {
        "reviewer": "REVIEWER_NAME",
        "reviewed_at": "2026-10-05",
        "answer_correct": true,
        "citations_supported": true
      }
    }
  }
}
```

```sh
python tools/evaluate.py --grade-report /tmp/answers.json --grades /tmp/grades.json --output /tmp/graded-answers.json
```

The grader requires the original report and dataset fingerprints. Unreviewed
answers retain null correctness/support scores. Summary scores include their
reviewed sample count. Report failures as well as successful cases; inspect
per-case results before changing defaults. A dry run or high recall alone does
not satisfy the plan's human-reviewed improvement acceptance criterion.
