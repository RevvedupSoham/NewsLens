"""Train a reproducible TF-IDF + Logistic Regression baseline on normalized ISOT."""
from __future__ import annotations
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
import joblib,pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
ROOT=Path(__file__).resolve().parents[1]
def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data",type=Path,default=ROOT/"data/processed/isot_articles.csv")
    p.add_argument("--model-out",type=Path,default=ROOT/"models/isot_tfidf_logreg.joblib")
    p.add_argument("--report-out",type=Path,default=ROOT/"reports/isot_baseline_metrics.json")
    p.add_argument("--test-size",type=float,default=.2); p.add_argument("--seed",type=int,default=42)
    a=p.parse_args()
    if not .1<=a.test_size<=.4: p.error("--test-size must be between 0.1 and 0.4")
    if not a.data.exists(): raise FileNotFoundError(f"{a.data} not found. Run scripts/import_isot.py first.")
    df=pd.read_csv(a.data).dropna(subset=["article_text","label"]).copy()
    df["article_text"]=df.article_text.astype(str).str.strip()
    df=df[df.article_text.ne("") & df.label.isin(["fake","real"])]
    df=df.drop_duplicates("article_id" if "article_id" in df else "article_text")
    if df.label.nunique()!=2 or df.label.value_counts().min()<2: raise ValueError("Need at least 2 samples per class.")
    xtr,xte,ytr,yte=train_test_split(df.article_text,df.label,test_size=a.test_size,random_state=a.seed,stratify=df.label)
    model=Pipeline([("tfidf",TfidfVectorizer(lowercase=True,strip_accents="unicode",stop_words="english",max_features=120000,ngram_range=(1,2),min_df=2,sublinear_tf=True)),("classifier",LogisticRegression(max_iter=1500,class_weight="balanced",random_state=a.seed))])
    model.fit(xtr,ytr); pred=model.predict(xte)
    metrics={"dataset":"Kaggle ISOT Fake and Real News Dataset","task":"binary inherited-label classification","created_at_utc":datetime.now(timezone.utc).isoformat(),"seed":a.seed,"rows_used":len(df),"train_rows":len(xtr),"test_rows":len(xte),"class_counts":{k:int(v) for k,v in df.label.value_counts().items()},"accuracy":float(accuracy_score(yte,pred)),"macro_f1":float(f1_score(yte,pred,average="macro")),"confusion_matrix_labels":["fake","real"],"confusion_matrix":confusion_matrix(yte,pred,labels=["fake","real"]).tolist(),"classification_report":classification_report(yte,pred,labels=["fake","real"],output_dict=True,zero_division=0),"split_note":"Random stratified holdout; not source-held-out; likely subject to collection artifacts.","interpretation_warning":"Inherited dataset labels are not independently verified truth. Never present predictions as proof of falsity or a media-bias score."}
    a.model_out.parent.mkdir(parents=True,exist_ok=True); a.report_out.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(model,a.model_out); a.report_out.write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    print(f"Rows={len(df):,}; train={len(xtr):,}; test={len(xte):,}; accuracy={metrics['accuracy']:.4f}; macro-F1={metrics['macro_f1']:.4f}")
    print(f"Model: {a.model_out}\nMetrics: {a.report_out}\nCaution: random-split metrics may reflect publisher/source artifacts.")
if __name__=="__main__": main()
