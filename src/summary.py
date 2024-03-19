from openai import OpenAI
from anthropic import Anthropic


def generate_summary(abstract, service, api_key):
    if service == "openai":
        client = OpenAI(api_key=api_key)
        prompt = f"Please provide a simplified summary of the following abstract, highlighting key terms and ideas unique to artificial intelligence, computer vision, or machine learning that may require further research to better understand the paper. Also, include a key takeaway from the abstract.\n\nAbstract:\n{abstract}"
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and knowledgeable AI and robotics researcher.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        summary = completion.choices[0].message.content
    elif service == "anthropic":
        client = Anthropic(api_key=api_key)
        prompt = f"Please provide a simplified summary of the following abstract, highlighting key terms and ideas unique to artificial intelligence, computer vision, or machine learning that may require further research to better understand the paper. Also, include a key takeaway from the abstract.\n\nAbstract:\n{abstract}"
        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
            model="claude-3-opus-20240229",
        )
        summary = message.content[0].text
    else:
        summary = "Invalid service selected."

    return summary


def rank_papers(papers, keywords, service, api_key, count):
    if service == "openai":
        client = OpenAI(api_key=api_key)
        prompt = f"Given the following keywords: {keywords}, rank the relevance of these paper titles and abstracts from most relevant to least relevant. Provide the ranking as a numbered list, including the paper title, ID, and URL for each ranked paper. Return only the top {count} papers in the ranking.\n\n"
        for paper in papers:
            prompt += f"Title: {paper['title']}\nID: {paper['id']}\nURL: {paper['url']}\nAbstract: {paper['abstract']}\n\n"
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and knowledgeable AI and robotics researcher.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        response = completion.choices[0].message.content
    elif service == "anthropic":
        client = Anthropic(api_key=api_key)
        prompt = f"Given the following keywords: {keywords}, rank the relevance of these paper titles and abstracts from most relevant to least relevant. Provide the ranking as a numbered list, including the paper title, ID, and URL for each ranked paper. Return only the top {count} papers in the ranking.\n\n"
        for paper in papers:
            prompt += f"Title: {paper['title']}\nID: {paper['id']}\nURL: {paper['url']}\nAbstract: {paper['abstract']}\n\n"
        message = client.messages.create(
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
            model="claude-3-opus-20240229",
        )
        response = message.content[0].text
    else:
        response = "Invalid service selected."

    return response
