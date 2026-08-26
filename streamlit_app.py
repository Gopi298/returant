import streamlit as st

# =========================================================
# RESTAURANT CHATBOT - STREAMLIT APP
# =========================================================

st.set_page_config(
    page_title="Foodie AI Restaurant",
    page_icon="🍴",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

* {
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #ff512f, #dd2476);
}

.main {
    padding-top: 20px;
}

.chat-container {
    max-width: 500px;
    margin: auto;
    background: white;
    border-radius: 25px;
    overflow: hidden;
    box-shadow: 0 15px 50px rgba(0,0,0,0.30);
}

.restaurant-header {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    color: white;
    padding: 25px;
    border-radius: 25px 25px 0 0;
}

.restaurant-title {
    font-size: 28px;
    font-weight: bold;
}

.restaurant-subtitle {
    font-size: 14px;
    margin-top: 5px;
}

.online {
    float: right;
    margin-top: -35px;
    font-size: 13px;
}

.chat-area {
    background: #f8f8f8;
    padding: 20px;
    min-height: 450px;
}

.bot-message {
    background: #eeeeee;
    color: #222222;
    padding: 14px 17px;
    border-radius: 18px;
    border-bottom-left-radius: 5px;
    margin-bottom: 15px;
    max-width: 85%;
    line-height: 1.5;
}

.user-message {
    background: #ff512f;
    color: white;
    padding: 14px 17px;
    border-radius: 18px;
    border-bottom-right-radius: 5px;
    margin-bottom: 15px;
    margin-left: auto;
    max-width: 85%;
    line-height: 1.5;
}

.quick-title {
    font-weight: bold;
    margin-bottom: 8px;
}

div.stButton > button {
    border-radius: 20px;
    border: none;
    background: #fff0eb;
    color: #e64120;
    font-weight: bold;
}

div.stButton > button:hover {
    background: #ff512f;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# RESTAURANT MENU
# =========================================================

MENU = {
    "pizza": [
        ("Margherita Pizza", 250),
        ("Paneer Pizza", 320),
        ("Chicken Pizza", 350),
    ],

    "biryani": [
        ("Veg Biryani", 180),
        ("Chicken Biryani", 250),
        ("Mutton Biryani", 320),
    ],

    "starters": [
        ("Paneer Tikka", 220),
        ("Chicken 65", 240),
        ("Gobi Manchurian", 180),
    ],
}


# =========================================================
# BOT RESPONSE
# =========================================================

def get_bot_response(message):

    text = message.lower().strip()

    # ---------------- HELLO ----------------

    if any(word in text for word in ["hello", "hi", "hey"]):

        return """
        👋 Hello!

        Welcome to <b>Foodie Restaurant</b>.

        How can I help you today? 🍴
        """


    # ---------------- MENU ----------------

    if "menu" in text or "food" in text:

        return """
        <b>🍴 Our Menu</b>

        <br><br>

        🍕 <b>Pizza</b>

        <br>
        Margherita Pizza - ₹250

        <br>
        Paneer Pizza - ₹320

        <br>
        Chicken Pizza - ₹350


        <br><br>

        🍚 <b>Biryani</b>

        <br>
        Veg Biryani - ₹180

        <br>
        Chicken Biryani - ₹250

        <br>
        Mutton Biryani - ₹320


        <br><br>

        🥘 <b>Starters</b>

        <br>
        Paneer Tikka - ₹220

        <br>
        Chicken 65 - ₹240

        <br>
        Gobi Manchurian - ₹180
        """


    # ---------------- VEG ----------------

    if "veg" in text or "vegetarian" in text:

        return """
        🥗 <b>Vegetarian Menu</b>

        <br><br>

        🍕 Margherita Pizza - ₹250

        <br>
        🍕 Paneer Pizza - ₹320

        <br>
        🍚 Veg Biryani - ₹180

        <br>
        🧀 Paneer Tikka - ₹220

        <br>
        🥦 Gobi Manchurian - ₹180
        """


    # ---------------- NON VEG ----------------

    if (
        "non veg" in text
        or "non-veg" in text
        or "chicken" in text
        or "mutton" in text
    ):

        return """
        🍗 <b>Non-Vegetarian Menu</b>

        <br><br>

        🍕 Chicken Pizza - ₹350

        <br>
        🍚 Chicken Biryani - ₹250

        <br>
        🍚 Mutton Biryani - ₹320

        <br>
        🍗 Chicken 65 - ₹240
        """


    # ---------------- PRICE ----------------

    if (
        "price" in text
        or "cost" in text
        or "how much" in text
    ):

        return """
        💰 Our food prices start from <b>₹180</b>.

        <br><br>

        Tell me the dish name and I can show you the price.
        """


    # ---------------- BOOKING ----------------

    if (
        "book" in text
        or "booking" in text
        or "reservation" in text
        or "table" in text
    ):

        return """
        📅 <b>Table Reservation</b>

        <br><br>

        I can help you reserve a table.

        <br><br>

        Please provide:

        <br>👥 Number of people
        <br>📅 Date
        <br>⏰ Time

        <br><br>

        Example:

        <br>
        <i>4 people, August 30, 7:30 PM</i>
        """


    # ---------------- LOCATION ----------------

    if (
        "location" in text
        or "address" in text
        or "where" in text
    ):

        return """
        📍 <b>Foodie Restaurant</b>

        <br><br>

        Chennai, Tamil Nadu

        <br><br>

        🕐 <b>Opening Hours</b>

        <br>
        10:00 AM - 11:00 PM
        """


    # ---------------- HOURS ----------------

    if (
        "open" in text
        or "timing" in text
        or "hours" in text
    ):

        return """
        🕐 <b>Restaurant Hours</b>

        <br><br>

        Monday - Sunday

        <br>
        10:00 AM - 11:00 PM
        """


    # ---------------- THANK YOU ----------------

    if "thank" in text:

        return """
        😊 You're welcome!

        <br><br>

        Thank you for choosing
        <b>Foodie Restaurant</b>! 🍴
        """


    # ---------------- DEFAULT ----------------

    return """
    🤖 I'm your Foodie Restaurant Assistant.

    <br><br>

    I can help you with:

    <br>🍴 Menu
    <br>🥗 Vegetarian food
    <br>🍗 Non-vegetarian food
    <br>💰 Prices
    <br>📅 Table booking
    <br>📍 Location
    <br>🕐 Opening hours

    <br><br>

    Try asking:

    <br>
    <i>"Show me the menu"</i>
    """


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="chat-container">

<div class="restaurant-header">

<div class="restaurant-title">
🍴 Foodie AI
</div>

<div class="restaurant-subtitle">
Restaurant Assistant
</div>

<div class="online">
🟢 Online
</div>

</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
            👋 Hello! Welcome to <b>Foodie Restaurant</b>.

            <br><br>

            I can help you with:

            <br>🍴 Menu
            <br>🥗 Vegetarian food
            <br>🍗 Non-vegetarian food
            <br>💰 Prices
            <br>📅 Table booking
            <br>📍 Location
            """
        }
    ]


# =========================================================
# CHAT DISPLAY
# =========================================================

st.markdown(
    '<div class="chat-area">',
    unsafe_allow_html=True
)


for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="bot-message">
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# QUICK BUTTONS
# =========================================================

st.markdown("### Quick Questions")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button("🍴 Menu", use_container_width=True):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Show me the menu"
            }
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": get_bot_response("Show me the menu")
            }
        )

        st.rerun()


with col2:

    if st.button("🥗 Veg", use_container_width=True):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Show vegetarian food"
            }
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": get_bot_response(
                    "Show vegetarian food"
                )
            }
        )

        st.rerun()


with col3:

    if st.button("📅 Booking", use_container_width=True):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": "I want to book a table"
            }
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": get_bot_response(
                    "I want to book a table"
                )
            }
        )

        st.rerun()


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask about menu, food, price, booking..."
)


if user_input:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Bot message
    response = get_bot_response(user_input)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()
