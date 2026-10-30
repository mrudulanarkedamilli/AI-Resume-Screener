
import pandas as pd
import plotly.express as px
import streamlit as st


def show_candidate_analytics(results):
    """Display analytics for already-computed candidate results."""

    if not results:
        st.info("Upload and analyze resumes to view candidate analytics.")
        return

    df = pd.DataFrame(results)

    required = {"candidate", "score", "skill_coverage"}
    missing = required - set(df.columns)

    if missing:
        st.error(
            "Analytics data is missing: " + ", ".join(sorted(missing))
        )
        return

    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["skill_coverage"] = pd.to_numeric(
        df["skill_coverage"], errors="coerce"
    )

    df = df.dropna(subset=["score", "skill_coverage"]).copy()

    if df.empty:
        st.warning("No valid candidate scores were found.")
        return

    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))

    st.markdown("## 📊 Candidate Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Candidates Analyzed", len(df))
    col2.metric("Highest Match", f"{df['score'].max():.1f}%")
    col3.metric("Average Match", f"{df['score'].mean():.1f}%")

    st.markdown("### 🎯 Candidate Matching Scores")

    fig = px.bar(
        df,
        x="candidate",
        y="score",
        color="score",
        text="score",
        color_continuous_scale="Blues",
        labels={
            "candidate": "Candidate",
            "score": "Match Score (%)"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_range=[0, 110],
        coloraxis_showscale=False,
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🏆 Candidate Ranking Table")

    display_columns = [
        "Rank", "candidate", "score", "skill_coverage"
    ]

    for optional in ["matched_skills", "missing_skills"]:
        if optional in df.columns:
            display_columns.append(optional)

    st.dataframe(
        df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 🧠 Skill Coverage Comparison")

    coverage_fig = px.bar(
        df,
        x="candidate",
        y="skill_coverage",
        text="skill_coverage",
        color="skill_coverage",
        color_continuous_scale="Purples",
        labels={
            "candidate": "Candidate",
            "skill_coverage": "Skill Coverage (%)"
        }
    )

    coverage_fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    coverage_fig.update_layout(
        yaxis_range=[0, 110],
        coloraxis_showscale=False,
        height=400
    )

    st.plotly_chart(coverage_fig, use_container_width=True)

    st.markdown("### 📥 Download Results")

    export_df = df.copy()

    for column in ["matched_skills", "missing_skills"]:
        if column in export_df.columns:
            export_df[column] = export_df[column].apply(
                lambda value: ", ".join(map(str, value))
                if isinstance(value, (list, tuple, set))
                else str(value)
            )

    csv_data = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Candidate Rankings (CSV)",
        data=csv_data,
        file_name="candidate_rankings.csv",
        mime="text/csv",
        use_container_width=True
    )
