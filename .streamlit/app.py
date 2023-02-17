import streamlit as st
import logging
import os
import scrape as scr
import oai

# configuring logger
logging.basicConfig(format="\n% (asctime)s - %(message)s", level=logging.INFO, force=True)

# summarize function
def summarize(text: str):
    summary_prompt = "Summarize: "
    openai = oai.Openai()
    flagged = openai.moderate(text)
    if flagged:
        st.session_state.text_error = "Text contains offensive content"
        return
    st.session_state.error = ""
    st.session_state.summary = (
        openai.complete(prompt=text + summary_prompt).replace("\n", " ")
    )

st.set_page_config(page_title="Text Summarizer", page_icon=":newspaper:")
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "error" not in st.session_state:
    st.session_state.error = ""

st.title("Text Summarizer")

selectbox = st.selectbox("Raw text or URL", ["Raw text", "URL"])
if selectbox == "Raw text":
    text = st.text_area("Enter text here", height=300)
    if text:
        summarize(text)
        if st.session_state.summary:
            st.text_area("Summary", st.session_state.summary, height=300)
            logging.info("Summary generated")
            st.button(
                label="Regenerate summary",
                # type = "secondary",
                on_click=summarize,
                args=[text],
            )

elif selectbox == "URL":
    url = st.text_input("Enter URL here")
    if url:
        scraper = scr.Scraper()
        response = scraper.request_url(url)
        if "invalid" in str(response).lower():
            st.error(str(response))
        elif response.status_code != 200:
            st.error(f"Response status {response.status_code}")
        else:
            url_text = (
                scraper.extract_content(response)[:6000].strip().replace("\n", " ")
            )
            summarize(url_text)
            if st.session_state.summary:
                st.text_area(
                    label="URL summary", value=st.session_state.summary, height=100
                )
                logging.info(f"URL: {url}\nSummary: {st.session_state.summary}")
                # Force responsive layout for columns also on mobile
                st.write(
                    """<style>
                    [data-testid="column"] {
                        width: calc(50% - 1rem);
                        flex: 1 1 calc(50% - 1rem);
                        min-width: calc(50% - 1rem);
                    }
                    </style>""",
                    unsafe_allow_html=True,
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.components.v1.html(
                        f"""
                            <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{st.session_state.summary}\n- Summary generated via web-summarizer.streamlit.app of" data-url="{url}" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        height=45,
                    )
                with col2:
                    st.button(
                        label="Regenerate summary",
                        type="secondary",
                        on_click=summarize,
                        args=[url_text],
                    )
        