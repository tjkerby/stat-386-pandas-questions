"""Generate the visible slide results from the same teaching data and analyses."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "slides" / "outputs"


def markdown_table(frame: pd.DataFrame) -> str:
    """Write a portable Markdown table without an extra formatting dependency."""
    def cell(value):
        if pd.isna(value):
            return "NaN"
        return str(value).replace("|", "\\|").replace("\n", " ")
    header = "| " + " | ".join(map(str, frame.columns)) + " |"
    align = "| " + " | ".join(
        "--:" if pd.api.types.is_numeric_dtype(frame[c]) else ":--"
        for c in frame.columns
    ) + " |"
    rows = ["| " + " | ".join(cell(v) for v in row) + " |"
            for row in frame.itertuples(index=False, name=None)]
    return "\n".join([header, align, *rows]) + "\n"


def build_slide_outputs(talks, summary, annual, recent, eligible, compared, above):
    OUTPUT_DIR.mkdir(exist_ok=True)

    def table(name, frame):
        (OUTPUT_DIR / f"{name}.md").write_text(markdown_table(frame))

    def text(name, value):
        (OUTPUT_DIR / f"{name}.md").write_text("```text\n" + str(value) + "\n```\n")

    toy = pd.DataFrame({
        "talk": list("ABCDEF"),
        "session": ["morning"] * 3 + ["afternoon"] * 3,
        "num_words": [1000, 2000, 3000, 1000, 1200, 1400],
    })
    grouped = toy.groupby("session")
    assert grouped.obj is toy
    assert grouped.ngroups == 2
    assert grouped.indices["morning"].tolist() == [0, 1, 2]
    assert grouped.get_group("morning")["talk"].tolist() == list("ABC")
    table("toy", toy)
    table("toy-medians", grouped["num_words"].median().rename("median_words").reset_index())
    text("groupby-membership", str(type(grouped).__name__) + " " + str(grouped.ngroups)
         + "\n" + repr(grouped.indices))
    table("morning-group", grouped.get_group("morning"))
    table("groupby-reductions", pd.DataFrame({
        "median": grouped["num_words"].median(),
        "mean": grouped["num_words"].mean(),
        "size": grouped.size(),
    }).reset_index())
    text("groupby-source", "True")

    decode = talks.loc[
        talks["year"].eq(2020) & talks["session"].eq("sunday-morning"),
        ["talk_name", "speaker", "num_words"],
    ].sort_values("num_words", ascending=False).head(3)
    construct = talks.loc[
        talks["year"].between(2019, 2020) & talks["session"].eq("saturday-morning"),
        ["talk_name", "speaker", "year", "num_words"],
    ].sort_values("num_words", ascending=False).head(3)
    assert decode["num_words"].tolist() == [2591, 1912, 1858]
    table("review-decode", decode)
    table("review-construct", construct)
    text("overall-median", talks["num_words"].median())
    table("group-medians", talks.groupby("session")["num_words"].median()
          .rename("median_words").reset_index())

    counts = talks["session"].value_counts()
    proportions = talks["session"].value_counts(normalize=True)
    table("counts-proportions", pd.DataFrame({
        "count": counts, "proportion": proportions.round(3)
    }).rename_axis("session").reset_index())
    table("recent-proportions", recent["session"].value_counts(normalize=True)
          .round(3).rename("proportion").rename_axis("session").reset_index())
    table("runtime-counts", talks.groupby("session", as_index=False).agg(
        n_talks=("runtime", "size"), n_recorded_runtimes=("runtime", "count")
    ))
    text("summary-shape", summary.shape)
    table("session-summary", summary.round(1))
    keys = talks.groupby(["year", "session"], as_index=False).agg(
        n_talks=("num_words", "size"), median_words=("num_words", "median")
    )
    table("year-session", keys.head(4))
    text("year-session-shape", keys.shape)

    long_toy = toy.loc[toy["num_words"] >= 1500]
    filtered = long_toy.groupby("session", as_index=False).agg(
        median_words=("num_words", "median"))
    all_toy = grouped["num_words"].median().rename("median_words").reset_index()
    selected = all_toy.loc[all_toy["median_words"] >= 1500]
    assert filtered["median_words"].tolist() == [2500.0]
    assert selected["median_words"].tolist() == [2000.0]
    table("filter-first", filtered)
    table("summarize-first", selected)
    toy["session_median_words"] = grouped["num_words"].transform("median")
    assert toy["session_median_words"].tolist() == [2000, 2000, 2000, 1200, 1200, 1200]
    table("toy-transformed", toy)

    all_compared = talks.copy()
    all_compared["session_median_words"] = (
        talks.groupby("session")["num_words"].transform("median"))
    all_compared["above_session_median"] = (
        all_compared["num_words"] > all_compared["session_median_words"])
    table("talk-references", all_compared.iloc[[0, 2, 10, 12]][
        ["session", "num_words", "session_median_words", "above_session_median"]])
    all_above = all_compared.loc[all_compared["above_session_median"]]
    table("above-all-years", all_above[["talk_name", "session", "num_words"]].head(3))
    text("all-years-count", len(all_above))

    medians = talks.groupby("session")["num_words"].median()
    refs = talks.groupby("session")["num_words"].transform("median")
    text("alignment", "medians.index[:2]  = " + repr(medians.index[:2].tolist())
         + "\nreference.index[:2] = " + repr(refs.index[:2].tolist()))
    table("recent-references", compared[["session", "num_words", "session_median_words"]].head(3))
    dates = talks.copy()
    dates["date"] = pd.to_datetime(dates["date"], format="%Y-%m-%d %H:%M:%S.%f")
    dates["talk_year"] = dates["date"].dt.year
    dates["talk_month"] = dates["date"].dt.month
    assert dates["talk_year"].eq(dates["year"]).all()
    display = dates[["date", "talk_year", "talk_month"]].head(3).copy()
    display["date"] = display["date"].dt.strftime("%Y-%m-%d")
    table("date-components", display)
    table("annual", annual[["talk_year", "n_talks", "median_words"]])
    table("eligible-summary", eligible[["session", "n_talks", "median_words"]])
    slide_above = compared.loc[
        compared["session"].isin(eligible["session"])
        & compared["above_session_median"]
    ]
    assert len(slide_above) == len(above) == 95
    table("above-recent", slide_above[
        ["talk_name", "session", "num_words", "session_median_words"]
    ].head(3))
    text("final-count", len(above))
    return {"groups": grouped.ngroups, "recent_talks": len(recent), "above_talks": len(above)}
