# Instructor guide

## Purpose

Students should leave able to translate a group comparison into an explicit
pandas analysis. They should identify the reference observations, explain what
defines a group, distinguish filtering observations from filtering summaries,
and choose aggregation or transformation based on the required result unit.

The lesson follows pandas foundations. The opening review retrieves masks,
`.loc[]`, column selection, ordering, and `head()` before introducing new
operations. It contains a decode challenge and a construction challenge, each
with an immediate answer slide.

## Preparation

1. Upload the package to the chosen GitHub repository and give students its
   actual link before class.
2. Run `uv sync` from a fresh clone and commit the generated `uv.lock`.
3. Run `uv run python src/pandas_demo.py` and confirm the answer checks.
4. Run `uv run quarto render` and inspect the native render in the browser.
5. Confirm that students can access the slides, starter, completed activity,
   downloadable notebooks, and data.
6. Open the starter in Positron and select `.venv`.
7. Press `S` in the slide deck to open speaker view.

The script and completed activity were executed in the available pandas 2.2.3
environment. A pandas 3 run and native Quarto render were unavailable here.
The included HTML site is a Pandoc preview, as described in README.md.

## Planned 60-minute pacing

| Minutes | Material |
|:--|:--|
| 0-7 | Decode and construct familiar pipelines, with immediate debriefs |
| 7-19 | Grouping, GroupBy membership, counts, aggregation, filtering order |
| 19-28 | Transformation, visible comparisons, label alignment, reference window |
| 28-32 | Date components and the displayed yearly summary |
| 32-38 | pandas bar charts, line chart, and histogram |
| 38-53 | Final pair activity |
| 53-60 | Full activity debrief, interpretation, and exit check |

The deck has 43 content slides plus the title, down from 51 total slides.
All examples and student attempts remain. The reduction comes from repeated
framing, group-size/index explanations, plotting setup, and worksheet setup.
Use the computed results already on the slides throughout the lecture. Make
one switch to the worksheet when students begin the final pair request.

## Compressed 50-minute pacing

| Minutes | Material |
|:--|:--|
| 0-6 | Both opening attempts and their answers |
| 6-16 | Grouping and summaries, including GroupBy inspection and filter prediction |
| 16-22 | Transformation and the displayed result |
| 22-28 | Dates and plots, reading the embedded output |
| 28-43 | Final pair request |
| 43-50 | Full debrief and exit check |

Keep the 15-minute pair activity. Shorten verbal explanation and use the
embedded results as evidence instead of running the same code live. Present
the date example and histogram briefly. Preserve the prediction attempts and
their immediate answer slides. The fuller worksheet remains available after
class and should not become another complete walkthrough during lecture.

## GroupBy mechanics

The two inspection slides use the six-talk teaching table. The GroupBy retains
the source data object and a grouping specification. pandas requests grouping
work when inspection or an operation needs it. Accessing `ngroups` or `indices`
can trigger that work; these properties are observations of membership, not
proof that the constructor eagerly copied separate tables.

`indices` maps group keys to row positions: morning uses 0, 1, and 2, while
afternoon uses 3, 4, and 5. `get_group("morning")` returns the three matching
observations. The original source still contains all six talks. Column
selection and a reduction then request the desired calculation. The slides
show medians, means, and group sizes together for comparison. The activity
contains the same inspection checkpoints.

## Computed slide outputs

`uv run python src/pandas_demo.py` regenerates figures, result CSVs, and
`slides/outputs/*.md`. The deck includes those fragments with Quarto include
shortcodes. Run the script before rendering after any data or analysis edits.

Output excerpts explicitly identify their scope. Counts and proportions, and
GroupBy reductions, place separately returned Series side by side for easier
comparison. The runtime comparison shows every category. The multi-key example
shows the first four rows plus the full shape. The final talk-level excerpt
shows the first three qualifying rows in the displayed code's original order.

## The three conceptual pauses

### A summary's result unit

Ask students to sketch the median table for six invented talks in two sessions.
It has two rows: morning median 2,000 and afternoon median 1,200. Talk identities
are absent. The immediately following result slide summarizes this distinction.

### Filtering order

Filtering toy talks to at least 1,500 words first leaves B and C, producing a
morning median of 2,500. Calculating session medians from all talks first and
then retaining medians of at least 1,500 produces a morning median of 2,000.
Both retain only morning, but they calculate statistics from different data.

### Transformation's result unit

Ask students to fill in a reference beside each toy talk. Morning A/B/C receive
2,000 and afternoon D/E/F receive 1,200. The transformation retains six rows.
Only C and F strictly exceed their own session median.

## Activity flow

Checkpoint 0 is the opening review. The rest of the worksheet supplies guided
practice and a reference after class. During the lecture, use the embedded outputs rather than alternating between
slides and an editor. The worksheet supplies practice and recovery, rather
than a second complete lecture. Give the main independent pair time to checkpoint 6.

Ask pairs to plan the result units before coding. Pause once after they create
the recent summary and once before the group reference. Keep the completed
activity available for recovery.

## Verified checkpoints

| Check | Expected result |
|:--|:--|
| Original dataset | 794 talks, 14 columns |
| Full-data session summary | 9 categories |
| Recorded runtimes | 663, with 131 missing |
| Derived year | Matches the supplied year for all talks |
| Yearly summary | 11 years, 2010-2020 |
| 2018-2020 reference observations | 201 talks |
| Recent session summary before count filtering | 7 categories, counts sum to 201 |
| Eligible categories with at least 10 talks | 6 categories, counts sum to 194 |
| Excluded recent category | saturday-evening, 7 talks |
| Transform on recent data | 201 aligned reference values |
| Above own recent session median, eligible categories only | 95 talks |

## Final summary

| Session | Count | Median words |
|:--|--:|--:|
| sunday-morning | 37 | 1790 |
| saturday-morning | 41 | 1728 |
| saturday-afternoon | 39 | 1629 |
| sunday-afternoon | 46 | 1621 |
| priesthood | 13 | 1554 |
| womens | 18 | 1480.5 |

The ten-talk threshold is a requested condition. It does not establish a
statistical reliability standard. Emphasize the dataset and reference window
when students write their interpretation.

## Likely misconceptions

- **groupby already produces a summary.** A GroupBy describes groups. A
  reduction or other operation requests the result.
- **count always counts rows.** count excludes missing values in the selected
  variable. size counts rows. Missing group keys are excluded by default unless
  `dropna=False`; the session keys here are complete.
- **a proportion has an obvious denominator.** Count the observations remaining
  after the filter. Talks and distinct speakers are different units.
- **a group median can be directly assigned to talk rows.** The group-indexed
  Series has different labels. transform supplies a talk-indexed result.
- **half the talks must exceed the median.** Strict comparison excludes ties,
  and odd group sizes also prevent an exact half.
- **the recent result can reuse the all-years reference.** The final task asks
  for medians calculated from the 2018-2020 talks.
- **the plot proves a session effect.** The chart describes groups with varying
  speakers and coverage across years. It does not establish causation.
- **a bar chart and histogram have the same unit.** Named categories define bar
  chart positions; numeric intervals define histogram bars.

## Scope boundaries

Dates support grouping and chronological order. No resampling or time-series
index machinery is required. Plotting introduces pandas methods and a few
Matplotlib axis labels. Leave joins, reshaping, regex, and missingness theory
for their planned lectures.
