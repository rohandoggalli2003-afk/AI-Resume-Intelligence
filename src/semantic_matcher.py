from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def calculate_similarity(resume_text, job_description):

    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True
    )

    job_embedding = model.encode(
        [job_description],
        normalize_embeddings=True
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    # Convert cosine similarity into a
    # 0–100 compatibility score.
    score = ((float(similarity) + 1) / 2) * 100

    score = max(
        0,
        min(score, 100)
    )

    return round(score, 2)