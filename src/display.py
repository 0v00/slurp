import sqlite3


# def display_ranked_papers(ranked_papers):
#     for i, paper in enumerate(ranked_papers, start=1):
#         print(f"Rank: {i}")
#         print(f"Title: {paper['title']}")
#         print(f"URL: {paper['url']}")
#         print(f"PDF URL: {paper['pdf_url']}")
#         print(f"Interest: {paper['interest']}")
#         print("---")


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
    conn = sqlite3.connect("papers.db")
    c = conn.cursor()

    if interest:
        if count == "all":
            c.execute(
                "SELECT id, title, authors, url, pdf_url, interest, scraped_at FROM papers WHERE interest = ?",
                (interest,),
            )
        else:
            c.execute(
                "SELECT id, title, authors, url, pdf_url, interest, scraped_at FROM papers WHERE interest = ? LIMIT ?",
                (interest, int(count)),
            )
    else:
        if count == "all":
            c.execute(
                "SELECT id, title, authors, url, pdf_url, interest, scraped_at FROM papers"
            )
        else:
            c.execute(
                "SELECT id, title, authors, url, pdf_url, interest, scraped_at FROM papers LIMIT ?",
                (int(count),),
            )

    papers = c.fetchall()
    conn.close()

    if not papers:
        print("No papers found.")
    else:
        for paper in papers:
            print(f"Title: {paper[1]}")
            print(f"URL: {paper[3]}")
            print(f"PDF URL: {paper[4]}")
            print()
