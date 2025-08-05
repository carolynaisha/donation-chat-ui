import streamlit as st

st.set_page_config(page_title="Secure Donation", layout="centered")
st.markdown("""
<h1 style='text-align: center;'>
🛡️ Secure Donation
</h1>
""", unsafe_allow_html=True)
st.caption("Thank you for supporting us today. Let’s get started.")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.data = {}

TOTAL = 7
st.progress((st.session_state.step - 1) / TOTAL)

# Step 1 – Unrestricted or Specific appeal
if st.session_state.step == 1:
    st.subheader("Where would you like your donation to go?")
    st.write("Unrestricted donations help us respond faster, cover core costs and plan ahead. Or choose a specific programme you'd like to support.")
    fund_choice = st.radio(
        "Donation direction",
        ["Where it's needed most (Unrestricted)", "I’d like to support a specific area"],
        key="appeal_choice"
    )
    if "Unrestricted" in fund_choice:
        st.session_state.data["appeal"] = "Unrestricted"
    else:
        area = st.selectbox(
            "Choose your preferred programme area",
            ["Emergency Relief", "Children’s Education", "Climate Resilience", "Healthcare Access"],
            key="specific_area"
        )
        st.session_state.data["appeal"] = area
    if st.button("Next: Donation amount"):
        st.session_state.step = 2
    st.divider()

# Step 2 – Donation amount
elif st.session_state.step == 2:
    st.sub






