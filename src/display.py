import sqlite3


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
