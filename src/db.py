import sqlite3
import uuid
from datetime import datetime


def init_db():
    conn = sqlite3.connect("papers.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS papers
              (id TEXT PRIMARY KEY,
              title TEXT,
              authors TEXT,
              abstract TEXT,
              url TEXT,
              pdf_url TEXT,
              interest TEXT,
              scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    conn.commit()
    conn.close()


def save_papers(papers):
    conn = sqlite3.connect("papers.db")
    c = conn.cursor()

    for paper in papers:
        c.execute("SELECT COUNT(*) FROM papers WHERE title = ?", (paper["title"],))
        count = c.fetchone()[0]

        if count == 0:
            paper_id = str(uuid.uuid4())
            scraped_at = datetime.now()
            c.execute(
                "INSERT INTO papers (id, title, authors, abstract, url, pdf_url, interest, scraped_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    paper_id,
                    paper["title"],
                    paper["authors"],
                    paper["abstract"],
                    paper["url"],
                    paper["pdf_url"],
                    paper["interest"],
                    scraped_at,
                ),
            )
        else:
            print(f"Skipped duplicate paper: {paper['title']}")

    conn.commit()
    conn.close()


def save_paper(paper):
    conn = sqlite3.connect("papers.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM papers WHERE title = ?", (paper["title"],))
    count = c.fetchone()[0]

    if count == 0:
        paper_id = str(uuid.uuid4())
        scraped_at = datetime.now()
        c.execute(
            "INSERT INTO papers (id, title, authors, abstract, url, pdf_url, interest, scraped_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                paper_id,
                paper["title"],
                paper["authors"],
                paper["abstract"],
                paper["url"],
                paper["pdf_url"],
                None,
                scraped_at,
            ),
        )
        conn.commit()
    else:
        print(f"Paper with title '{paper['title']}' already exists. Skipping.")

    conn.close()


def get_paper_by_id(paper_id):
    conn = sqlite3.connect("papers.db")
    c = conn.cursor()

    c.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
    paper = c.fetchone()

    conn.close()
    return paper


def get_all_papers():
    conn = sqlite3.connect("papers.db")
    c = conn.cursor()

    c.execute("SELECT * FROM papers")
    papers = c.fetchall()

    conn.close()

    paper_dicts = []
    for paper in papers:
        paper_dict = {
            "id": paper[0],
            "title": paper[1],
            "authors": paper[2],
            "abstract": paper[3],
            "url": paper[4],
            "pdf_url": paper[5],
            "interest": paper[6],
            "scraped_at": paper[7],
        }
        paper_dicts.append(paper_dict)

    return paper_dicts


def get_paper_by_url(url):
    conn = sqlite3.connect("papers.db")
    c = conn.cursor()

    c.execute("SELECT * FROM papers WHERE url = ?", (url,))
    paper = c.fetchone()

    conn.close()

    if paper:
        paper_dict = {
            "id": paper[0],
            "title": paper[1],
            "authors": paper[2],
            "abstract": paper[3],
            "url": paper[4],
            "pdf_url": paper[5],
            "interest": paper[6],
            "scraped_at": paper[7],
        }
        return paper_dict
    else:
        return None
