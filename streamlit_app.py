import streamlit as st
from PIL import Image

# Dictionary of known ingredients for allergen simulation
known_ingredients = {
    "nuts": ["peanut", "almond", "walnut"],
    "dairy": ["milk", "cheese", "butter"],
    "gluten": ["wheat", "barley", "rye"],
    "seafood": ["shrimp", "fish", "crab"]
}

# Initialize session state for allergy selection tracking
if "allergies_selected" not in st.session_state:
    st.session_state["allergies_selected"] = False
    st.session_state["user_allergies"] = []

st.sidebar.markdown("# Allergy Assistant 🤧")

# Display allergy selection dialog upon opening the app
@st.dialog("Select Your Allergies")
def select_allergies():
    user_allergies = st.multiselect(
        "Choose your allergies:",
        options=list(known_ingredients.keys()),
        help="Select from known allergen groups."
    )
    if st.button("Confirm Allergies"):
        if user_allergies:
            st.session_state["allergies_selected"] = True
            st.session_state["user_allergies"] = user_allergies
            st.rerun()
        else:
            st.warning("Please select at least one allergy to continue.")

# Only show main application if allergies are confirmed
if st.session_state["allergies_selected"]:
    # Main application interface
    with st.container(height=None, border=True):
        st.write("Registered allergies:", ", ".join(st.session_state["user_allergies"]))

        # Section for combined media upload, text input, and camera capture
        st.header("Upload Media or Take a Picture for Allergen Analysis")
        file_type = st.radio("Choose the type of media:", ["Image", "Video", "Text", "Camera"])

        # Simulated allergen identification function
        def identify_allergens(content, allergies):
            allergens_found = []
            for allergy in allergies:
                for ingredient in known_ingredients[allergy]:
                    if ingredient in content.lower():
                        allergens_found.append(ingredient)
            return allergens_found

        if file_type == "Image":
            uploaded_file = st.file_uploader("Upload an image of the food", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                ingredients_text = "milk, peanut, shrimp, wheat"
                allergens_found = identify_allergens(ingredients_text, st.session_state["user_allergies"])
                if allergens_found:
                    st.warning("Potential allergenic ingredients identified: " + ", ".join(allergens_found))
                else:
                    st.success("No allergenic ingredients identified.")

        elif file_type == "Video":
            uploaded_file = st.file_uploader("Upload a video of the food", type=["mp4", "mov"])
            if uploaded_file:
                st.video(uploaded_file)
                ingredients_text = "milk, peanut, shrimp, wheat"
                allergens_found = identify_allergens(ingredients_text, st.session_state["user_allergies"])
                if allergens_found:
                    st.warning("Potential allergenic ingredients identified: " + ", ".join(allergens_found))
                else:
                    st.success("No allergenic ingredients identified.")

        elif file_type == "Text":
            ingredients_text = st.text_area("Enter or paste the list of ingredients")
            if ingredients_text:
                allergens_found = identify_allergens(ingredients_text, st.session_state["user_allergies"])
                if allergens_found:
                    st.warning("Potential allergenic ingredients identified: " + ", ".join(allergens_found))
                else:
                    st.success("No allergenic ingredients identified.")

        elif file_type == "Camera":
            enable = st.checkbox("Enable camera")
            img_file_buffer = st.camera_input("Take a picture", disabled=not enable)
            if img_file_buffer is not None:
                image = Image.open(img_file_buffer)
                st.image(image, caption="Captured Image", use_column_width=True)
                ingredients_text = "milk, peanut, shrimp, wheat"  # Example of simulated OCR result
                allergens_found = identify_allergens(ingredients_text, st.session_state["user_allergies"])
                if allergens_found:
                    st.warning("Potential allergenic ingredients identified: " + ", ".join(allergens_found))
                else:
                    st.success("No allergenic ingredients identified.")

# Show allergy selection dialog on first load
if not st.session_state["allergies_selected"]:
    st.markdown("# Configure with your preferences")
    if st.button("Choose my allergies"):
        select_allergies()