import requests
from bs4 import BeautifulSoup


def scrape_arxiv(interests):
    """
    Scrape based on interests
    """

    interest_urls = {
        "cv": "https://arxiv.org/list/cs.CV/recent",
        "ml": "https://arxiv.org/list/cs.LG/recent",
        "ai": "https://arxiv.org/list/cs.AI/recent",
        "ro": "https://arxiv.org/list/cs.RO/recent",
        "cl": "https://arxiv.org/list/cs.CL/recent",
        "dc": "https://arxiv.org/list/cs.DC/recent",
        "et": "https://arxiv.org/list/cs.ET/recent",
        "ir": "https://arxiv.org/list/cs.IR/recent",
        "pl": "https://arxiv.org/list/cs.PL/recent",
    }

    papers = []

    for interest in interests:
        if interest.lower() in interest_urls:
            url = interest_urls[interest.lower()]
            print(f"scraping for {interest}: {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            dt_elements = soup.find_all("dt")
            dd_elements = soup.find_all("dd")

            for dt, dd in zip(dt_elements, dd_elements):
                abs_link = dt.find("a", {"href": lambda x: x and x.startswith("/abs")})
                if abs_link:
                    abs_url = "https://arxiv.org" + abs_link["href"]
                    abs_response = requests.get(abs_url)
                    abs_soup = BeautifulSoup(abs_response.content, "html.parser")
                    abstract = abs_soup.find(
                        "blockquote", class_="abstract"
                    ).text.strip()
                    abstract = abstract.replace("Abstract:", "").strip()
                    pdf_url = (
                        "https://arxiv.org"
                        + abs_soup.find("a", class_="abs-button", text="Download PDF")[
                            "href"
                        ]
                    )
                    paper = {
                        "title": dd.find("div", class_="list-title")
                        .text.replace("Title:", "")
                        .strip(),
                        "authors": dd.find("div", class_="list-authors")
                        .text.replace("Authors:", "")
                        .strip(),
                        "abstract": abstract,
                        "url": abs_url,
                        "pdf_url": pdf_url,
                        "interest": interest,
                    }
                    papers.append(paper)
                else:
                    print("Abstract URL not found for paper")
        else:
            print(f"no matching url found for interest: {interest}")

    return papers
