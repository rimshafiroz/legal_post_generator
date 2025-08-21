import streamlit as st
from content_api import get_post_ideas , get_firm_context
from send_to_slack import send_post_to_slack
from huggingface_api import generate_image_from_context
from img_overlay import write_text_on_image
# from predis_api import generate_predis_image
import os
import tempfile


def main():
    st.title("Law Firm Social Media Post Generator")
    st.write("This tool generates 2 unique Instagram-style post ideas with graphics based on firm details.")
    niche = st.selectbox("Select a legal niche", ["Corporate Law", "Family Law", "Criminal Law", "Intellectual Property", "Immigration Law", "Real Estate Law", "Tax Law"])
    selected_date = st.date_input("Select date (optional)")

    if st.button("Generate Posts"):
        with st.spinner("Generating post ideas and images..."):
            date_override = selected_date or None
            # Build context once so we can show the single trending headline
            context = get_firm_context(niche, date_override=date_override)
            posts = get_post_ideas(niche, num_posts=2, date_override=date_override)
            # Show trending headline (non-holiday) once above the posts
            if not context.get("is_holiday"):
                headline = context.get("trending")
                headline_url = context.get("trending_url")
                st.markdown("**Today's trending topic:**")
                if headline_url:
                    st.markdown(f"- [{headline}]({headline_url})")
                else:
                    st.markdown(f"- {headline}")
            images = []
            image_paths = []
            for i, post in enumerate(posts):
                try:
                    img = generate_image_from_context(context, post_text=post, variant_index=i)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                        image_path = write_text_on_image(
                            img,
                            post,
                            output_path=tmpfile.name,
                            is_holiday=bool(context.get("is_holiday")),
                            style_variant=i
                        )
                        image_paths.append(image_path)
                except Exception as e:
                    st.warning(f"Image generation failed for post {i+1}: {e}")
                    image_paths.append(None)
            # Display posts with images and download buttons
            for i, (post, img_path) in enumerate(zip(posts, image_paths), 1):
                st.markdown(f"### Post {i}")
                if img_path:
                    st.image(img_path, caption=f"Post idea for {niche}")
                    with open(img_path, "rb") as f:
                        st.download_button(
                            label=f"Download Post {i}",
                            data=f,
                            file_name=f"post_{i}_{niche.replace(' ', '_').lower()}.png",
                            mime="image/png"
                        )
                st.write(post)
            # Combine posts into a single message, e.g., as a numbered list
            slack_message = "\n\n".join([f"{i+1}. {post}" for i, post in enumerate(posts)])
            success = send_post_to_slack(slack_message)
            if success:
                st.success("Posts sent to Slack!")
            else:
                st.error("Failed to send posts to Slack.")

if __name__ == "__main__":
    main()
