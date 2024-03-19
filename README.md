# Slurp CLI Tool

Slurp is a command-line tool that allows you to fetch, list, rank, and summarize research papers from arXiv based on your interests. It provides functionality to rank research papers based on keywords and generate simplified summaries of paper abstracts using OpenAI or Anthropic APIs.

## Install

1. Create and activate a virtual env
- `python3 -m venv myvenv`
- `source myvenv/bin/activate`

2. Install
- `pip install -e .`

## Setup

Run the setup command to configure your research interests and generate a `config.toml` file:

```slurp setup```

Enter your research interests and keywords when prompted, separated by commas.

Interests follow arXiv category taxonomy e.g. `ro` for `robotics`, `cv` for `computer vision` etc.

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

```slurp rank COUNT --service SERVICE [--download] [--path PATH]```

- `COUNT`: Specify the number of top papers to rank and display.
- `--service`: Select the service to use for ranking (required). Choose between `openai` and `anthropic`.
- `--download`: Download the ranked papers (optional).
- `--path`: Specify the download path for ranked papers (optional, default: current working directory).

These rankings will be generated from analyzing **all** papers (e.g. machine learning, robotics, etc.) in the db.

Example:

```slurp rank 5 --service anthropic --download --path /path/to/download```

Output:

```code
Here is the ranking of the paper titles and abstracts from most relevant to least relevant, based on the given keywords ['reinforcement', 'llm']:

1. Title: Larimar: Large Language Models with Episodic Memory Control
ID: 1736f9d2-3f6c-43be-8085-c6b78ef5d6b1
URL: https://arxiv.org/abs/2403.11901

2. Title: Supervised Fine-Tuning as Inverse Reinforcement Learning
ID: 3fd784f5-5aac-44cc-98e6-ac419672a875
URL: https://arxiv.org/abs/2403.12017

3. Title: Reinforcement Learning with Latent State Inference for Autonomous On-ramp Merging under Observation Delay
ID: c6d4f799-1c9b-450b-857b-a861a8405e5b
URL: https://arxiv.org/abs/2403.11852

Paper downloaded successfully: /PATH/TO/DIR/1736f9d2-3f6c-43be-8085-c6b78ef5d6b1.pdf
Paper downloaded successfully: /PATH/TO/DIR/3fd784f5-5aac-44cc-98e6-ac419672a875.pdf
Paper downloaded successfully: /PATH/TO/DIR/c6d4f799-1c9b-450b-857b-a861a8405e5b.pdf
```

### Generate Abstract Summary

To generate a simplified summary of a paper's abstract, as well as discover key words and terms useful for understanding the paper, use the `abstract` command:

```slurp abstract PAPER_ID --service SERVICE```

- `PAPER_ID`: The UUID of the paper.
- `--service`: Select the service to use for generating the summary (`openai` or `anthropic`).

Example:

```slurp abstract 34d50a36-21de-4395-8d5e-b2566b46daee --service anthropic```

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

To download a paper's PDF based on its UUID, use the `download` command:

```slurp download PAPER_ID [--path PATH]```

- `PAPER_ID`: The UUID of the paper.
- `--path`: Specify the download path (default: current working directory).

Example:

```slurp download 34d50a36-21de-4395-8d5e-b2566b46daee --path /PATH/TO/DIR/```

Output:

```Paper downloaded successfully: /PATH/TO/DIR/34d50a36-21de-4395-8d5e-b2566b46daee.pdf```

### TODO:
- [ ] Summarize entire paper
- [ ] Summarize page in a paper
- [ ] `PAPER_ID` is too long, pick another option or change how `abstract` and `download` subcommands work
- [ ] Use arXiv API so we don't get rate-limited or blocked
- [ ] Do the meme, rewrite in Rust and make a TUI