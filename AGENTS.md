# AGENTS.md

This repo is a personal study collection, not a single application. The git repo root
is this directory; each top-level folder is an independent course project (e.g.
`Hello-Agents`, `Claude-for-Work-Learn-to-Work-Faster-Smarter`, `Harness-Your-Way`,
`All-In-Rag`, `DeepLearningAI`, ...). Do not assume code or config is shared between folders.
The root `Readme.md` is a coarse course index, not a project spec.

## Workflow conventions
- The recurring pattern: follow a course, then maintain that course's lesson notes in the
  folder's `Readme.md` (course outlines and notes are written in Chinese and/or English),
  then commit that single file per lesson on `main` with the lesson title as the message
  (e.g. `40. Skill Marketplaces`, `1.1 从提示词工程到 Graph 工程`). Match this style.
- `Harness-Your-Way/` is the currently active course (SDD / OpenCode). It is sparse:
  a `Readme.md` plus image assets.

## Python
- Multiple Python virtualenvs exist in the tree; never assume one is active or sufficient.
  Activate the venv for the folder you work in before running scripts, e.g.
  `source .venv/bin/activate` then `python my_main.py`.
- Version gotcha: `Hello-Agents/.venv312` (= Python 3.12.12 from Homebrew) is the one the
  course requires for `pip install spacy`; the other local venvs differ (root `.venv` is
  3.12.12, `Hello-Agents/.venv` is 3.14.0).
- `Hello-Agents/` is the biggest project: lots of runnable scripts (`my_*.py`,
  `chapter07_basic_setup.py`, `test_8_memory.py`, etc.) plus Jupyter notebooks.

## Secrets
- `.env` (gitignored) holds API keys; `Hello-Agents/env.template` documents every supported
  provider (OpenAI, AWS Bedrock, DeepSeek, Qwen/DashScope, ModelScope, Kimi, GLM, Ollama,
  vLLM). Scripts generally read `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL_ID`.
  Never print, log, or commit these.

## Hello-Agents framework (`pkg/` is gitignored)
- Course code imports `hello_agents`, which is NOT installed from PyPI. It is an editable
  install cloned from upstream and pinned to a tag, living under `Hello-Agents/pkg/`:
  - `cd pkg && git clone https://github.com/jjyaoao/HelloAgents.git HelloAgents-0.27`
  - `git checkout V0.2.7`
  - `pip install -e pkg/HelloAgents-0.27`
- Replicate this when recreating a fresh environment; do not expect `pip install hello-agents`
  to work.