import streamlit as st
import random
import time

# --- Page Config ---
st.set_page_config(page_title="Simon Says — Python", page_icon="🎵", layout="centered")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# --- Game Colors ---
COLORS = ["Red", "Green", "Blue", "Yellow"]
COLOR_CODES = {
    "Red": "#ff4b4b",
    "Green": "#4bff6a",
    "Blue": "#4b7bff",
    "Yellow": "#fff94b"
}
SOUND_FILES = {
    "Red": "https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg",
    "Green": "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg",
    "Blue": "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg",
    "Yellow": "https://actions.google.com/sounds/v1/cartoon/pop.ogg"
}

# --- Initialize State ---
if "sequence" not in st.session_state:
    st.session_state.sequence = []
if "player_input" not in st.session_state:
    st.session_state.player_input = []
if "round" not in st.session_state:
    st.session_state.round = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "showing" not in st.session_state:
    st.session_state.showing = False
if "high_score" not in st.session_state:
    st.session_state.high_score = 0


def reset_game():
    st.session_state.sequence = []
    st.session_state.player_input = []
    st.session_state.round = 0
    st.session_state.game_over = False
    st.session_state.showing = False


def next_round():
    st.session_state.round += 1
    st.session_state.player_input = []
    st.session_state.sequence.append(random.choice(COLORS))
    st.session_state.showing = True


def check_input():
    expected = st.session_state.sequence[:len(st.session_state.player_input)]
    if st.session_state.player_input != expected:
        st.session_state.game_over = True
        # update high score if needed
        if st.session_state.round - 1 > st.session_state.high_score:
            st.session_state.high_score = st.session_state.round - 1
        return
    if len(st.session_state.player_input) == len(st.session_state.sequence):
        time.sleep(0.5)
        next_round()


# --- Play Sound ---
def play_sound(color):
    sound_file = SOUND_FILES[color]
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{sound_file}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True,
    )


# --- UI Layout ---
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #444;
    }
    .simon-btn {
        height: 120px;
        border-radius: 15px;
        font-size: 22px;
        font-weight: bold;
        color: black;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .simon-btn:hover {
        transform: scale(1.05);
        transition: 0.2s;
        border: 2px solid #333;
    }
    .game-over {
        text-align: center;
        color: red;
        font-size: 28px;
        font-weight: bold;
    }
    .score-box {
        background: #f0f2f6;
        padding: 12px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>🎵 Simon Says</div>", unsafe_allow_html=True)
st.caption("Repeat the sequence of colors. Each round adds one more!")

# Show High Score
st.markdown(
    f"<div class='score-box'>🏆 Highest Score: {st.session_state.high_score}</div>",
    unsafe_allow_html=True
)

if st.button("🚀 Start New Game", use_container_width=True):
    reset_game()
    next_round()
    st.rerun()

if st.session_state.round > 0:
    st.subheader(f"Round {st.session_state.round}")

    # Show sequence (flashing colors)
    if st.session_state.showing:
        placeholder = st.empty()
        for color in st.session_state.sequence:
            placeholder.markdown(
                f"""
                <div style='text-align:center; font-size:45px; font-weight:bold;
                background:{COLOR_CODES[color]}; color:black; padding:25px;
                border-radius:15px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);'>
                {color} ✨
                </div>
                """,
                unsafe_allow_html=True
            )
            play_sound(color)   # 🔊 Play sound here
            time.sleep(1)
            placeholder.empty()
            time.sleep(0.3)
        st.session_state.showing = False
        st.rerun()

    if not st.session_state.game_over:
        st.write("👉 Click the colors in order:")

        cols = st.columns(2)
        for idx, color in enumerate(COLORS):
            if cols[idx % 2].button(color, use_container_width=True, key=f"btn_{color}"):
                if not st.session_state.showing and not st.session_state.game_over:
                    st.session_state.player_input.append(color)
                    play_sound(color)   # 🔊 Sound when player clicks
                    check_input()
                    st.rerun()
    else:
        st.markdown(
            f"<div class='game-over'>❌ Game Over! You reached Round {st.session_state.round}.</div>",
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption("Built with ❤️ in Python + Streamlit")
