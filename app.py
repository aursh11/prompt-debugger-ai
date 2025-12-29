import streamlit as st
from openai import OpenAI

# ---------------- OPENAI CLIENT ---------------- #
client = OpenAI()

# ---------------- PROMPT TEMPLATE ---------------- #
PROMPT_TEMPLATE = """
You are an expert Prompt Engineer with deep knowledge of Large Language Models.

Your task is to analyze and improve prompts.

Steps:
1. Identify issues in clarity, structure, missing context, or constraints
2. Rewrite the prompt into a high-quality, professional version
3. Explain why the improved prompt works better
4. Give a quality score from 1 to 10 for the improved prompt

Constraints:
- Do not change the original intent
- Be concise and structured
- Focus only on prompt quality

Output Format:

IMPROVED_PROMPT:
<rewrite without quotation marks>

ISSUES:
- issue 1
- issue 2
- issue 3

WHY_BETTER:
- reason 1
- reason 2
- reason 3

QUALITY_SCORE:
<number between 1 and 10>

Prompt to improve:
\"\"\"
{user_prompt}
\"\"\"
"""

def improve_prompt(user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional AI prompt engineer."},
            {"role": "user", "content": PROMPT_TEMPLATE.format(user_prompt=user_prompt)}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


# ---------------- STREAMLIT CONFIG ---------------- #
st.set_page_config(
    page_title="Prompt Debugger & Improver AI",
    page_icon="🧠",
    layout="centered"
)

# ---------------- GLOBAL CSS ---------------- #
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #e6e6e6;
}

h1, h2, h3 {
    color: #ffffff;
    font-weight: 700;
}

p, li {
    color: #dcdcdc;
    font-size: 16px;
    line-height: 1.6;
}

.score-badge {
    display: inline-block;
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: black;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 15px;
}

.copy-btn {
    background-color: #2563eb;
    color: white;
    padding: 8px 14px;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown("<h1 style='text-align:center;'> Prompt Debugger & Improver AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>Turn weak prompts into professional, high-quality prompts</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- INPUT ---------------- #
user_prompt = st.text_area(
    " Enter a weak or unclear prompt",
    height=150,
    placeholder="e.g. write mail"
)

# ---------------- ACTION ---------------- #
if st.button(" Improve Prompt"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Analyzing and improving prompt..."):
            raw_output = improve_prompt(user_prompt)

        try:
            improved = raw_output.split("IMPROVED_PROMPT:")[1].split("ISSUES:")[0].strip()
            issues = raw_output.split("ISSUES:")[1].split("WHY_BETTER:")[0].strip()
            why_better = raw_output.split("WHY_BETTER:")[1].split("QUALITY_SCORE:")[0].strip()
            score = raw_output.split("QUALITY_SCORE:")[1].strip()
        except Exception:
            st.error("Unexpected response format. Please try again.")
            st.stop()

        st.markdown("---")

        # ---------------- SCORE ---------------- #
        st.markdown("##  Prompt Quality Score")
        st.markdown(
            f"<span class='score-badge'>Score: {score}/10</span>",
            unsafe_allow_html=True
        )

        # ---------------- IMPROVED PROMPT ---------------- #
        st.markdown("##  Improved Prompt")

        st.markdown(
            f"""
            <div id="promptBox" style="
                background-color: #ffffff;
                color: #000000;
                padding: 20px;
                border-radius: 12px;
                font-family: 'Courier New', monospace;
                font-size: 16px;
                line-height: 1.6;
                box-shadow: 0px 6px 20px rgba(0,0,0,0.35);
            ">
                {improved}
            </div>
            """,
            unsafe_allow_html=True
        )

    
        # ---------------- ISSUES ---------------- #
        st.markdown("## Issues Detected")
        st.markdown(
            f"""
            <div style="
                background-color: #1c1f26;
                color: #f5f5f5;
                padding: 16px;
                border-radius: 10px;
                border-left: 5px solid #ff4b4b;
            ">
                {issues}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------- WHY BETTER ---------------- #
        st.markdown("##  Why This Is Better")
        st.markdown(
            f"""
            <div style="
                background-color: #1c1f26;
                color: #f5f5f5;
                padding: 16px;
                border-radius: 10px;
                border-left: 5px solid #22c55e;
            ">
                {why_better}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Built by an Applied AI Engineer | Prompt Engineering Project")
