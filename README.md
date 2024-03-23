# Slurp

Slurp is a command-line tool that allows you to fetch, list, rank, and summarize research papers from arXiv based on your interests. It provides functionality to rank research papers based on keywords and generate simplified summaries of paper abstracts using OpenAI or Anthropic APIs.

## Install

Create and activate a virtual env:
```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

Install:
```bash
pip3 install -e . 
```

## Setup

Run the setup command to configure your research interests and generate a `config.toml` file:

```slurp setup```

Enter your research interests and keywords when prompted, separated by commas.

Add interests according to arXiv category taxonomy e.g. `ro` for `robotics`, `cv` for `computer vision` etc.

Keywords can be any strings e.g. `llm`, `reinforcement learning` etc.

Open the generated `config.toml` file and add your OpenAI and/or Anthropic API keys.

## Usage

### Fetch Papers

To fetch papers based on your configured interests, run the following command:

```slurp up```

This will scrape arXiv for papers matching your interests and save them to a local db.

### List Papers

To list the fetched papers, use the `list` command:

```slurp list [--interest INTEREST] [--count COUNT]```

- `--interest`: Filter papers by a specific interest.
- `--count`: Specify the number of papers to list (default: 10). Use `all` to list all papers.

Example:

```slurp list --interest "ro" --count 3```

Output:

```code
Title: GaussianGrasper: 3D Language Gaussian Splatting for Open-vocabulary  Robotic Grasping
ID: 5d45f243-a568-45db-8a3f-8dddee4dfc7f
URL: https://arxiv.org/abs/2403.09637
PDF URL: https://arxiv.org/pdf/2403.09637

Title: Scalable Autonomous Drone Flight in the Forest with Visual-Inertial SLAM  and Dense Submaps Built without LiDAR
ID: 5c02ec89-742a-40b9-a86b-a751aeed2eea
URL: https://arxiv.org/abs/2403.09596
PDF URL: https://arxiv.org/pdf/2403.09596

Title: ExploRLLM: Guiding Exploration in Reinforcement Learning with Large  Language Models
ID: 7c650a0f-7b61-4f34-9594-901819133d39
URL: https://arxiv.org/abs/2403.09583
PDF URL: https://arxiv.org/pdf/2403.09583
```

### Rank Papers

To rank the fetched papers based on title and abstract relevance to `config.toml` keywords, use the `rank` command:

```slurp rank COUNT```

- `COUNT`: Specify the number of top papers to rank and display.

These rankings will be generated from analyzing **all** papers (e.g. machine learning, robotics, etc.) in the db.

Example:

```slurp rank 5```

Output:

```code
Here is the ranking of the paper titles and abstracts from most relevant to least relevant, based on the given keywords ['reinforcement', 'llm']:

1. Title: Larimar: Large Language Models with Episodic Memory Control
URL: https://arxiv.org/abs/2403.11901

2. Title: Supervised Fine-Tuning as Inverse Reinforcement Learning
URL: https://arxiv.org/abs/2403.12017

3. Title: Reinforcement Learning with Latent State Inference for Autonomous On-ramp Merging under Observation Delay
URL: https://arxiv.org/abs/2403.11852
```

### Generate Abstract Summary

To generate a simplified summary of a paper's abstract, as well as discover key words and terms useful for understanding the paper, use the `abstract` command:

```slurp abstract PAPER_URL --service SERVICE```

- `PAPER_URL`: The arXiv URL of the paper.
- `--service`: Select the service to use for generating the summary (`openai` or `anthropic`).

Example:

```slurp abstract https://arxiv.org/abs/2403.14626 --service anthropic```

Output:

```code
Key Terms and Ideas:
1. Synchronisation: The process of making multiple systems or agents work together in a coordinated manner.
2. Consensus methods: Techniques used to achieve agreement among multiple agents in a distributed system.
3. Peaking phenomenon: An undesirable transient behaviour where the system's output exhibits a large overshoot before settling to the desired value.

# ...more key terms and ideas

Key Takeaway:
This study proposes a synchronisation-oriented approach to adaptive control, 
which views model reference adaptation as a synchronisation problem between actual and virtual dynamic systems.
By designing a coupling input to achieve desired closed-loop error dynamics
and shaping the collective behaviour through input allocation,
the proposed approach enables a more systematic and generalised way
to design adaptive control systems with improved transient response characteristics
and mitigated peaking phenomenon.
```

### Download Paper

To download a paper's PDF based on its URL, use the `download` command:

```slurp download PAPER_URL [--path PATH]```

- `PAPER_URL`: The arXiv URL of the paper.
- `--path`: Specify the download path (default: current working directory).

Example:

```slurp download https://arxiv.org/abs/2403.14626 --path /PATH/TO/DIR/```

Output:

```Paper downloaded successfully: /PATH/TO/DIR/TITLE.pdf```

### TODO:
- [ ] Add option for `slurp up` to only fetch the `N` most recent papers
- [ ] Summarize entire paper
- [ ] Summarize page in a paper
- [ ] Use arXiv API so we don't get rate-limited or blocked
- [ ] Improve ranking - use embeddings
- [ ] Add paper overlap feature - use embeddings
- [ ] Do the meme, rewrite in Rust and make into a TUI