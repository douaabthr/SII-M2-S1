# Import the page source files
import pages.Visualisation,pages.Training,pages.Testing

import streamlit as st

st.set_page_config(layout="wide")

# Define the pages using st.Page
pages = [
    st.Page("main_app.py", title="Home"),  # removed icon
    st.Page(pages.Visualisation, title="1. Visualisation",icon="🌸"),  # removed icon
    st.Page(pages.Training, title="2. Training",icon="🌸"),  # removed icon
    st.Page(pages.Testing, title="3. Testing",icon="🌸"),  


    
]

# Set up the navigation and run the current page
pg = st.navigation(pages)  # default position is sidebar

# Elements placed here will appear on all pages
st.sidebar.markdown("---")


# Run the selected page content
pg.run()
