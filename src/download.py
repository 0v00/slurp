import os
import requests


def download_paper(paper, download_path):
    pdf_url = paper["pdf_url"]
    response = requests.get(pdf_url)
    if response.status_code == 200:
        filename = f"{paper['title']}.pdf"
        file_path = os.path.join(download_path, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Paper downloaded successfully: {file_path}")
    else:
        print("Failed to download the paper.")


def download_ranked_papers(response, papers, download_path):
    for line in response.strip().split("\n"):
        if "ID:" in line:
            paper_id = line.split("ID:")[1].strip()
            paper = next((p for p in papers if p["id"] == paper_id), None)
            if paper:
                pdf_url = paper["pdf_url"]
                response = requests.get(pdf_url)
                if response.status_code == 200:
                    filename = f"{paper_id}.pdf"
                    file_path = os.path.join(download_path, filename)
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    print(f"Paper downloaded successfully: {file_path}")
                else:
                    print(f"Failed to download the paper with ID {paper_id}.")
