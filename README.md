# NewsLens

**NewsLens** is a Django research dashboard prototype with a Kaggle-only dataset and ML baseline workflow. The current UI includes Overview, Articles, Compare, Analysis, Narrative Trends, Settings, and Profile.

> **Research integrity note:** Dashboard pages still include illustrative demo values. They are not findings from the Kaggle dataset. The first implemented ML workflow is an ISOT inherited-label baseline for experimentation, not a factuality verdict engine or media-bias detector.

## Current scope

- Dataset source policy: **Kaggle only**.
- Initial dataset: [Fake and Real News Dataset (ISOT)](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset).
- Local CSV import, structural validation, TF-IDF + Logistic Regression baseline.
- Evaluation report with class metrics and confusion matrix.
- Raw dataset, processed data, trained model, and generated reports remain local and are excluded from Git.

## Setup

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Download the dataset

1. Open the [ISOT Kaggle dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset).
2. Download the dataset ZIP through Kaggle and inspect its current license/terms.
3. Extract the original `Fake.csv` and `True.csv` files into `data/raw/ISOT/`.

The raw source CSVs are not tracked. Keep `Fake.csv` and `True.csv` local.

## Prepare the dataset

```powershell
python scripts/import_isot.py
python scripts/validate_dataset.py
```

The importer requires `title` and `text`; it retains `subject` and `date` if available. It generates `data/processed/isot_articles.csv` with `article_id`, `title`, `text`, `article_text`, `label`, `subject`, `date`, and `source_dataset`. The inherited label is mapped from the source file (`Fake.csv` to `fake`, `True.csv` to `real`).

## Train a baseline

```powershell
python scripts/train_baseline.py
```

Baseline: TF-IDF word unigrams/bigrams + class-weighted Logistic Regression, using a reproducible stratified random holdout (seed 42). Outputs:

- `models/isot_tfidf_logreg.joblib`
- `reports/isot_baseline_metrics.json`

The report includes accuracy, macro-F1, per-class precision/recall/F1, and confusion matrix.

## Interpretation and limitations

- ISOT labels are inherited dataset labels, not independent fact-check judgments for every article.
- Publisher/source selection, writing style, duplicates, and event/subject distributions may leak label cues.
- A random split is a pipeline smoke-test, not evidence of generalization. Add duplicate-aware and source-held-out validation before strong claims.
- Never present a prediction as proof an article is false, a publisher's trustworthiness, or a media-bias score.
- ISOT does not supply the bias/framing annotations needed for our original narrative research objective.
- Check the current dataset license, attribution, and usage terms before use or redistribution.

See [Dataset Card](docs/DATASET_CARD_ISOT.md).

## Project structure

- `config/`: Django configuration.
- `dashboard/`: UI views and service layer; much of the displayed data is mock content.
- `templates/`: Django pages.
- `static/`: CSS and JavaScript.
- `scripts/`: Kaggle CSV import, validation, and baseline training.
- `data/`: dataset templates and local-data locations.

## Next milestones

1. Connect dataset summary and measured evaluation results to a Django results page.
2. Add provenance and near-duplicate diagnostics.
3. Add group-aware evaluation when source metadata permits.
4. Consider a Kaggle-hosted annotated framing corpus only after reviewing labels and terms.
5. Replace mock dashboard metrics only with reproducible computed results.

## Current UI caveat

The dashboard remains a visual prototype: some analysis actions, settings persistence, filters, and chart values are hardcoded or stubbed. Do not cite those values as research findings.

## Source
- [ISOT dataset on Kaggle](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
