
import streamlit as st
from auth import register_user, login_user


def show_login_page():
    st.markdown("""
    <style>
    .block-container {
        max-width: 950px;
        padding-top: 3rem;
    }
    .login-heading {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #6366f1;
    }
    .login-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 17px;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="login-heading">AI Resume Screener</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="login-subtitle">'
        'Intelligent Recruitment & Candidate Ranking Platform'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])

    with center:
        login_tab, register_tab = st.tabs(
            ["Sign In", "Create Account"]
        )

        with login_tab:
            st.subheader("Welcome Back")

            with st.form("login_form"):
                email = st.text_input("Email Address")
                password = st.text_input(
                    "Password", type="password"
                )
                submitted = st.form_submit_button(
                    "Sign In", use_container_width=True
                )

            if submitted:
                success, name = login_user(email, password)

                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = name
                    st.session_state["user_email"] = email.strip().lower()
                    st.success("Login successful!")
                    st.rerun()
    
                else:
                    st.error("Invalid email or password.")

        with register_tab:
            st.subheader("Create Your Account")

            with st.form("register_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email", key="reg_email")
                password = st.text_input(
                    "Password", type="password", key="reg_password"
                )
                confirm = st.text_input(
                    "Confirm Password", type="password"
                )
                registered = st.form_submit_button(
                    "Create Account", use_container_width=True
                )

            if registered:
                if password != confirm:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(
                        name, email, password
                    )

                    if success:
                        st.success(message + " Please sign in.")
                    else:
                        st.error(message)

    st.markdown("---")
    st.caption(
        "AI-Powered Resume Screening | NLP | Machine Learning"
    )
