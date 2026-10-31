# Dataset Card: Kaggle ISOT Fake and Real News Dataset

## Intended role
Initial educational baseline for binary classification of inherited `fake` / `real` labels. This is not a media-bias or narrative-framing annotation corpus.

## Source
Kaggle: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
Record the actual download date, version, author attribution and license displayed when downloading. Terms can change.

## Labels and expected fields
The import maps rows from `Fake.csv` to `fake` and `True.csv` to `real`. Expected required columns are `title` and `text`; `subject` and `date` are retained if available.

## Risks and limitations
- Dataset labels are inherited and are not independent fact-check verdicts.
- Source-selection artifacts and publisher-writing styles may correlate with labels.
- Random holdout scores may overestimate generalization.
- Never present a model prediction as proof that an article is false or as a publisher trust score.
- This data does not support media-bias ground truth.
- Inspect near duplicates, source coverage, dates and subjects. Pursue group/source-held-out validation before strong claims.

## Data stewardship
Raw files, processed datasets, and model binaries are not committed. Respect current Kaggle terms, source attribution, and underlying rights.

## Evaluation
The baseline's stratified random holdout is a pipeline smoke test, not deployment-grade evaluation. Report per-class precision/recall/F1 and confusion matrix with caveats.
