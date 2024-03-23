from db import get_n_papers


def display_ranked_papers(ranked_papers):
    for keyword, papers in ranked_papers.items():
        print(f"Keyword: {keyword}")
        print("-" * 50)
        for i, paper in enumerate(papers, start=1):
            print(f"Top {i}")
            print(f"Title: {paper['title']}")
            print(f"URL: {paper['url']}")
            print(f"PDF URL: {paper['pdf_url']}")
            print(f"Interest: {paper['interest']}")
            print()
        print()


def list_papers(interest=None, count="10"):
    papers = get_n_papers(interest, count)

    if not papers:
        print("No papers found.")
    else:
        for paper in papers:
            print(f"Title: {paper['title']}")
            print(f"URL: {paper['url']}")
            print(f"PDF URL: {paper['pdf_url']}")
            print(f"Interest: {paper['interest']}")
            print()
