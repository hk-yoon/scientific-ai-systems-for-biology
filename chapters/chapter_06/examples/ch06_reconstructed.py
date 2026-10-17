"""Chapter 6.12.5: newly reconstructed educational demonstration.
NOT a verbatim recovery of the damaged Word code. Synthetic data only.
"""
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score


def build_data(seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(20):
        culture = f"C{i+1:02d}"
        stress = int(i >= 10)
        for j in range(20):
            # Independent culture offsets induce within-culture correlation.
            # Parameter values are NEW pedagogical choices, not original constants.
            rows.append((culture, j, stress,
                         rng.normal(3.7 + 1.5 * stress, .45),
                         rng.normal(1.2 + .7 * stress, .23),
                         rng.normal(.45 + .22 * stress, .10)))
    return pd.DataFrame(rows, columns=["culture_id", "cell_id", "stress", "length", "width", "roughness"])


def run(seed=42):
    df = build_data(seed)
    test_cultures = {"C09", "C10", "C19", "C20"}
    train = df.loc[~df.culture_id.isin(test_cultures)].copy()
    test = df.loc[df.culture_id.isin(test_cultures)].copy()
    assert set(train.culture_id).isdisjoint(set(test.culture_id))
    features = ["length", "width", "roughness"]
    model = Pipeline([("scale", StandardScaler()),
                      ("clf", LogisticRegression(max_iter=1000, random_state=seed))])
    model.fit(train[features], train.stress)
    pred = model.predict(test[features])
    proba = model.predict_proba(test[features])[:, 1]
    cm = confusion_matrix(test.stress, pred, labels=[0, 1])
    auc = roc_auc_score(test.stress, proba)
    summary = {"train_rows": len(train), "test_rows": len(test),
               "train_cultures": train.culture_id.nunique(),
               "test_cultures": test.culture_id.nunique(),
               "test_class_counts": test.stress.value_counts().sort_index().to_dict(),
               "confusion_matrix": cm.tolist(), "roc_auc": float(auc)}
    print(summary)
    print(classification_report(test.stress, pred, digits=3))
    return summary

if __name__ == "__main__":
    run()
