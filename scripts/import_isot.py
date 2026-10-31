"""Normalize Kaggle ISOT Fake/Real News CSV files into one local dataset."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data"/"raw"/"ISOT"
OUT=ROOT/"data"/"processed"/"isot_articles.csv"

def read_input(path:Path,label:str)->pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Place Kaggle Fake.csv and True.csv under data/raw/ISOT/.")
    df=pd.read_csv(path)
    missing={"title","text"}-set(df.columns)
    if missing: raise ValueError(f"{path.name} missing required columns: {sorted(missing)}")
    df=df.copy(); df["label"]=label
    return df

def make_id(title:str,body:str)->str:
    return hashlib.sha256(f"{title.strip()}\n{body.strip()}".encode("utf-8",errors="replace")).hexdigest()[:20]

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--raw-dir",type=Path,default=RAW); p.add_argument("--output",type=Path,default=OUT)
    a=p.parse_args()
    df=pd.concat([read_input(a.raw_dir/"Fake.csv","fake"),read_input(a.raw_dir/"True.csv","real")],ignore_index=True,sort=False)
    df["title"]=df.title.fillna("").astype(str).str.strip()
    df["text"]=df.text.fillna("").astype(str).str.strip()
    for col in ("subject","date"):
        if col not in df: df[col]=""
        df[col]=df[col].fillna("").astype(str)
    df["article_text"]=(df.title+"\n\n"+df.text).str.strip()
    df["article_id"]=[make_id(t,b) for t,b in zip(df.title,df.text)]
    df["source_dataset"]="Kaggle ISOT Fake and Real News Dataset"
    before=len(df); df=df.drop_duplicates("article_id"); df=df[df.article_text.ne("")].reset_index(drop=True)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    cols=["article_id","title","text","article_text","label","subject","date","source_dataset"]
    df[cols].to_csv(a.output,index=False,encoding="utf-8")
    print(f"Input rows: {before:,} | Exported: {len(df):,} | Removed: {before-len(df):,}")
    print(df.label.value_counts().to_string()); print(f"Saved {a.output}")
if __name__=="__main__": main()
