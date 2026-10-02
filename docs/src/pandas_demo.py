"""Completed analyses and pandas plots for STAT 386."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from build_slide_outputs import build_slide_outputs

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "talks.csv"
FIGURE_DIR = ROOT / "slides" / "figures"
RESULT_DIR = ROOT / "results"


def load_talks() -> pd.DataFrame:
    talks = pd.read_csv(DATA_PATH)
    talks["date"] = pd.to_datetime(
        talks["date"], format="%Y-%m-%d %H:%M:%S.%f"
    )
    return talks


def session_summary(talks: pd.DataFrame) -> pd.DataFrame:
    return (
        talks.groupby("session", as_index=False)
        .agg(
            n_talks=("num_words", "size"),
            mean_words=("num_words", "mean"),
            median_words=("num_words", "median"),
        )
        .sort_values("median_words", ascending=False)
    )


def add_session_comparison(talks: pd.DataFrame) -> pd.DataFrame:
    result = talks.copy()
    result["session_median_words"] = (
        result.groupby("session")["num_words"].transform("median")
    )
    result["above_session_median"] = (
        result["num_words"] > result["session_median_words"]
    )
    return result


def yearly_summary(talks: pd.DataFrame) -> pd.DataFrame:
    work = talks.copy()
    work["talk_year"] = work["date"].dt.year
    return (
        work.groupby("talk_year", as_index=False)
        .agg(
            n_talks=("num_words", "size"),
            mean_words=("num_words", "mean"),
            median_words=("num_words", "median"),
        )
        .sort_values("talk_year")
    )


def final_activity(talks: pd.DataFrame):
    # The reference medians use only the requested 2018-2020 observations.
    recent = talks.loc[talks["year"].between(2018, 2020)].copy()
    all_groups = session_summary(recent)
    eligible = all_groups.loc[all_groups["n_talks"] >= 10].copy()
    compared = add_session_comparison(recent)
    eligible_sessions = eligible["session"]
    above = compared.loc[
        compared["session"].isin(eligible_sessions)
        & compared["above_session_median"],
        ["talk_name", "speaker", "session", "year", "num_words",
         "session_median_words"],
    ].sort_values(["session", "num_words"], ascending=[True, False])
    return recent, all_groups, eligible, compared, above


def make_figures(talks, summary, annual, eligible):
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 16,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "bold", "axes.labelcolor": "#162433",
        "text.color": "#162433", "axes.edgecolor": "#597083",
        "savefig.facecolor": "#f8fafc", "figure.facecolor": "#f8fafc",
        "axes.facecolor": "#f8fafc",
    })

    def save(ax, name):
        ax.figure.tight_layout()
        ax.figure.savefig(FIGURE_DIR / name, dpi=170, bbox_inches="tight")
        plt.close(ax.figure)

    # These are ordinary pandas plotting methods. Matplotlib supplies the axes.
    counts = talks["session"].value_counts().sort_values()
    ax = counts.plot.barh(figsize=(10, 5.5), color="#0062a8")
    ax.set(xlabel="Number of talks", ylabel="Session",
           title="Recorded talks by session, 2010-2020")
    save(ax, "session-counts.png")

    display = summary.sort_values("median_words")
    ax = display.plot.barh(x="session", y="median_words", legend=False,
                           figsize=(10, 5.5), color="#0062a8")
    ax.set(xlabel="Median word count", ylabel="Session",
           title="Typical talk length by session")
    save(ax, "session-medians.png")

    ax = annual.plot.line(x="talk_year", y="median_words", marker="o",
                          legend=False, figsize=(10, 5.5), color="#0062a8")
    ax.set(xlabel="Year", ylabel="Median word count",
           title="Typical talk length by year")
    ax.set_xticks(annual["talk_year"])
    save(ax, "yearly-medians.png")

    ax = talks["num_words"].plot.hist(bins=20, figsize=(10, 5.5),
                                     color="#0062a8", edgecolor="white")
    ax.set(xlabel="Word count", ylabel="Number of talks",
           title="Distribution of recorded talk lengths")
    save(ax, "word-counts.png")

    ax = eligible.sort_values("median_words").plot.barh(
        x="session", y="median_words", legend=False,
        figsize=(10, 5.5), color="#0062a8")
    ax.set(xlabel="Median word count", ylabel="Session",
           title="Sessions with at least 10 talks, 2018-2020")
    save(ax, "activity-medians.png")


def verify(talks, summary, annual, recent, all_groups, eligible, compared, above):
    # Checks express properties of the question and known dataset checkpoints.
    assert talks.shape == (794, 14)
    assert talks["link"].is_unique
    assert summary["n_talks"].sum() == 794
    assert len(summary) == 9
    assert talks["runtime"].notna().sum() == 663
    assert talks["session"].value_counts(normalize=True).sum() == 1.0
    assert talks["date"].dt.year.eq(talks["year"]).all()
    assert annual["talk_year"].tolist() == list(range(2010, 2021))
    assert annual["n_talks"].sum() == 794
    assert summary.loc[summary["session"].eq("priesthood"),
                       "median_words"].item() == 1876
    assert len(recent) == 201
    assert all_groups["n_talks"].sum() == len(recent)
    assert len(compared) == len(recent)
    assert compared.index.equals(recent.index)
    assert eligible["n_talks"].ge(10).all()
    assert above["session"].isin(eligible["session"]).all()
    assert above["num_words"].gt(above["session_median_words"]).all()
    assert above["year"].between(2018, 2020).all()
    # Hand-calculable example makes the aggregation/transform distinction explicit.
    toy = pd.DataFrame({
        "session": ["morning"] * 3 + ["afternoon"] * 3,
        "num_words": [1000, 2000, 3000, 1000, 1200, 1400],
    })
    assert toy.groupby("session")["num_words"].transform("median").tolist() == [
        2000, 2000, 2000, 1200, 1200, 1200]


def main():
    talks = load_talks()
    summary = session_summary(talks)
    annual = yearly_summary(talks)
    recent, all_groups, eligible, compared, above = final_activity(talks)
    verify(talks, summary, annual, recent, all_groups, eligible, compared, above)
    make_figures(talks, summary, annual, eligible)
    build_slide_outputs(talks, summary, annual, recent, eligible, compared, above)
    RESULT_DIR.mkdir(exist_ok=True)
    for name, table in [
        ("session-summary", summary), ("yearly-summary", annual),
        ("recent-session-summary", all_groups), ("activity-summary", eligible),
        ("activity-above-median", above),
    ]:
        table.to_csv(RESULT_DIR / f"{name}.csv", index=False)
    print("Session summary\n", summary.round(1).to_string(index=False))
    print("\nFinal activity summary\n", eligible.round(1).to_string(index=False))
    print(f"\nRecent talks: {len(recent)}; eligible sessions: {len(eligible)}; "
          f"talks above their session median in eligible sessions: {len(above)}")
    print("All question and dataset checks passed.")


if __name__ == "__main__":
    main()
