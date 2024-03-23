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
