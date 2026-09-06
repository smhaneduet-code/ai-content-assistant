
import streamlit as st
from groq import Groq


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)


# ==========================================
# TITLE
# ==========================================

st.title("✍️ AI Content Assistant")

st.write(
    "Create engaging social media content using AI."
)


# ==========================================
# GET GROQ API KEY
# ==========================================

try:

    api_key = st.secrets["GROQ_API_KEY"]

except Exception:

    st.error(
        "GROQ_API_KEY is not configured. "
        "Please add it to Streamlit Secrets."
    )

    st.stop()


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=api_key
)


# ==========================================
# USER INPUTS
# ==========================================

content_type = st.selectbox(
    "Content Type",
    [
        "Social Media Post",
        "Advertisement",
        "Product Promotion",
        "Educational Post",
        "Announcement",
        "Motivational Post"
    ]
)


platform = st.selectbox(
    "Platform",
    [
        "Instagram",
        "Facebook",
        "LinkedIn",
        "X (Twitter)",
        "TikTok"
    ]
)


topic = st.text_input(
    "Topic",
    placeholder="Example: Benefits of electric vehicles"
)


target_audience = st.text_input(
    "Target Audience",
    placeholder="Example: University students"
)


tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Friendly",
        "Casual",
        "Funny",
        "Inspirational",
        "Persuasive",
        "Educational"
    ]
)


# ==========================================
# GENERATE CONTENT
# ==========================================

if st.button(
    "🚀 Generate Content",
    use_container_width=True
):

    if not topic.strip():

        st.warning(
            "Please enter a topic."
        )

        st.stop()


    if not target_audience.strip():

        st.warning(
            "Please enter your target audience."
        )

        st.stop()


    prompt = f"""
You are an expert social media content writer.

Create high-quality social media content.

Content Type: {content_type}
Platform: {platform}
Topic: {topic}
Target Audience: {target_audience}
Tone: {tone}

Return exactly:

POST:
Write the complete post suitable for the selected platform.

CAPTION:
Write a short and engaging caption.

HASHTAGS:
Provide 8-12 relevant hashtags.

Requirements:

- Make the content original.
- Make it engaging.
- Match the selected platform.
- Match the target audience.
- Match the requested tone.
- Use natural language.
- Do not explain your process.
- Do not add unnecessary sections.
"""


    try:

        with st.spinner(
            "Creating your content..."
        ):

            response = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional "
                            "social media content assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.7,

                max_completion_tokens=1200
            )


        generated_content = (
            response.choices[0]
            .message
            .content
        )


        st.success(
            "Content generated successfully!"
        )


        st.markdown(
            "### 📝 Generated Content"
        )


        st.write(
            generated_content
        )


        st.download_button(

            label="⬇️ Download Content",

            data=generated_content,

            file_name="generated_content.txt",

            mime="text/plain",

            use_container_width=True
        )


    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Powered by Streamlit + Groq"
)
