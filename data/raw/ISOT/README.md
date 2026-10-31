# Kaggle ISOT raw data

Download from https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
and extract the original `Fake.csv` and `True.csv` into this directory.

Raw downloads are intentionally excluded from Git. Check the dataset's current license,
attribution requirements, and permitted use before research or redistribution.

Expected local files: `Fake.csv`, `True.csv`.

From repository root:
```bash
python scripts/import_isot.py
python scripts/validate_dataset.py
python scripts/train_baseline.py
```
