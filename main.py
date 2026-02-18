import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_groq import ChatGroq
import streamlit as st


st.set_page_config(page_title="Health Care Assistant", layout="wide")


def apply_custom_styles():
    st.markdown(
        """
        <style>
        :root {
            --primary-color: #0b7fab;
            --accent-color: #16a393;
            --bg-color: #f5f7fb;
            --card-bg: #ffffff;
            --border-soft: #e1e7f0;
            --text-main: #1f2933;
            --text-muted: #6b7280;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b7fab 0%, #0f93c1 40%, #f5f7fb 100%);
        }

        section[data-testid="stSidebar"] .css-1d391kg, 
        section[data-testid="stSidebar"] .css-1cypcdb {
            padding-top: 1.75rem;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }

        h1 {
            color: var(--primary-color);
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        h2, h3 {
            color: var(--text-main);
            font-weight: 600;
        }

        .subtitle-text {
            color: var(--text-muted);
            font-size: 0.98rem;
            margin-bottom: 1.3rem;
        }

        .hc-input-card {
            background-color: var(--card-bg);
            border-radius: 14px;
            padding: 1.5rem 1.4rem;
            border: 1px solid var(--border-soft);
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
        }

        .hc-metrics-row {
            display: flex;
            gap: 0.75rem;
            margin-top: 0.75rem;
            flex-wrap: wrap;
        }

        .hc-pill {
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            border: 1px solid rgba(11, 127, 171, 0.16);
            background: rgba(240, 250, 255, 0.9);
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .hc-section-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--text-muted);
            margin-bottom: 0.35rem;
        }

        .hc-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 1.2rem 1.1rem;
            border: 1px solid var(--border-soft);
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
            margin-bottom: 0.9rem;
        }

        .hc-card h4 {
            margin: 0 0 0.4rem 0;
            font-size: 0.98rem;
            color: var(--primary-color);
        }

        .hc-card p {
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.4;
            color: var(--text-main);
            white-space: pre-line;
        }

        .hc-badge {
            display: inline-block;
            padding: 0.18rem 0.6rem;
            border-radius: 999px;
            font-size: 0.74rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            background: rgba(22, 163, 147, 0.06);
            color: var(--accent-color);
            border: 1px solid rgba(22, 163, 147, 0.24);
            margin-bottom: 0.35rem;
        }

        .stTextArea textarea, .stTextInput input {
            border-radius: 10px;
            border: 1px solid var(--border-soft);
            background-color: #f9fbff;
        }

        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 1px rgba(11, 127, 171, 0.35);
        }

        .stButton>button {
            border-radius: 999px;
            background: linear-gradient(90deg, #0b7fab, #16a393);
            color: #ffffff;
            border: none;
            padding: 0.5rem 1.4rem;
            font-weight: 600;
            letter-spacing: 0.04em;
        }

        .stButton>button:hover {
            background: linear-gradient(90deg, #0a6d94, #138778);
        }

        .stExpander {
            border-radius: 12px;
            border: 1px solid var(--border-soft);
            background-color: #f8fafc;
        }

        .stExpander div[role="button"] {
            font-size: 0.9rem;
            color: var(--text-main);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_custom_styles()


with st.sidebar:
    st.markdown(
        """
        <div style="padding-bottom: 1rem;">
            <div class="hc-badge">Secure session</div>
            <h2 style="color: #f9fafb; margin-bottom: 0.25rem;">Health Care Assistant</h2>
            <p style="color: #e5e7eb; font-size: 0.86rem; margin-bottom: 1.1rem;">
                Enter your API key to start a private, AI-assisted triage session.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(" ")
    api_key_input = st.text_input("Gemini API Key", type="password")

    if api_key_input:
        os.environ["GOOGLE_API_KEY"] = api_key_input


st.markdown(
    """
    <div>
        <h1>Health Planning Assistant</h1>
        <p class="subtitle-text">
            A focused assistant that summarizes likely conditions, first aid options, and
            supportive nutrition for your symptoms. Designed for rapid, structured review.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.35, 1])

with left:
    st.markdown('<div class="hc-section-label">Patient summary</div>', unsafe_allow_html=True)
    input_text = st.text_area(
        "Describe the symptoms and relevant history",
        placeholder=(
            "Example: 3-day history of mild fever, dry cough, sore throat, and fatigue. "
            "No known chronic conditions or recent travel."
        ),
        height=140,
    )
    analyze_clicked = st.button("Analyze symptoms", use_container_width=True)
    st.markdown(
        """
        <div class="hc-metrics-row">
            <span class="hc-pill">Summarized, not diagnostic</span>
            <span class="hc-pill">Two conditions, medications, nutrition</span>
            <span class="hc-pill">Conversation-aware follow-up</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown('<div class="hc-section-label">Assistant overview</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hc-card">
            <h4>What this assistant provides</h4>
            <p>
                This tool organizes symptom information into three views:
                likely conditions, first aid options that may be discussed
                with a clinician, and supportive nutrition ideas. It is
                intended to structure thinking, not replace medical care.
            </p>
        </div>
        <div class="hc-card">
            <h4>Clinical safety note</h4>
            <p>
                All outputs are generated by an AI model and may be incomplete
                or inaccurate. Always confirm findings, medications, and diet
                changes with a qualified health professional.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if "conditions_history" not in st.session_state:
    st.session_state["conditions_history"] = []
if "medications_history" not in st.session_state:
    st.session_state["medications_history"] = []
if "nutrition_history" not in st.session_state:
    st.session_state["nutrition_history"] = []

with st.sidebar:
    backend = st.selectbox("Model backend", ["Gemini (Google)", "Llama (Groq)"], index=0)
    if backend == "Gemini (Google)":
        model_options = ["gemini-2.5-flash", "gemini-2.5-pro"]
    else:
        model_options = ["llama-3.1-8b-instant", "llama-3.1-70b-versatile"]
    selected_model = st.selectbox("Model", model_options, index=0)
    if backend == "Llama (Groq)":
        groq_key_input = st.text_input("Groq API Key (for Llama)", type="password")
        if groq_key_input:
            os.environ["GROQ_API_KEY"] = groq_key_input

if backend == "Gemini (Google)" and not os.getenv("GOOGLE_API_KEY"):
    st.info("Add your Gemini API key in the left panel to begin.")
    st.stop()
elif backend == "Llama (Groq)" and not os.getenv("GROQ_API_KEY"):
    st.info("Add your Groq API key in the left panel to use Llama models.")
    st.stop()

if backend == "Gemini (Google)":
    llm = GoogleGenerativeAI(
        model=selected_model,
        temperature=0.8,
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
    )
else:
    llm = ChatGroq(
        model=selected_model,
        temperature=0.8,
    )

symptoms_prompt = PromptTemplate(
    input_variables=["symptoms"],
    template="List 2 possible conditions for these symptoms: {symptoms}. Summarize.",
)
medications_prompt = PromptTemplate(
    input_variables=["condition"],
    template="Provide 2 first aid medications for {condition}. Summarize.",
)

nutrition_prompt = PromptTemplate(
    input_variables=["condition"],
    template="Recommend 2 nutritional foods for {condition}. Summarize.",
)

def run_healthcare_flow(llm_obj, symptoms_text):
    def to_text(value):
        if isinstance(value, str):
            return value
        content = getattr(value, "content", None)
        if isinstance(content, str):
            return content
        return str(value)

    symptoms_input = {"symptoms": symptoms_text}
    condition_prompt_text = symptoms_prompt.format(**symptoms_input)
    condition_raw = llm_obj.invoke(condition_prompt_text)
    condition_text = to_text(condition_raw)
    st.session_state["conditions_history"].append(condition_text)

    medications_input = {"condition": condition_text}
    medications_prompt_text = medications_prompt.format(**medications_input)
    medications_raw = llm_obj.invoke(medications_prompt_text)
    medications_text = to_text(medications_raw)
    st.session_state["medications_history"].append(medications_text)

    nutrition_input = {"condition": condition_text}
    nutrition_prompt_text = nutrition_prompt.format(**nutrition_input)
    nutrition_raw = llm_obj.invoke(nutrition_prompt_text)
    nutrition_text = to_text(nutrition_raw)
    st.session_state["nutrition_history"].append(nutrition_text)

    return {
        "condition": condition_text,
        "medications": medications_text,
        "nutrition": nutrition_text,
    }

if analyze_clicked and input_text:
    try:
        results = run_healthcare_flow(llm, input_text)

        st.markdown("### Structured assessment")

        col_conditions, col_medications, col_nutrition = st.columns(3)

        with col_conditions:
            st.markdown(
                f"""
                <div class="hc-card">
                    <h4>Possible conditions</h4>
                    <p>{results.get('condition', '')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_medications:
            st.markdown(
                f"""
                <div class="hc-card">
                    <h4>First aid medications</h4>
                    <p>{results.get('medications', '')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_nutrition:
            st.markdown(
                f"""
                <div class="hc-card">
                    <h4>Nutritional support</h4>
                    <p>{results.get('nutrition', '')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.expander("Conversation history – conditions"):
            history = st.session_state.get("conditions_history", [])
            st.info("\n\n".join(history) if history else "No history yet.")

        with st.expander("Conversation history – medications"):
            history = st.session_state.get("medications_history", [])
            st.info("\n\n".join(history) if history else "No history yet.")

        with st.expander("Conversation history – nutrition"):
            history = st.session_state.get("nutrition_history", [])
            st.info("\n\n".join(history) if history else "No history yet.")
    except Exception as e:
        msg = str(e)
        if "RESOURCE_EXHAUSTED" in msg or "429" in msg:
            if backend == "Gemini (Google)":
                st.error(
                    "Your Gemini API quota appears to be exhausted or rate-limited. "
                    "You can switch to the Llama (Groq) backend in the sidebar."
                )
            else:
                st.error(
                    "Your Llama (Groq) quota appears to be exhausted or rate-limited. "
                    "Check your Groq plan and billing, or try again later."
                )
        else:
            if backend == "Gemini (Google)":
                fallback_models = [m for m in model_options if m != selected_model]
                retried = False
                if any(s in msg for s in ["404", "not found for API version", "is not supported for generateContent"]):
                    for fm in fallback_models:
                        try:
                            alt_llm = GoogleGenerativeAI(
                                model=fm,
                                temperature=0.8,
                                google_api_key=os.environ.get("GOOGLE_API_KEY"),
                            )
                            results = run_healthcare_flow(alt_llm, input_text)
                            st.warning(
                                f"Model '{selected_model}' is unavailable for this API version or method. "
                                f"Switched to '{fm}' for this run."
                            )
                            col_conditions, col_medications, col_nutrition = st.columns(3)
                            with col_conditions:
                                st.markdown(
                                    f"""
                                    <div class="hc-card">
                                        <h4>Possible conditions</h4>
                                        <p>{results.get('condition', '')}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            with col_medications:
                                st.markdown(
                                    f"""
                                    <div class="hc-card">
                                        <h4>First aid medications</h4>
                                        <p>{results.get('medications', '')}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            with col_nutrition:
                                st.markdown(
                                    f"""
                                    <div class="hc-card">
                                        <h4>Nutritional support</h4>
                                        <p>{results.get('nutrition', '')}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            with st.expander("Conversation history – conditions"):
                                history = st.session_state.get("conditions_history", [])
                                st.info("\n\n".join(history) if history else "No history yet.")
                            with st.expander("Conversation history – medications"):
                                history = st.session_state.get("medications_history", [])
                                st.info("\n\n".join(history) if history else "No history yet.")
                            with st.expander("Conversation history – nutrition"):
                                history = st.session_state.get("nutrition_history", [])
                                st.info("\n\n".join(history) if history else "No history yet.")
                            retried = True
                            break
                        except Exception:
                            continue
                if not retried:
                    st.error(f"An error occurred while generating results: {e}")
            else:
                st.error(f"An error occurred while generating results: {e}")
