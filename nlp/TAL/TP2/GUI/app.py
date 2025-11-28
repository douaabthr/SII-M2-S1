# Import the page source files
import pages.Articles,pages.Vocabulary,pages.Sentences,pages.Ngrams,pages.Next_Word_Prediction,pages.Sequence_Prediction
import pages.Tokens # Make sure you have this file
import streamlit as st

st.set_page_config(layout="wide")

# Define the pages using st.Page
pages = [
    st.Page("main_app.py", title="Home"),  # removed icon
    st.Page(pages.Articles, title="1. Articles",icon="🌸"),  # removed icon
    st.Page(pages.Tokens, title="2. Tokens"), 
    st.Page(pages.Vocabulary, title="3. Vocabulary"),   # removed icon
    st.Page(pages.Sentences, title="4. Sentences"), 
    st.Page(pages.Ngrams, title="5. N-grams"), 
    st.Page(pages.Ngrams, title="6. Next_Word_Prediction"), 
    st.Page(pages.Ngrams, title="7. Sequence_Prediction"), 
]

# Set up the navigation and run the current page
pg = st.navigation(pages)  # default position is sidebar

# Elements placed here will appear on all pages
st.sidebar.markdown("---")
st.sidebar.caption("App built with Streamlit")

# Run the selected page content
pg.run()
