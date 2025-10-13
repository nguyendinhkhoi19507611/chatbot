"""
Hybrid Career Recommender

Combines three signals:
1) Zero-shot classification over career labels (multilingual)
2) Sentence embedding similarity to career descriptions
3) Classic TF-IDF + RandomForest (existing) when available

Output is a weighted ensemble for robust results with small data.
"""

from __future__ import annotations

import os
import json
from typing import List, Dict, Any

import numpy as np

# Lazy import heavy deps
_hf_loaded = False
_zshot = None
_embedder = None


def _lazy_load_models():
    global _hf_loaded, _zshot, _embedder
    if _hf_loaded:
        return
    try:
        from transformers import pipeline
        from sentence_transformers import SentenceTransformer
        # Multilingual zero-shot (supports Vietnamese)
        _zshot = pipeline(
            "zero-shot-classification",
            model="joeddav/xlm-roberta-large-xnli"
        )
        # Multilingual sentence embeddings
        _embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        _hf_loaded = True
    except Exception as e:
        print(f"⚠ Warning: Failed to load HF models: {e}")
        _hf_loaded = False


class HybridCareerRecommender:
    def __init__(self, career_data_path: str = None, classic_model=None):
        # Load career data
        if career_data_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            career_data_path = os.path.join(os.path.dirname(current_dir), 'data', 'career_data.json')
        with open(career_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.careers = data['careers']
        self.labels = [c['name'] for c in self.careers]
        # Precompute embedding corpus for careers
        self._career_embeddings = None
        self._ensure_embeddings()
        # Optional classic model (TF-IDF + RF)
        self.classic_model = classic_model

    def _ensure_embeddings(self):
        _lazy_load_models()
        if _embedder is None:
            return
        if self._career_embeddings is None:
            texts = [c['description'] + ' ' + ' '.join(c['interests']) for c in self.careers]
            self._career_embeddings = _embedder.encode(texts, normalize_embeddings=True)

    def _zero_shot_scores(self, query: str) -> np.ndarray:
        _lazy_load_models()
        if _zshot is None:
            return np.zeros(len(self.careers), dtype=float)
        try:
            res = _zshot(query, candidate_labels=self.labels, hypothesis_template="Đây là về nghề nghiệp {}.")
            # Map scores back to career order
            label_to_score = {lbl: score for lbl, score in zip(res['labels'], res['scores'])}
            return np.array([label_to_score.get(c['name'], 0.0) for c in self.careers], dtype=float)
        except Exception as e:
            print(f"Zero-shot failed: {e}")
            return np.zeros(len(self.careers), dtype=float)

    def _embedding_scores(self, query: str) -> np.ndarray:
        _lazy_load_models()
        if _embedder is None or self._career_embeddings is None:
            return np.zeros(len(self.careers), dtype=float)
        try:
            q = _embedder.encode([query], normalize_embeddings=True)
            sims = (q @ self._career_embeddings.T)[0]
            # Normalize to [0,1]
            sims = (sims - sims.min()) / (sims.max() - sims.min() + 1e-9)
            return sims
        except Exception as e:
            print(f"Embedding scoring failed: {e}")
            return np.zeros(len(self.careers), dtype=float)

    def _classic_scores(self, query: str) -> np.ndarray:
        if not self.classic_model:
            return np.zeros(len(self.careers), dtype=float)
        try:
            recs = self.classic_model.predict(query, top_n=len(self.careers))
            score_map = {r['career_id']: r['confidence'] for r in recs}
            # Convert to vector in career order
            vec = np.array([score_map.get(c['id'], 0.0) for c in self.careers], dtype=float)
            # Normalize
            if vec.max() > 0:
                vec = vec / vec.max()
            return vec
        except Exception as e:
            print(f"Classic model scoring failed: {e}")
            return np.zeros(len(self.careers), dtype=float)

    def recommend(self, query: str, top_n: int = 5, weights: Dict[str, float] | None = None) -> List[Dict[str, Any]]:
        if weights is None:
            # Prioritize semantic + zero-shot; classic as supporting
            weights = {"zero_shot": 0.45, "embedding": 0.45, "classic": 0.10}
        zs = self._zero_shot_scores(query)
        em = self._embedding_scores(query)
        cl = self._classic_scores(query)
        # Weighted ensemble
        scores = weights["zero_shot"] * zs + weights["embedding"] * em + weights["classic"] * cl
        top_idx = np.argsort(scores)[-top_n:][::-1]
        out = []
        for i in top_idx:
            c = self.careers[i]
            out.append({
                'career_id': c['id'],
                'career_name': c['name'],
                'description': c['description'],
                'confidence': float(scores[i]),
                'interests': c.get('interests', []),
                'skills': c.get('skills', []),
                'salary_range': c.get('salary_range'),
                'education': c.get('education')
            })
        return out


