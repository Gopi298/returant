import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Login System",
    page_icon="🔐",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.login-container {
    max-width: 450px;
    margin: auto;
    padding: 30px;
}

.title {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# USER DATABASE
# --------------------------------------------------

USERS = {
    "admin": "admin123",
    "gopi": "gopi123",
    "user": "user123"
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------

if not st.session_state.logged_in:

    st.markdown(
        '<div class="login-container">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="title">🔐 Login</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Please enter your username and password</div>',
        unsafe_allow_html=True
    )

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    login_button = st.button(
        "🔓 Login",
        use_container_width=True
    )

    if login_button:

        if username in USERS and USERS[username] == password:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login successful!")

            st.rerun()

        else:

            st.error("❌ Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# HOME PAGE AFTER LOGIN
# --------------------------------------------------

else:

    st.title("🏠 Welcome")

    st.success(
        f"Welcome, {st.session_state.username}!"
    )

    st.write(
        "You have successfully logged into the application."
    )

    st.markdown("---")

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Users", "100")

    with col2:
        st.metric("Projects", "25")

    with col3:
        st.metric("Status", "Active")

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()
