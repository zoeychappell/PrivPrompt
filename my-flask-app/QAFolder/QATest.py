# pip install bert-score sentence-transformers textdistance rapidfuzz numpy
# Requires app.py to have run the QA portion of the code first before running this code

from sentence_transformers import SentenceTransformer, util, CrossEncoder
import textdistance
from rapidfuzz import fuzz
from bert_score import score as bertscore
import re
import json
import numpy as np
import csv
import os
from datetime import datetime

# ================== SAVE RESULTS TO CSV ==================
csv_filename = "similarity_scores.csv"
csv_reliable = "reliable_scores.csv"

with open("pii_data.json", encoding="utf-8") as f:
    data = json.load(f)

# Ensure both CSV files exist (with header row if empty or missing)
def ensure_csv_exists(filename, fieldnames):
    """Create a CSV with headers if it doesn't exist or is empty."""
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

# ================== CONFIG / INPUTS ==================
# If you already load texts from files, keep that. (unchanged)
with open("text1.txt", encoding="utf-8") as f:
    text1 = f.read()

with open("text2.txt", encoding="utf-8") as f:
    text2 = f.read()

# >>> NEW: Bring in your detected PII
PII = {
    "emails": data["emails"],
    "ssns":   data["ssns"],
    "names":  data["names"],
    "phones": data["phones"]
}
# If you also have the sanitized placeholders you use (e.g., "name1", "user1@email.com"),
# add them here to prevent them from affecting similarity:
SAN_PLACEHOLDERS = {
    "names": [r"name\d+"],
    "emails": [r"user\d+@email\.com"],
    "ssns": [r"xxx-xx-\d{4}"],
    "phones": [r"xxx-xxx-\d{4}"]
}

# ================== MODELS (unchanged) ==================
bi_model = SentenceTransformer('all-MiniLM-L6-v2')  # small, fast, free
ce_model = CrossEncoder('cross-encoder/stsb-roberta-base')

# ================== HELPERS ==================
def safe_regex_escape_list(items):
    """Escape a list of strings for use in regex OR pattern."""
    return [re.escape(s) for s in items if s]

# >>> NEW: canonicalize both outputs by masking PII AND placeholders
def canonicalize_text(t: str,
                      pii: dict,
                      san_placeholders: dict,
                      tags=("NAME", "EMAIL", "SSN", "PHONE")) -> str:
    out = t

    # Build patterns once
    name_patterns  = safe_regex_escape_list(pii.get("names", [])) + safe_regex_escape_list(san_placeholders.get("names", []))
    email_patterns = safe_regex_escape_list(pii.get("emails", [])) + safe_regex_escape_list(san_placeholders.get("emails", []))
    ssn_patterns   = safe_regex_escape_list(pii.get("ssns", [])) + safe_regex_escape_list(san_placeholders.get("ssns", []))
    phone_patterns = safe_regex_escape_list(pii.get("phones", [])) + safe_regex_escape_list(san_placeholders.get("phones", []))

    # Also catch generic shapes in case lists miss something (optional; comment out if you don't want heuristics)
    email_patterns += [r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"]
    ssn_patterns   += [r"\b\d{3}-\d{2}-\d{4}\b"]
    phone_patterns += [r"\b\d{3}-\d{3}-\d{4}\b"]
    # For names, if you don't want heuristics, rely only on your list.

    # Replace occurrences (case-insensitive)
    if name_patterns:
        out = re.sub(r"(?i)\b(" + "|".join(name_patterns) + r")\b", f"<{tags[0]}>", out)
    if email_patterns:
        out = re.sub(r"(?i)(" + "|".join(email_patterns) + r")", f"<{tags[1]}>", out)
    if ssn_patterns:
        out = re.sub(r"(?i)(" + "|".join(ssn_patterns) + r")", f"<{tags[2]}>", out)
    if phone_patterns:
        out = re.sub(r"(?i)(" + "|".join(phone_patterns) + r")", f"<{tags[3]}>", out)

    return out

# ================== METRICS (y_raw vs y_san) ==================
# 1) SBERT (bi-encoder)
emb1 = bi_model.encode(text1, convert_to_tensor=True)
emb2 = bi_model.encode(text2, convert_to_tensor=True)
sbert_cos = util.cos_sim(emb1, emb2).item()  # ~[0,1] higher = more similar

# 2) Cross-Encoder STS
ce_score = float(ce_model.predict([(text1, text2)])[0])  # ~[0,1]

# 3) Lexical baselines
lev_ratio = float(textdistance.levenshtein.normalized_similarity(text1, text2))  # [0..1]

w1 = set(text1.lower().split())
w2 = set(text2.lower().split())
jaccard_words = len(w1 & w2) / len(w1 | w2) if (w1 or w2) else 1.0  # [0..1]

rf_token_set = fuzz.token_set_ratio(text1, text2) / 100.0  # [0..1]

# 4) BERTScore (semantic)
P, R, F1 = bertscore([text1], [text2], lang="en", model_type="microsoft/deberta-base-mnli")
bert_f1 = float(F1[0])   # ~[0,1] higher = more similar

# Ensembles (original + recommended)
ensemble = 0.45 * sbert_cos + 0.45 * ce_score + 0.10 * max(jaccard_words, rf_token_set)
ensemble_semantic = 0.5 * sbert_cos + 0.5 * bert_f1

# >>> NEW: Non-PII drift path (canonicalized y_raw and y_san)
text1_c = canonicalize_text(text1, PII, SAN_PLACEHOLDERS)
text2_c = canonicalize_text(text2, PII, SAN_PLACEHOLDERS)

# Recompute semantic metrics on canonicalized texts
emb1c = bi_model.encode(text1_c, convert_to_tensor=True)
emb2c = bi_model.encode(text2_c, convert_to_tensor=True)
sbert_cos_nonpii = util.cos_sim(emb1c, emb2c).item()

Pc, Rc, F1c = bertscore([text1_c], [text2_c], lang="en", model_type="microsoft/deberta-base-mnli")
bert_f1_nonpii = float(F1c[0])

ensemble_semantic_nonpii = 0.5 * sbert_cos_nonpii + 0.5 * bert_f1_nonpii

# >>> NEW: Simple “surface” diagnostics
delta_len_chars = len(text2) - len(text1)

# ================== PRINT ==================
print(f"SBERT cosine similarity             (Most reliable) : {sbert_cos:.3f}")
print(f"Cross-Encoder (STSB) similarity     (Unreliable)    : {ce_score:.3f}")
print(f"BERTScore F1 (semantic)             (Kinda reliable): {bert_f1:.3f}")
print(f"Levenshtein ratio (lexical)         (Unreliable)    : {lev_ratio:.3f}")
print(f"Jaccard (unique words)              (Unreliable)    : {jaccard_words:.3f}")
print(f"RapidFuzz token_set_ratio(lexical)  (Unsure)        : {rf_token_set:.3f}")
print(f"Ensemble (original heuristic)       (Unreliable)    : {ensemble:.3f}")
print(f"Ensemble (SBERT + BERTScore)        (Recommended)   : {ensemble_semantic:.3f}")

# >>> NEW: Non-PII reporting
print("\n--- Non-PII drift (canonicalized) ---")
print(f"SBERT cosine (non-PII)                              : {sbert_cos_nonpii:.3f}")
print(f"BERTScore F1 (non-PII)                              : {bert_f1_nonpii:.3f}")
print(f"Ensemble (semantic, non-PII)                        : {ensemble_semantic_nonpii:.3f}")

# >>> NEW: Deltas / diagnostics
print("\n--- Diagnostics ---")
print(f"Δ length (chars, sanitized - raw)                   : {delta_len_chars:+d}")

# >>> NEW: Example thresholding
threshold = 0.70
print(f"\nHighly similar overall (SBERT+BERTScore)? {'YES' if ensemble_semantic >= threshold else 'NO'}")
print(f"Meaning preserved outside PII (non-PII ensemble)?   {'YES' if ensemble_semantic_nonpii >= threshold else 'NO'}")

# Prepare all scores you might want to analyze later
row = {
    "timestamp": datetime.now().isoformat(timespec="seconds"),
    "LLM": data["llm_choice"],
    "sbert_cos": sbert_cos,
    "ce_score": ce_score,
    "bert_f1": bert_f1,
    "lev_ratio": lev_ratio,
    "jaccard_words": jaccard_words,
    "rf_token_set": rf_token_set,
    "ensemble": ensemble,
    "ensemble_semantic": ensemble_semantic,
    "sbert_cos_nonpii": sbert_cos_nonpii,
    "bert_f1_nonpii": bert_f1_nonpii,
    "ensemble_semantic_nonpii": ensemble_semantic_nonpii,
    "delta_len_chars": delta_len_chars,
    "threshold": threshold,
    "highly_similar_overall": ensemble_semantic >= threshold,
    "meaning_preserved_outside_pii": ensemble_semantic_nonpii >= threshold
}

# Prepare subset of the most reliable scores
row_lite = {
    "timestamp": row["timestamp"],
    "LLM": data["llm_choice"],
    "sbert_cos": sbert_cos,
    "bert_f1": bert_f1,
    "ensemble_semantic": ensemble_semantic,
    "delta_len_chars": delta_len_chars
}

# Ensure CSVs exist before appending
ensure_csv_exists(csv_filename, list(row.keys()))
ensure_csv_exists(csv_reliable, list(row_lite.keys()))
def append_to_csv(filename, row):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writerow(row)
        
append_to_csv(csv_filename, row)
append_to_csv(csv_reliable, row_lite)

print(f"\nSaved scores to {csv_filename} and {csv_reliable}")
