# STAT 386: Answering questions with advanced pandas

This Quarto website continues the pandas foundations lesson. Students begin by
decoding a familiar pandas pipeline and writing a new one, then learn grouped
summaries, group-relative comparisons, date components, and pandas plotting.

The main reasoning check is: **What does one row represent before and after this
operation?**

## Contents

- `slides/pandas-questions.qmd`: 44-slide RevealJS deck, including the title,
  with speaker notes and immediate debriefs.
- `slides/theme.scss`: the same visual theme as pandas foundations.
- `slides/figures/`: five plots generated from the bundled data.
- `slides/outputs/`: computed tables and values included directly in the deck.
- `activity/pandas-questions.qmd` and `.ipynb`: student activities.
- `activity/pandas-questions-complete.qmd` and `.ipynb`: completed activities.
- `data/talks.csv`: the same 794-talk, 14-column dataset as pandas foundations.
- `src/pandas_demo.py`: completed analyses, meaningful checks, and plot exports.
- `src/build_slide_outputs.py`: generates the tables and values shown on slides.
- `results/`: computed summaries and the final talk-level answer as CSV files.
- `INSTRUCTOR_GUIDE.md`: pacing, discussion answers, and recovery checkpoints.
- `_quarto.yml` and `index.qmd`: website configuration and landing page.
- `docs/`: an HTML preview ready to view or serve through GitHub Pages.

## Lecture flow

The 44-slide deck keeps both opening review attempts, the three conceptual
predictions with debriefs, every analysis and plotting example, the pair
activity, and the exit check. It combines repeated framing, group-size/index
explanations, and plotting/setup material. GroupBy inspection now shows group
membership, an extracted group, and the unchanged source object. The planned
route is about 60 minutes, including 15 minutes of pair work and a full debrief.

## Student setup

Download and extract the repository, or fork it on GitHub and clone your fork.
Open a terminal at its root and run:

```bash
uv sync
```

Open `activity/pandas-questions.qmd` or `activity/pandas-questions.ipynb` in
Positron. Select the `.venv` Python interpreter or kernel. Work through the
starter, then use the completed version for recovery after attempting a task.

Student TODO cells use `eval: false` to keep the published worksheet free of
unfinished-code execution. Run your completed code interactively in Positron.
If you want Quarto to execute a completed TODO cell during a render, remove that
cell's `#| eval: false` line. The completed activity executes every code cell.

## Completed analysis

```bash
uv run python src/pandas_demo.py
```

This checks the supplied data and final answers, then regenerates five figures,
the CSV results, and every included slide-output fragment. The script uses a noninteractive Matplotlib backend so it
also works on a build server. The activities use `plt.show()` for interactive
figures.

## Render the Quarto website

Install Quarto separately, create the environment, and run:

```bash
uv sync
uv run python src/pandas_demo.py
uv run quarto render
```

Using `uv run` makes the project Python environment available to Quarto. Output
goes to `docs/`. Each document executes from its own directory, so activity
paths use `../data/talks.csv`. The slides contain code examples, the
five script-generated figures, and included Markdown fragments with computed
outputs. Regenerate the figures and output fragments after changing data or
analysis code before rendering. The lecture can stand on its own during
presentation; students switch to the worksheet for the pair activity.

The render list excludes the notebook working copies, avoiding output-name
collisions with the Quarto activities. With `freeze: false`, activities execute
again whenever the site renders.

## Publish on GitHub Pages

1. Create the repository with your chosen name and upload these files.
2. In Settings > Pages, choose **Deploy from a branch**.
3. Select your actual default branch, such as `main`, and the `/docs` folder.
4. Save. Link students to the resulting project-site URL.

For a repository named `stat-386-pandas-questions` owned by `USERNAME`, the URL
is `https://USERNAME.github.io/stat-386-pandas-questions/`.

All internal links are relative. The Quarto configuration does not assume a
particular owner or branch. After later edits, regenerate figures, render the
site, and commit the updated source files and `docs/` together. `uv sync`
creates the initial `uv.lock`; commit it to record the resolved environment.

## Preview and verification note

The included `docs/` preview was generated with Pandoc and the RevealJS assets
from the foundations repository because Quarto could not be installed in the
authoring environment. Completed activity cells were executed sequentially and
their outputs were included in that preview. It is a usable static website,
but it is not a Quarto render. Run the commands above for the native Quarto
website, including Quarto's code-copy and navigation features.

The completed script and activity were checked with pandas 2.2.3 and Matplotlib
3.10.8, the available runtime. The project declares pandas 3 to match the
foundations repository. A pandas 3 run and native Quarto render remain the
instructor's final environment checks. The examples use operations shared by
pandas 2.2 and 3, with explicit copies for independent filtered tables.

## Data and technical references

The supplied data is reused unchanged from
[pandas foundations](https://github.com/tjkerby/stat-386-pandas-foundations).
Talk links identify their original sources. `date` is a recorded talk/session
date, `num_words` is a recorded word count, and runtime is a text field that can
be missing. Interpret results as descriptions of the supplied observations.

- [pandas grouping](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [pandas value counts](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
- [pandas dates](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)
- [pandas plotting](https://pandas.pydata.org/docs/user_guide/visualization.html)
- [Quarto Python environments](https://quarto.org/docs/projects/virtual-environments.html)

