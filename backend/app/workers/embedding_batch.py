"""Batch embedding generation for rows missing embeddings."""


async def generate_embeddings_batch(limit: int = 200):
    # 1) fetch flight_offers where embedding is null
    # 2) build semantic text from normalized columns
    # 3) call embedding model
    # 4) update pgvector column
    return limit
