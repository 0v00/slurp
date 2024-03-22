import argparse
import toml
import os
from scraper import scrape_arxiv, scrape_paper
from db import init_db, save_papers, save_paper, get_paper_by_url, get_all_papers
from display import list_papers
from download import download_paper, download_ranked_papers
from summary import generate_summary, rank_papers


def setup_cmd(args):
    """
    Set up the CLI with interests and generate a config.toml file
    """
    interests = input("Enter your research interests (comma-separated): ")
    interest_list = [interest.strip() for interest in interests.split(",")]
    interest_list = [interest for interest in interest_list if interest]

    keywords = input("Enter important keywords for research papers (comma-separated): ")
    keyword_list = [keyword.strip() for keyword in keywords.split(",")]
    keyword_list = [keyword for keyword in keyword_list if keyword]

    config = {
        "openai_api_key": "",
        "anthropic_api_key": "",
        "interests": interest_list,
        "keywords": keyword_list,
    }

    with open("config.toml", "w") as file:
        toml.dump(config, file)
    print("Config saved to config.toml. Add your API keys to the config file.")


def up_cmd(args):
    """
    Fetch papers
    """

    if not os.path.exists("config.toml"):
        print("Config file not found. Run 'slurp setup' first.")
        return

    with open("config.toml", "r") as file:
        config = toml.load(file)

    interests = config["interests"]
    init_db()
    papers = scrape_arxiv(interests)
    save_papers(papers)


def list_cmd(args):
    """
    List papers in the terminal
    """

    if not os.path.exists("papers.db"):
        print("Database not found.")
        return

    interest = args.interest
    count = args.count

    list_papers(interest, count)


def abstract_cmd(args):
    """
    Generate a simplified summary, including key terms and concepts
    of a paper's abstract using OpenAI or Anthropic
    """
    if not os.path.exists("papers.db"):
        print("Database not found. Run 'slurp up' first to fetch papers.")
        return

    paper_url = args.paper_url
    service = args.service

    if not os.path.exists("config.toml"):
        print("Config file not found. Run 'slurp setup' first.")
        return

    with open("config.toml", "r") as file:
        config = toml.load(file)

    if service == "openai":
        api_key = config["openai_api_key"]
    elif service == "anthropic":
        api_key = config["anthropic_api_key"]
    else:
        print("Invalid service selected. Please choose 'openai' or 'anthropic'.")
        return

    if not api_key:
        print(f"API key for {service} not found in config.toml.")
        return

    paper = get_paper_by_url(paper_url)
    if not paper:
        paper = scrape_paper(paper_url)
        save_paper(paper)

    abstract = paper["abstract"]
    summary = generate_summary(abstract, service, api_key)
    print(summary)


def rank_cmd(args):
    """
    Rank papers based on keywords
    """
    if not os.path.exists("papers.db"):
        print("Database not found. Run 'slurp up' first to fetch papers.")
        return

    if not os.path.exists("config.toml"):
        print("Config file not found. Run 'slurp setup' first.")
        return

    with open("config.toml", "r") as file:
        config = toml.load(file)

    keywords = config["keywords"]
    service = args.service
    count = args.count
    download = args.download

    if service == "openai":
        api_key = config["openai_api_key"]
    elif service == "anthropic":
        api_key = config["anthropic_api_key"]
    else:
        print("Invalid service selected. Please choose either 'openai' or 'anthropic'.")
        return

    if not api_key:
        print(f"API key for {service} not found in config.toml.")
        return

    papers = get_all_papers()
    response = rank_papers(papers, keywords, service, api_key, count)
    print(response)
    if download:
        download_path = args.path or os.getcwd()
        download_ranked_papers(response, papers, download_path)


def download_cmd(args):
    """
    Download a paper's PDF based on its UUID
    """
    if not os.path.exists("papers.db"):
        print("Database not found. Run 'slurp up' first to fetch papers.")
        return

    paper_url = args.paper_url
    download_path = args.path or os.getcwd()

    paper = get_paper_by_url(paper_url)
    if not paper:
        paper = scrape_paper(paper_url)
        save_paper(paper)

    download_paper(paper, download_path)


def main():
    parser = argparse.ArgumentParser(description="Slurp")
    subparsers = parser.add_subparsers(dest="command")

    setup_parser = subparsers.add_parser(
        "setup", help="Add interests and generate config file"
    )
    setup_parser.set_defaults(func=setup_cmd)

    up_parser = subparsers.add_parser("up", help="Fetch papers")
    up_parser.set_defaults(func=up_cmd)

    list_parser = subparsers.add_parser("list", help="List papers from the database.")
    list_parser.add_argument("--interest", help="Filter papers by interest.")
    list_parser.add_argument(
        "--count",
        default="10",
        help="Number of papers to list (default: 10, use 'all' for all papers).",
    )
    list_parser.set_defaults(func=list_cmd)

    paper_parser = subparsers.add_parser(
        "abstract", help="Generate a simplified summary of a paper's abstract"
    )
    paper_parser.add_argument("paper_url", help="URL of the paper")
    paper_parser.add_argument(
        "--service",
        choices=["openai", "anthropic"],
        required=True,
        help="Select a service",
    )
    paper_parser.set_defaults(func=abstract_cmd)

    download_parser = subparsers.add_parser(
        "download", help="Download a paper's PDF based on its UUID"
    )
    download_parser.add_argument("paper_url", help="URL of the paper")
    download_parser.add_argument(
        "--path", help="Download path (default: current working directory)"
    )
    download_parser.set_defaults(func=download_cmd)

    rank_parser = subparsers.add_parser(
        "rank", help="Rank papers based on keywords using OpenAI or Anthropic"
    )
    rank_parser.add_argument(
        "count", type=int, help="Number of top papers to rank and display"
    )
    rank_parser.add_argument(
        "--service",
        choices=["openai", "anthropic"],
        required=True,
        help="Select a service",
    )
    rank_parser.add_argument(
        "--download",
        action="store_true",
        help="Download the ranked papers (default: False)",
    )
    rank_parser.add_argument(
        "--path",
        help="Download path for ranked papers (default: current working directory)",
    )
    rank_parser.set_defaults(func=rank_cmd)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
