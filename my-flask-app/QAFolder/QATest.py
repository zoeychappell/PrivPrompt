# pip install bert-score sentence-transformers numpy
# Requires app.py to have run the QA portion of the code first before running this code

from sentence_transformers import SentenceTransformer, util
from bert_score import score as bertscore
import re, json, csv, os
from datetime import datetime

# ================== SAVE RESULTS TO CSV ==================
csv_reliable = "reliable_scores.csv"
csv_pii_eval = "pii_sanitization_eval.csv"

with open("pii_data.json", encoding="utf-8") as f:
    data = json.load(f)

def ensure_csv_exists(filename, fieldnames):
    """Create a CSV with headers if it doesn't exist or is empty."""
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def append_to_csv(filename, row):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writerow(row)

# ================== CONFIG / INPUTS ==================
with open("text1.txt", encoding="utf-8") as f:
    text1 = f.read()

with open("text2.txt", encoding="utf-8") as f:
    text2 = f.read()

# Detected PII from your JSON (safe .get for migration)
PII = {
    "emails": data.get("emails", []),
    "ssns":   data.get("ssns", []),
    "names":  data.get("names", []),
    "phones": data.get("phones", []),
    "dates":  data.get("dates", []),   
}

# Your sanitizer placeholders (regex patterns; DO NOT escape)
SAN_PLACEHOLDERS = {
    "names":  [r"name\d+"],
    "emails": [r"user\d+@email\.com"],
    "ssns":   [r"xxx-xx-\d{4}"],
    "phones": [r"xxx-xxx-\d{4}"],
    "dates":  [r"date\d+", r"dob\d+", r"xx/xx/xxxx", r"xxxx-xx-xx"],
}

# ================== MODELS ==================
bi_model = SentenceTransformer("all-MiniLM-L6-v2")  # SBERT bi-encoder

# ================== HELPERS ==================
def safe_regex_escape_list(items):
    """Escape detected PII literals for regex OR pattern."""
    return [re.escape(s) for s in items if s]

def canonicalize_text(
    t: str,
    pii: dict,
    san_placeholders: dict,
    tags=("NAME", "EMAIL", "SSN", "PHONE", "DATE"),
    use_heuristics=True,
) -> str:
    out = t

    # Literal PII (escape!)
    name_literals  = safe_regex_escape_list(pii.get("names", []))
    email_literals = safe_regex_escape_list(pii.get("emails", []))
    ssn_literals   = safe_regex_escape_list(pii.get("ssns", []))
    phone_literals = safe_regex_escape_list(pii.get("phones", []))
    date_literals  = safe_regex_escape_list(pii.get("dates", []))

    # Placeholder regexes (DO NOT escape!)
    name_ph  = san_placeholders.get("names", [])
    email_ph = san_placeholders.get("emails", [])
    ssn_ph   = san_placeholders.get("ssns", [])
    phone_ph = san_placeholders.get("phones", [])
    date_ph  = san_placeholders.get("dates", [])

    # Combine into patterns
    name_patterns  = name_literals + list(name_ph)
    email_patterns = email_literals + list(email_ph)
    ssn_patterns   = ssn_literals + list(ssn_ph)
    phone_patterns = phone_literals + list(phone_ph)
    date_patterns  = date_literals + list(date_ph)

    if use_heuristics:
        email_patterns += [r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"]
        ssn_patterns   += [r"\b\d{3}-\d{2}-\d{4}\b"]
        phone_patterns += [
            r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
            r"\(\d{3}\)\s*\d{3}[-.\s]?\d{4}",
            r"\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
        ]
        date_patterns += [
            r"\b\d{4}-\d{2}-\d{2}\b",                     # YYYY-MM-DD
            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",               # M/D/YY(YY)
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},\s+\d{4}\b"
        ]

    def sub_if(patterns, tag):
        nonlocal out
        if patterns:
            pat = "|".join(patterns)
            out = re.sub(rf"(?i)({pat})", f"<{tag}>", out)

    sub_if(name_patterns,  tags[0])
    sub_if(email_patterns, tags[1])
    sub_if(ssn_patterns,   tags[2])
    sub_if(phone_patterns, tags[3])
    sub_if(date_patterns,  tags[4])

    return out

# ================== METRICS (ONLY RELIABLE ONES) ==================
# SBERT cosine on raw vs sanitized
emb1 = bi_model.encode(text1, convert_to_tensor=True)
emb2 = bi_model.encode(text2, convert_to_tensor=True)
sbert_cos = util.cos_sim(emb1, emb2).item()

# BERTScore F1 on raw vs sanitized
P, R, F1 = bertscore([text1], [text2], lang="en", model_type="microsoft/deberta-base-mnli")
bert_f1 = float(F1[0])

ensemble_semantic = 0.5 * sbert_cos + 0.5 * bert_f1

# Non-PII drift path
text1_c = canonicalize_text(text1, PII, SAN_PLACEHOLDERS)
text2_c = canonicalize_text(text2, PII, SAN_PLACEHOLDERS)

emb1c = bi_model.encode(text1_c, convert_to_tensor=True)
emb2c = bi_model.encode(text2_c, convert_to_tensor=True)
sbert_cos_nonpii = util.cos_sim(emb1c, emb2c).item()

Pc, Rc, F1c = bertscore([text1_c], [text2_c], lang="en", model_type="microsoft/deberta-base-mnli")
bert_f1_nonpii = float(F1c[0])

ensemble_semantic_nonpii = 0.5 * sbert_cos_nonpii + 0.5 * bert_f1_nonpii

# Diagnostics
delta_len_chars = len(text2) - len(text1)
threshold = 0.70

# ================== PRINT ==================
print(f"SBERT cosine similarity (raw)       : {sbert_cos:.3f}")
print(f"BERTScore F1 (raw)                  : {bert_f1:.3f}")
print(f"Ensemble (raw, SBERT+BERTScore)     : {ensemble_semantic:.3f}")

print("\n--- Non-PII drift (canonicalized) ---")
print(f"SBERT cosine (non-PII)              : {sbert_cos_nonpii:.3f}")
print(f"BERTScore F1 (non-PII)              : {bert_f1_nonpii:.3f}")
print(f"Ensemble (non-PII, semantic)        : {ensemble_semantic_nonpii:.3f}")

print("\n--- Diagnostics ---")
print(f"Δ length (chars, sanitized - raw)   : {delta_len_chars:+d}")
print(f"\nHighly similar overall?             : {'YES' if ensemble_semantic >= threshold else 'NO'}")
print(f"Meaning preserved outside PII?      : {'YES' if ensemble_semantic_nonpii >= threshold else 'NO'}")


# ================== MANUAL PII EVAL INPUTS ==================
print("\n--- PII Evaluation ---")
print("Please enter counts based on your manual review.")
print("If something doesn't apply, enter 0.\n")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter an integer value.")

total_pii = get_int("Total # of actual PII items in the prompt (ground truth): ")
tp = get_int("PII items correctly identified & sanitized (true positives): ")
fn = get_int("PII items missed / not sanitized (false negatives): ")
fp = get_int("Non-PII items incorrectly sanitized (false positives): ")

# Consistency check for the ground-truth PII
if total_pii != tp + fn:
    print(
        f"\n[Warning] total_pii ({total_pii}) ≠ TP + FN ({tp + fn}). "
        "Please double-check your counts."
    )

# ================== DERIVED METRICS ==================
precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0   # PII recall / coverage
f1_pii    = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
miss_rate = fn / total_pii if total_pii > 0 else 0.0   # fraction of PII missed

print("\n--- PII Sanitization Metrics ---")
print(f"Precision (over sanitized items) : {precision:.3f}")
print(f"Recall    (over actual PII)      : {recall:.3f}")
print(f"F1 score (PII)                   : {f1_pii:.3f}")
print(f"Miss rate (PII not sanitized)    : {miss_rate:.3f}\n")



# ================== WRITE RELIABLE CSV ==================
row_lite = {
    "timestamp": datetime.now().isoformat(timespec="seconds"),
    "LLM": data["llm_used"],
    "sbert_cos": sbert_cos,
    "bert_f1": bert_f1,
    "ensemble_semantic": ensemble_semantic,
    "delta_len_chars": delta_len_chars,
    "precision": precision,
    "recall": recall,
    "f1_pii": f1_pii,
    "miss_rate": miss_rate
}

ensure_csv_exists(csv_reliable, list(row_lite.keys()))
append_to_csv(csv_reliable, row_lite)

print(f"\nSaved reliable scores to {csv_reliable}")
