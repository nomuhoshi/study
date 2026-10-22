import json, sys
import spacy
from wordfreq import zipf_frequency

nlp = spacy.load("en_core_web_sm")
CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV"}
AUX = {"be", "have", "do", "will", "would", "can", "could", "shall", "should", "may", "might", "must"}


def band(lemma):
    z = zipf_frequency(lemma, "en")
    return "high" if z >= 4.5 else ("mid" if z >= 3.5 else "low")


def analyze(text, unknown, polysemy):
    doc = nlp(text)
    toks = []
    for t in doc:
        if t.is_punct or t.is_space or t.like_num or t.pos_ not in CONTENT_POS:
            continue
        lem = t.lemma_.lower()
        if lem in AUX:
            continue
        toks.append(lem)
    def label(l):
        return "unknown" if l in unknown else ("polysemy" if l in polysemy else "known")
    total = len(toks)
    tok_unknown = sum(label(l) == "unknown" for l in toks)
    tok_poly = sum(label(l) == "polysemy" for l in toks)
    types = sorted(set(toks))
    bands = {}
    for b in ("high", "mid", "low"):
        ts = [l for l in types if band(l) == b]
        known = [l for l in ts if label(l) == "known"]
        bands[b] = {"types": len(ts), "known": len(known),
                    "rate": round(len(known) / len(ts), 3) if ts else None}
    return {
        "content_tokens": total,
        "unknown_tokens": tok_unknown,
        "polysemy_tokens": tok_poly,
        "unknown_rate": round(tok_unknown / total, 3),
        "unclear_rate": round((tok_unknown + tok_poly) / total, 3),
        "content_types": len(types),
        "unknown_types": sum(label(l) == "unknown" for l in types),
        "polysemy_types": sum(label(l) == "polysemy" for l in types),
        "band_known_rate": bands,
        "lemmas": {l: [label(l), band(l)] for l in types},
    }


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    print(json.dumps(analyze(cfg["text"], set(cfg["unknown"]), set(cfg["polysemy"])),
                     ensure_ascii=False, indent=1))
