import streamlit as st
from content_api import get_post_ideas
from send_to_slack import send_post_to_slack


def main():
    st.title("Law Firm Social Media Post Generator")
    st.write("This tool generates 3-4 post ideas based on firm details.")
    niche = st.selectbox("Select a legal niche", ["Corporate Law", "Family Law", "Criminal Law", "Intellectual Property", "Immigration Law", "Real Estate Law", "Tax Law"])
    
    if st.button("Generate Posts"):
        with st.spinner("Generating post ideas..."):
            posts = get_post_ideas(niche)
            for i, post in enumerate(posts, 1):
                st.write(f"{post}")

            # Combine posts into a single message, e.g., as a numbered list
            slack_message = "\n\n".join([f"{post}" for i, post in enumerate(posts, 1)])
            success = send_post_to_slack(slack_message)
            if success:
                st.success("Posts sent to Slack!")
            else:
                st.error("Failed to send posts to Slack.")

if __name__ == "__main__":
    main()