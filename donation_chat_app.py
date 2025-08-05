import streamlit as st

st.set_page_config(page_title="Secure Donation", layout="centered")
st.title("Thank you for supporting us today. Let’s get started.")
st.markdown("🛡️ Secure Donation")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.data = {}

TOTAL = 7
st.progress((st.session_state.step - 1) / TOTAL)

# Step 1 – Unrestricted or Specific appeal
if st.session_state.step == 1:
    st.markdown("📦 **Where would you like your donation to go?**")
    fund_choice = st.radio("Choose one:", ["Where it's needed most (unrestricted)", "I’d like to support a specific area"])
    if fund_choice.startswith("Where"):
        st.session_state.data["appeal"] = "Unrestricted"
    else:
        area = st.selectbox("Select a programme:", [
            "Emergency Relief", "Children’s Education", "Climate Resilience", "Healthcare Access"
        ])
        st.session_state.data["appeal"] = area
    if st.button("Next"):
        st.session_state.step = 2

# Step 2 – Donation amount
elif st.session_state.step == 2:
    st.markdown("💰 **How much would you like to donate today?** 🔒")
    amt = st.text_input("e.g. 25")
    if st.button("Next"):
        st.session_state.data['amount'] = amt
        st.session_state.step = 3

# Step 3 – Monthly option
elif st.session_state.step == 3:
    st.markdown("🔁 **Would you consider supporting us monthly?**")
    st.caption("Monthly gifts give charities steady income, reduce admin costs, and deepen impact over time. They help plan ahead and amplify the lifetime value of your gift. " +
               "([4agoodcause.com](https://4agoodcause.com/why-monthly-giving-matters-the-impact-and-sustainability-it-brings/), [readingpartners.org](https://readingpartners.org/blog/monthly-giving-benefits-donor-cause/))")
    monthly = st.radio("Monthly donation?", ["Yes, let's do it", "No, just one-off"])
    st.session_state.data['recurring'] = monthly.startswith("Yes")
    if st.session_state.data['recurring']:
        new = st.text_input("Enter your monthly amount (£)", value=st.session_state.data['amount'])
        st.session_state.data['amount'] = new
    if st.button("Continue"):
        st.session_state.step = 4

# Step 4 – Learn more or continue
elif st.session_state.step == 4:
    see = st.radio("Would you like to learn more about how your donation is spent before continuing?", ["Yes", "No, I’m ready to donate"])
    if see == "Yes":
        st.session_state.step = 5
    else:
        st.session_state.step = 6

# Step 5 – Impact explanation + story
elif st.session_state.step == 5:
    st.info("🧾 For every £1 donated: 84p goes directly to programmes, 11p supports fundraising and awareness, 5p funds governance/admin.")
    st.markdown("📖 **Emma’s Story**")
    st.image("https://tse4.mm.bing.net/th/id/OIP.yceXI1tj7ZcWxo9np34YngHaE8?pid=Api", caption="Emma received help after flooding")
    st.write("""
**Emma’s Journey**  
Emma, age 9, lived in a region devastated by floods.  
Unrestricted charity funds meant our team responded quickly—with clean water, shelter and education support.  
Within days, Emma was back in class and dreaming big again.  
Your gift helped make that possible.
    """)
    if st.button("Continue to donate"):
        st.session_state.step = 6

# Step 6 – Donor details form
elif st.session_state.step == 6:
    st.markdown("🙋 **Please pop in your details:**")
    fn = st.text_input("First name")
    ln = st.text_input("Last name")
    payment = st.selectbox("How would you like to pay?", ["Credit/Debit Card", "PayPal", "Bank Transfer"])
    st.markdown("📧 Your email 🔒 (just for receipts)")
    email = st.text_input("you@example.com")
    st.markdown("🏡 Your address 🛡️ (for thank‑you or Gift Aid)")
    addr = st.text_area("123 Street, City, Postcode")
    st.session_state.data.update({
        'first_name': fn,
        'last_name': ln,
        'payment': payment,
        'email': email,
        'address': addr
    })
    if st.button("Submit my donation"):
        st.session_state.step = 7

# Step 7 – Thank you summary
elif st.session_state.step == 7:
    d = st.session_state.data
    st.success(f"🎉 Thank you, {d['first_name']}! Here’s what you chose:")
    st.write(f"- **Amount**: £{d['amount']} ({'monthly' if d['recurring'] else 'one-off'})")
    st.write(f"- **Donation area**: {d['appeal']}")
    st.write(f"- **Payment method**: {d['payment']}")
    st.write(f"- **Name & address**: {d['first_name']} {d['last_name']}, {d['address']}")
    st.write(f"- **Email**: {d['email']}")
    st.write(f"- **Monthly support**: {'Yes' if d['recurring'] else 'No'}")
    st.markdown("Need to make a change? Contact us at **hello@examplecharity.org.uk** and we’ll sort it out.")
    st.balloons()




