import streamlit as st
import subprocess
import re

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Recipe Generator",
    page_icon="🍳"
)

# -------------------------
# TITLE
# -------------------------
st.title("🇮🇳 AI Recipe Generator")
st.write("Generate Indian recipes using leftover ingredients.")

# -------------------------
# INPUTS
# -------------------------
ingredients = st.text_area(
    "🧺 Enter Ingredients",
    placeholder="potato, onion, rice"
)

constraints = st.text_input(
    "⏱️ Constraints",
    placeholder="under 20 minutes"
)

# -------------------------
# BUTTON
# -------------------------
if st.button("🍳 Generate Recipe"):

    # Empty input check
    if ingredients.strip() == "":
        st.warning("Please enter ingredients.")

    else:

        # -------------------------
        # PROMPT
        # -------------------------
        prompt = f"""
You are an expert Indian home cook.

Ingredients:
{ingredients}

Constraints:
{constraints}

Task:
Generate 2 Indian recipes.

Requirements:
- Use only provided ingredients
- Provide numbered cooking steps
- Keep recipes practical and simple
- Mention approximate calories
"""

        st.info("Generating recipes...")

        try:

            # -------------------------
            # RUN OLLAMA
            # -------------------------
            result = subprocess.run(
                ["ollama", "run", "tinyllama"],
                input=prompt,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="ignore",
                timeout=120
            )

            raw_output = result.stdout

            # -------------------------
            # CLEAN OUTPUT
            # -------------------------

            # Remove ANSI escape codes
            clean_output = re.sub(
                r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])',
                '',
                raw_output
            )

            # Remove strange leftover characters
            clean_output = clean_output.replace("", "")

            # Remove excessive blank lines
            clean_output = re.sub(r'\n\s*\n', '\n\n', clean_output)

            clean_output = clean_output.strip()

            # -------------------------
            # DISPLAY OUTPUT
            # -------------------------
            if clean_output:

                st.subheader("🍽️ Generated Recipes")

                st.text_area(
                    "Recipes",
                    clean_output,
                    height=400
                )

            else:
                st.error("No output received from model.")

        except subprocess.TimeoutExpired:
            st.error("Model took too long to respond.")

        except Exception as e:
            st.error(f"Error: {e}")