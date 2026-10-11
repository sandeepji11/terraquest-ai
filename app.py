import streamlit as st
import requests

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="TerraQuest AI",
    page_icon="🌿",
    layout="centered"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #e8f5e9, #ffffff);
    color: #1b4332;
}

/* Main Title */
h1 {
    color: #1b5e20 !important;
    text-align: center;
    font-size: 45px !important;
}

/* Headings */
h2, h3 {
    color: #2e7d32 !important;
}

/* Paragraphs */
p {
    color: #263238 !important;
}

/* Labels */
label,
[data-testid="stWidgetLabel"] p {
    color: #1b4332 !important;
}

/* Text Input */
.stTextInput input {
    background-color: #ffffff !important;
    color: #1b4332 !important;
    border: 2px solid #a5d6a7;
    border-radius: 10px;
}

/* Dropdown */
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #1b4332 !important;
    border-radius: 10px;
}

/* Buttons */
.stButton > button {
    background-color: #2e7d32 !important;
    color: white !important;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: bold;
    border: none;
    width: 100%;
}

/* Button Hover */
.stButton > button:hover {
    background-color: #1b5e20 !important;
    color: white !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #1b5e20 !important;
}

/* Slider */
[data-testid="stSlider"] {
    color: #1b4332 !important;
}

/* Captions */
.stCaption {
    color: #455a64 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "adventure" not in st.session_state:
    st.session_state.adventure = None

if "completed" not in st.session_state:
    st.session_state.completed = 0

if "adventure_started" not in st.session_state:
    st.session_state.adventure_started = False


# ==========================================
# HEADER
# ==========================================

st.title("🌿 TerraQuest AI")

st.markdown(
    "<h3 style='text-align:center; color:#2e7d32;'>"
    "Stop Scrolling. Start Exploring."
    "</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>"
    "Your AI-powered companion for real-world adventures."
    "</p>",
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# USER INPUTS
# ==========================================

st.subheader("🌍 Create Your Adventure")

location = st.text_input(
    "📍 Your City",
    placeholder="Enter your city (e.g., Pune)"
)

duration = st.slider(
    "⏱ Available Time (minutes)",
    min_value=10,
    max_value=120,
    value=30,
    step=10
)

interest = st.selectbox(
    "🌱 Your Interest",
    [
        "Nature",
        "Photography",
        "Walking",
        "Bird Watching",
        "Exploration",
        "Mindfulness"
    ]
)

difficulty = st.selectbox(
    "⚡ Difficulty Level",
    [
        "Easy",
        "Medium",
        "Challenging"
    ]
)


# ==========================================
# AI ADVENTURE GENERATOR
# ==========================================

def generate_adventure(city, minutes, activity, level):

    prompt = f"""
You are TerraQuest AI, a friendly outdoor adventure guide.

Create a personalized outdoor adventure.

User Details:
City: {city}
Available Time: {minutes} minutes
Interest: {activity}
Difficulty: {level}

Generate the following:

1. A creative adventure title.
2. Four interesting outdoor missions.
3. One fun nature observation.
4. A motivational closing message.

Important Rules:
- Keep the activities safe and accessible.
- Encourage outdoor exploration.
- Avoid dangerous or restricted locations.
- Do not invent specific local landmarks.
- Minimize screen time.
- Keep the response short and engaging.
- Format the answer using Markdown.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]


# ==========================================
# GENERATE ADVENTURE BUTTON
# ==========================================

if st.button("🚀 Generate My Adventure"):

    with st.spinner("🌿 AI is creating your adventure..."):

        try:

            city = location.strip() or "My Neighborhood"

            adventure = generate_adventure(
                city,
                duration,
                interest,
                difficulty
            )

            st.session_state.adventure = adventure
            st.session_state.adventure_started = False

            st.success("Your adventure is ready!")

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to Ollama. "
                "Make sure Ollama is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏳ AI took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.RequestException as error:

            st.error(f"AI request failed: {error}")

        except (KeyError, ValueError):

            st.error(
                "Unexpected response from Ollama. "
                "Please try again."
            )


# ==========================================
# DISPLAY GENERATED ADVENTURE
# ==========================================

if st.session_state.adventure:

    st.divider()

    st.subheader("🌿 Your Personalized Adventure")

    st.markdown(st.session_state.adventure)

    st.divider()

    st.subheader("📵 Touch Grass Mode")

    st.info(
        "Read your adventure, put your phone away, "
        "and explore the real world!"
    )

    if not st.session_state.adventure_started:

        if st.button("🌍 Start My Adventure"):

            st.session_state.adventure_started = True

            st.rerun()

    else:

        st.success(
            "🌱 Adventure started! "
            "Enjoy your time outdoors."
        )

        if st.button("🏆 I Completed My Adventure!"):

            st.session_state.completed += 1

            st.session_state.adventure = None

            st.session_state.adventure_started = False

            st.balloons()

            st.success(
                "Congratulations! "
                "You completed your adventure!"
            )


# ==========================================
# ACHIEVEMENTS
# ==========================================

st.divider()

st.subheader("🏅 Your Achievements")

st.metric(
    label="🌍 Adventures Completed",
    value=st.session_state.completed
)

if st.session_state.completed == 0:

    st.info(
        "Complete your first adventure "
        "to unlock a badge!"
    )

elif st.session_state.completed < 3:

    st.success(
        "🌱 Badge Unlocked: Nature Explorer"
    )

elif st.session_state.completed < 5:

    st.success(
        "🌿 Badge Unlocked: Nature Enthusiast"
    )

else:

    st.success(
        "🏆 Badge Unlocked: Outdoor Champion"
    )


# ==========================================
# ABOUT SECTION
# ==========================================

st.divider()

with st.expander("ℹ️ About TerraQuest AI"):

    st.write("""
    TerraQuest AI is an open-source AI-powered
    outdoor adventure generator.

    Our mission is simple:

    Encourage people to spend less time
    scrolling and more time exploring
    the real world.

    The application uses a locally running
    open-weight language model to generate
    personalized outdoor activities.
    """)

    st.markdown("**Technologies Used:**")

    st.write("🐍 Python")
    st.write("🌐 Streamlit")
    st.write("🧠 Ollama")
    st.write("🤖 Qwen2.5 1.5B")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    "<p style='text-align:center; color:#2e7d32;'>"
    "🌿 TerraQuest AI — Your Adventure Begins Outside!"
    "</p>",
    unsafe_allow_html=True
)

st.caption(
    "Powered by Open-Weight AI | "
    "Built with Python, Streamlit & Ollama"
)
