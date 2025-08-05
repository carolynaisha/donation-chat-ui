import streamlit as st

st.set_page_config(page_title="Secure Donation", layout="centered")
st.title("Secure Donation")
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
    st.subheader("Donation amount")
    amt = st.text_input("Please enter your donation amount in GBP", key="donation_amount")
    if st.button("Next: Monthly option"):
        st.session_state.data['amount'] = amt
        st.session_state.step = 3
    st.divider()

# Step 3 – Monthly option
elif st.session_state.step == 3:
    st.subheader("Would you consider donating monthly?")
    st.info("Monthly gifts provide stable funding, reduce admin costs, and increase long-term impact.")
    monthly = st.radio(
        "Would you like to make this a monthly donation?",
        ["Yes", "No"],
        key="monthly_option"
    )
    st.session_state.data['recurring'] = (monthly == "Yes")
    if st.session_state.data['recurring']:
        new = st.text_input("Enter your monthly amount in GBP", value=st.session_state.data['amount'], key="monthly_amount")
        st.session_state.data['amount'] = new
    if st.button("Continue"):
        st.session_state.step = 4
    st.divider()

# Step 4 – Learn more or continue
elif st.session_state.step == 4:
    st.subheader("Would you like to know more?")
    see = st.radio(
        "Do you want to learn how your donation is spent before continuing?",
        ["Yes", "No, I'm ready to donate"],
        key="learn_more"
    )
    if st.button("Continue to next step"):
        st.session_state.step = 5 if see == "Yes" else 6
    st.divider()

# Step 5 – Info + case study
elif st.session_state.step == 5:
    st.subheader("Where your money goes")
    st.success("For every £1: 84p goes to programmes, 11p to fundraising, 5p to admin.")

    st.subheader("Emma’s Story")
    st.image(
        "https://tse4.mm.bing.net/th/id/OIP.yceXI1tj7ZcWxo9np34YngHaE8?pid=Api",
        caption="Emma, age 9, stands with a backpack outside a rebuilt school after flood recovery.",
        use_column_width=True
    )
    st.markdown("""
Emma lived in a flood-affected region.  
Your donations helped her family access clean water, food and shelter.  
She was back in school within a week and dreaming of becoming a teacher.
    """)
    if st.button("I'm ready to donate"):
        st.session_state.step = 6
    st.divider()

# Step 6 – Donor form (with Gift Aid)
elif st.session_state.step == 6:
    st.subheader("Your details")

    col1, col2 = st.columns(2)
    fn = col1.text_input("First name", key="first_name")
    ln = col2.text_input("Last name", key="last_name")

    email = st.text_input("Email address (for receipt)", key="email")
    addr = st.text_area("Postal address (for thank-you letter or Gift Aid)", key="address")

    payment = st.selectbox("How would you like to pay?", ["Credit/Debit Card", "PayPal", "Bank Transfer"], key="payment_method")

    gift_aid = st.radio(
        "Are you a UK taxpayer? With Gift Aid, we can claim 25p for every £1 you give at no extra cost.",
        ["Yes, I want to Gift Aid this donation", "No"],
        key="gift_aid"
    )
    st.session_state.data.update({
        'first_name': fn,
        'last_name': ln,
        'payment': payment,
        'email': email,
        'address': addr,
        'gift_aid': gift_aid.startswith("Yes")
    })

    if st.button("Submit your donation"):
        st.session_state.step = 7
    st.divider()

# Step 7 – Thank you page
elif st.session_state.step == 7:
    d = st.session_state.data
    st.header("Thank you!")
    st.success(f"{d['first_name']}, your donation has been received.")
    st.markdown(f"""
**Donation Summary**  
- Amount: £{d['amount']} ({'Monthly' if d['recurring'] else 'One-off'})  
- Programme: {d['appeal']}  
- Payment method: {d['payment']}  
- Gift Aid: {"Yes" if d['gift_aid'] else "No"}  
- Name: {d['first_name']} {d['last_name']}  
- Address: {d['address']}  
- Email: {d['email']}
    """)
    st.info("If you need to change anything, email us at hello@examplecharity.org.uk.")
    st.balloons()





