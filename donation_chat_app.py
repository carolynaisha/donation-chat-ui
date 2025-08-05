import streamlit as st

st.set_page_config(page_title="Secure Donation", layout="centered")
st.markdown("<h1 style='text-align: center;'>🛡️ Secure Donation</h1>", unsafe_allow_html=True)
st.caption("Thank you for supporting us today. Let’s get started.")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.data = {}

TOTAL = 7
st.progress((st.session_state.step - 1) / TOTAL)

# Step 1 – Unrestricted or Specific appeal
if st.session_state.step == 1:
    st.subheader("📦 Where would you like your donation to go?")
    st.write("Unrestricted donations help us respond faster, cover core costs and plan ahead. Or choose a specific programme you'd like to support.")
    fund_choice = st.radio("", ["💡 Where it's needed most (Unrestricted)", "🎯 I’d like to support a specific area"])
    if "Unrestricted" in fund_choice:
        st.session_state.data["appeal"] = "Unrestricted"
    else:
        area = st.selectbox("Choose your preferred area:", [
            "Emergency Relief", "Children’s Education", "Climate Resilience", "Healthcare Access"
        ])
        st.session_state.data["appeal"] = area
    if st.button("Next"):
        st.session_state.step = 2
    st.divider()

# Step 2 – Donation amount
elif st.session_state.step == 2:
    st.subheader("💰 How much would you like to donate?")
    amt = st.text_input("Donation amount in £", placeholder="e.g. 25")
    if st.button("Next"):
        st.session_state.data['amount'] = amt
        st.session_state.step = 3
    st.divider()

# Step 3 – Monthly option
elif st.session_state.step == 3:
    st.subheader("🔁 Would you consider donating monthly?")
    st.info("Monthly gifts give charities reliable income, lower costs, and allow us to plan for long-term impact.")
    monthly = st.radio("Choose one:", ["✅ Yes, I'd like to give monthly", "➡️ No, just this once"])
    st.session_state.data['recurring'] = monthly.startswith("✅")
    if st.session_state.data['recurring']:
        new = st.text_input("Monthly amount (£)", value=st.session_state.data['amount'])
        st.session_state.data['amount'] = new
    if st.button("Continue"):
        st.session_state.step = 4
    st.divider()

# Step 4 – Learn more or continue
elif st.session_state.step == 4:
    st.subheader("📚 Want to know more before you give?")
    see = st.radio("Would you like to understand how your donation is used?", ["📘 Yes, tell me more", "🚀 No thanks, ready to donate"])
    if st.button("Continue"):
        st.session_state.step = 5 if see.startswith("📘") else 6
    st.divider()

# Step 5 – Info + case study
elif st.session_state.step == 5:
    st.subheader("💡 Where your money goes")
    st.success("For every £1: 84p goes directly to programmes, 11p helps raise more funds, 5p covers admin.")

    st.subheader("📖 Emma’s Story")
    st.image("https://tse4.mm.bing.net/th/id/OIP.yceXI1tj7ZcWxo9np34YngHaE8?pid=Api", caption="Emma received support after a flood")
    st.markdown("""
**Emma’s Journey**  
Emma, age 9, lived in a region devastated by floods.  
Thanks to unrestricted funds, our team responded immediately—with clean water, food, shelter, and access to school.  
Within a week, Emma was back in class and smiling again.  
**Your donation makes this possible.**
""")
    if st.button("I'm ready to donate"):
        st.session_state.step = 6
    st.divider()

# Step 6 – Donor form
elif st.session_state.step == 6:
    st.subheader("🙋 A few details before you donate")

    col1, col2 = st.columns(2)
    fn = col1.text_input("First name")
    ln = col2.text_input("Last name")

    payment = st.selectbox("💳 How would you like to pay?", ["Credit/Debit Card", "PayPal", "Bank Transfer"])

    email = st.text_input("📧 Email (for your receipt)")
    addr = st.text_area("🏠 Address (for thank you letter or Gift Aid)")

    st.session_state.data.update({
        'first_name': fn,
        'last_name': ln,
        'payment': payment,
        'email': email,
        'address': addr
    })
    if st.button("Submit donation"):
        st.session_state.step = 7
    st.divider()

# Step 7 – Thank you page
elif st.session_state.step == 7:
    d = st.session_state.data
    st.markdown(f"""
### 🎉 Thank you, {d['first_name']}!

Here’s a summary of your donation:
- 💷 **Amount**: £{d['amount']} ({'Monthly' if d['recurring'] else 'One-off'})
- 🎯 **Programme**: {d['appeal']}
- 💳 **Payment method**: {d['payment']}
- 🧾 **Email**: {d['email']}
- 🏠 **Name & Address**: {d['first_name']} {d['last_name']}, {d['address']}
""")
    st.info("Need to make a change? Email us at **hello@examplecharity.org.uk** and we’ll sort it out.")
    st.balloons()




