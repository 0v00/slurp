# Slurp

Slurp is a command-line tool that allows you to fetch, list, rank, and summarize research papers from arXiv based on your interests. It provides functionality to rank research papers based on keywords, and generate simplified summaries of paper abstracts using OpenAI or Anthropic APIs.

## Install

1. Create and activate a virtual env:
```bash
python -m venv myvenv
source myvenv/bin/activate
```

2. Install:
```bash
pip install git+https://github.com/0v00/slurp.git
```

3. Alternatively, for developing:
```bash
git clone https://github.com/0v00/slurp.git
cd slurp
pip install -e .
```

## Setup

Run the setup command to configure your research interests and generate a `config.toml` file:

```slurp setup```

Enter your research interests and keywords when prompted, separated by commas.

Add interests according to arXiv category taxonomy e.g. `ro` for `robotics`, `cv` for `computer vision` etc.

Keywords can be any strings e.g. `llm`, `reinforcement learning` etc.

Open the generated `config.toml` file and add your OpenAI and/or Anthropic API keys.

## Usage

### Scrape Papers

To scrape info from papers based on your configured interests, run the following command:

```slurp up```

This will scrape arXiv for papers matching your interests and save them to a local db.

### List Papers

To list the scraped papers, use the `list` command:

```slurp list [--interest INTEREST] [--count COUNT]```

- `--interest`: Filter papers by a specific interest. Uses arXiv category taxonomy.
- `--count`: Specify the number of papers to list (default: 10). Use `all` to list all papers.

Example:

```slurp list --interest "ro" --count 3```

Output:

```code
Title: GaussianGrasper: 3D Language Gaussian Splatting for Open-vocabulary  Robotic Grasping
URL: https://arxiv.org/abs/2403.09637
PDF URL: https://arxiv.org/pdf/2403.09637

Title: Scalable Autonomous Drone Flight in the Forest with Visual-Inertial SLAM  and Dense Submaps Built without LiDAR
URL: https://arxiv.org/abs/2403.09596
PDF URL: https://arxiv.org/pdf/2403.09596

Title: ExploRLLM: Guiding Exploration in Reinforcement Learning with Large  Language Models
URL: https://arxiv.org/abs/2403.09583
PDF URL: https://arxiv.org/pdf/2403.09583
```

### Rank Papers

To rank the scraped papers based on title and abstract similarity to `config.toml` keywords, use the `rank` command:

```slurp rank COUNT```

- `COUNT`: Specify the number of top papers to rank and display.

These rankings will be generated from analyzing **all** papers (e.g. machine learning, robotics, etc.) in the db. This uses `all-MiniLM-L6-v2` and `util.cos_sim`. It might take awhile for this command to run for the first time as it will download the model.

Example:

```slurp rank 3```

Output:

```code
Keyword: reinforcement
--------------------------------------------------
Top 1
Title: Rethinking Adversarial Inverse Reinforcement Learning: From the Angles  of Policy Imitation and Transferable Reward Recovery
URL: https://arxiv.org/abs/2403.14593
PDF URL: https://arxiv.org/pdf/2403.14593
Interest: ml

Top 2
Title: Physics-Based Causal Reasoning for Safe & Robust Next-Best Action  Selection in Robot Manipulation Tasks
URL: https://arxiv.org/abs/2403.14488
PDF URL: https://arxiv.org/pdf/2403.14488
Interest: ro

Top 3
Title: Tell Me What You Want (What You Really, Really Want): Addressing the  Expectation Gap for Goal Conveyance from Humans to Robots
URL: https://arxiv.org/abs/2403.14344
PDF URL: https://arxiv.org/pdf/2403.14344
Interest: ro
```

### Generate Abstract Summary

To generate a simplified summary of a paper's abstract, as well as discover key words and terms useful for understanding the paper, use the `abstract` command:

```slurp abstract PAPER_URL --service SERVICE```

- `PAPER_URL`: The arXiv URL of the paper.
- `--service`: Select the service to use for generating the summary (`openai` or `anthropic`).

If you use an arXiv URL that is not yet in the DB, it will be scraped and added before generating a summary.

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
- [ ] Add paper overlap feature - use embeddings
- [ ] Do the meme, rewrite in Rust and make into a TUI