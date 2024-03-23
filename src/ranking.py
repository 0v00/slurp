from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


def rank_papers_cosine(papers, keywords, count):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    keyword_embeddings = model.encode(keywords)
    paper_titles = [paper["title"] for paper in papers]
    paper_embeddings = model.encode(paper_titles)

    similarities = cosine_similarity(keyword_embeddings, paper_embeddings)
    top_indices = similarities.argsort()[0][-count:][::-1]

    ranked_papers = []
    for index in top_indices:
        paper = papers[index]
        ranked_papers.append(
            {
                "title": paper["title"],
                "id": paper["id"],
                "url": paper["url"],
                "pdf_url": paper["pdf_url"],
                "interest": paper["interest"],
            }
        )

    return ranked_papers


def rank_papers_knn(papers, keywords, count):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    keyword_embeddings = model.encode(keywords)
    paper_titles = [paper["title"] for paper in papers]
    paper_embeddings = model.encode(paper_titles)

    nn_model = NearestNeighbors(n_neighbors=count, metric="euclidean")
    nn_model.fit(paper_embeddings)

    distances, indices = nn_model.kneighbors(keyword_embeddings)

    ranked_papers = []
    for i in range(count):
        index = indices[0][i]
        distance = distances[0][i]
        paper = papers[index]
        ranked_papers.append(
            {
                "title": paper["title"],
                "id": paper["id"],
                "url": paper["url"],
                "pdf_url": paper["pdf_url"],
                "interest": paper["interest"],
                "distance": distance,
            }
        )

    return ranked_papers
