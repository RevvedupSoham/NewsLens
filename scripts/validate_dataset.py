"""Check structural quality of the normalized local ISOT CSV."""
import argparse
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("csv",nargs="?",type=Path,default=ROOT/"data/processed/isot_articles.csv"); a=p.parse_args()
    if not a.csv.exists(): raise FileNotFoundError(f"{a.csv} missing. Run scripts/import_isot.py.")
    df=pd.read_csv(a.csv); required={"article_id","title","text","article_text","label"}; missing=required-set(df)
    if missing: raise SystemExit(f"FAIL: missing columns {sorted(missing)}")
    issues={"rows":len(df),"missing_ids":int(df.article_id.isna().sum()),"duplicate_ids":int(df.article_id.duplicated().sum()),"empty_text":int(df.article_text.fillna("").str.strip().eq("").sum()),"unknown_labels":sorted(set(df.label.dropna())-{"fake","real"}),"class_counts":{k:int(v) for k,v in df.label.value_counts().items()}}
    for k,v in issues.items(): print(f"{k}: {v}")
    if not issues["rows"] or issues["missing_ids"] or issues["duplicate_ids"] or issues["empty_text"] or issues["unknown_labels"] or set(issues["class_counts"])!={"fake","real"}: raise SystemExit("FAIL: review dataset quality issues.")
    print("PASS: structural checks only. Label accuracy, bias, source diversity and license remain unverified.")
if __name__=="__main__": main()
