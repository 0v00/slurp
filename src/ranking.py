from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def rank_papers_cosine(papers, keywords, count):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    paper_titles = [paper["title"] for paper in papers]
    paper_embeddings = model.encode(paper_titles)

    ranked_papers = {}
    for keyword in keywords:
        keyword_embedding = model.encode([keyword])
        similarities = cosine_similarity(keyword_embedding, paper_embeddings)
        top_indices = similarities.argsort()[0][-count:][::-1]

        keyword_ranked_papers = []
        for index in top_indices:
            paper = papers[index]
            keyword_ranked_papers.append(
                {
                    "title": paper["title"],
                    "id": paper["id"],
                    "url": paper["url"],
                    "pdf_url": paper["pdf_url"],
                    "interest": paper["interest"],
                }
            )

        ranked_papers[keyword] = keyword_ranked_papers

    return ranked_papers
