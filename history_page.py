
import streamlit as st

from screening_history import (
    get_screenings,
    load_screening,
    delete_screening
)
from pdf_report import generate_pdf_report


def show_history_page():
    st.title("📚 Screening History")
    st.write("View and download your previously saved analyses.")

    email = st.session_state.get("user_email")

    if not email:
        st.warning("Please log out and sign in again to access history.")
        return

    sessions = get_screenings(email)

    if not sessions:
        st.info("No saved screenings yet. Analyze resumes and save a report.")
        return

    for session in sessions:
        session_id = session["id"]

        with st.expander(
            f"📁 {session['job_title']} | "
            f"{session['created_at'][:16]} UTC"
        ):
            df = load_screening(session_id, email)

            if df is None or df.empty:
                st.warning("No results found.")
                continue

            st.metric("Candidates", len(df))
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            csv_data = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 Download CSV",
                data=csv_data,
                file_name=f"screening_{session_id}.csv",
                mime="text/csv",
                key=f"history_csv_{session_id}"
            )

            st.download_button(
                "📄 Download PDF",
                data=generate_pdf_report(df),
                file_name=f"screening_{session_id}.pdf",
                mime="application/pdf",
                key=f"history_pdf_{session_id}"
            )

            if st.button(
                "🗑️ Delete Saved Screening",
                key=f"delete_history_{session_id}"
            ):
                delete_screening(session_id, email)
                st.success("Screening deleted.")
                st.rerun()
