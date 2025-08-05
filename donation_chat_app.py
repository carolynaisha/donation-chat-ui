import streamlit as st
import random

# ---------- Setup ----------
st.set_page_config(page_title="Secure Donation", layout="centered")
st.markdown("<h1 style='text-align: center;'>🛡️ Secure Donation</h1>", unsafe_allow_html=True)
st.caption("Thank you for supporting us today. Let’s get started.")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.data = {}
    st.session_state.step_history = []
    st.session_state.ab_test_group = random.choice(["emotional", "logical"])
    st.session_state.is_returning_donor = False  # flag will flip later

TOTAL = 7
st.progress((st.session_state.step - 1) / TOTAL)
st.markdown(f"**Step {st.session_state.step} of {TOTAL}**")

# ---------- Back Button ----------
def back():
    if st.session_state.step_history:
        st.session_state.step = st.session_state.step_history.pop()

# ---------- Live social proof ----------
donor_count = 1243 + random.randint(0, 50)
st.markdown(f"👥 Join **{donor_count:,} donors** who gave this week!")

# ---------- Quick Donate Shortcut ----------
if st.session_state.step == 1 and not st.session_state.is_returning_donor:
    email_check = st.text_input("If you've donated before, enter your email to skip ahead (optional):")
    if email_check.lower() in ["aisha@example.com", "j.smith@example.org"]:
        st.session_state.is_returning_donor = True
        st.session_state.data["email"] = email_check
        st.session_state.data["amount"] = "20"
        st.session_state.data["recurring"] = True
        st.session_state.data["appeal"] = "Unrestricted"
        st.session_state.step = 6
        st.stop()

# ---------- Step 1 ----------
if st.session_state.step == 1:
    st.subheader("Where would you like your donation to go?")
    fund_choice = st.radio("Donation direction", ["Where it's needed most (Unrestricted)", "Choose a specific programme"])
    if "Unrestricted" in fund_choice:
        st.session_state.data["appeal"] = "Unrestricted"
    else:
        area = st.selectbox("Choose your preferred area:", [
            "Emergency Relief", "Children’s Education", "Climate Resilience", "Healthcare Access"
        ])
        st.session_state.data["appeal"] = area
    if st.button("Next"):
        st.session_state.step_history.append(1)
        st.session_state.step = 2

# ---------- Step 2 ----------
elif st.session_state.step == 2:
    st.subheader("How much would you like to donate?")
    amt = st.text_input("Donation amount (£)", key="donation_amount")
    error = False
    if st.button("Next"):
        try:
            amount_float = float(amt)
            if amount_float <= 0:
                raise ValueError
            st.session_state.data['amount'] = amt
            st.session_state.step_history.append(2)
            st.session_state.step = 3
        except:
            st.error("Please enter a valid positive amount.")
            error = True
    if st.button("Back"):
        back()

# ---------- Step 3 ----------
elif st.session_state.step == 3:
    st.subheader("Would you consider donating monthly?")
    monthly = st.radio("Make this a monthly donation?", ["Yes", "No"])
    st.session_state.data['recurring'] = (monthly == "Yes")
    if st.session_state.data['recurring']:
        amt = st.text_input("Monthly donation amount (£)", value=st.session_state.data['amount'])
        st.session_state.data['amount'] = amt
    if st.button("Next"):
        st.session_state.step_history.append(3)
        st.session_state.step = 4
    if st.button("Back"):
        back()

# ---------- Step 4 ----------
elif st.session_state.step == 4:
    st.subheader("Would you like to learn how your donation is used?")
    learn = st.radio("Choose an option", ["Yes, tell me more", "No, I’m ready to donate"])
    if st.button("Continue"):
        st.session_state.step_history.append(4)
        st.session_state.step = 5 if learn.startswith("Yes") else 6
    if st.button("Back"):
        back()
# ---------- Step 5 ----------
elif st.session_state.step == 5:
    group = st.session_state.ab_test_group
    st.subheader("How your donation helps")

    if group == "emotional":
        st.success("84p of every £1 goes to programmes, 11p to fundraising, and 5p to admin.")
        st.markdown("#### Emma’s Story")
        st.image(
            "https://tse4.mm.bing.net/th/id/OIP.yceXI1tj7ZcWxo9np34YngHaE8?pid=Api",
            caption="Emma stands with a backpack outside a rebuilt school after flooding.",
            use_column_width=True
        )
        st.write("""
Emma, age 9, lived in a region devastated by floods.  
Your donation helped her return to school within a week — with clean water, food, and books.  
She now dreams of becoming a teacher. Your support made that possible.
""")
    else:  # logical group
        st.info("84% of your donation directly supports programme delivery. 11% helps us reach more donors.5% supports governance and overheads.")
        st.markdown("#### Why unrestricted donations matter")
        st.write("""
They help us:
- Respond immediately to emergencies  
- Invest in staff and infrastructure  
- Support multiple regions fairly  
Unrestricted funding allows us to prioritise based on greatest impact.
""")
    if st.button("Continue to donate"):
        st.session_state.step_history.append(5)
        st.session_state.step = 6
    if st.button("Back"):
        back()

# ---------- Step 6 ----------
elif st.session_state.step == 6:
    st.subheader("Tell us a bit about you")

    col1, col2 = st.columns(2)
    fn = col1.text_input("First name")
    ln = col2.text_input("Last name")

    email = st.text_input("Email address")
    addr = st.text_area("Postal address")

    payment = st.selectbox("Payment method", ["Credit/Debit Card", "PayPal", "Bank Transfer"])

    gift_aid = st.radio(
        "Are you a UK taxpayer?",
        ["Yes – add Gift Aid", "No"],
        help="With Gift Aid, we can claim 25p extra for every £1 you donate."
    )

    st.session_state.data.update({
        'first_name': fn,
        'last_name': ln,
        'email': email,
        'address': addr,
        'payment': payment,
        'gift_aid': gift_aid.startswith("Yes")
    })

    if st.button("Submit donation"):
        st.session_state.step_history.append(6)
        st.session_state.step = 7
    if st.button("Back"):
        back()

# ---------- Step 7 ----------
elif st.session_state.step == 7:
    d = st.session_state.data
    try:
        amount = float(d['amount'])
        formatted_amount = f"£{amount:,.2f}"
    except:
        formatted_amount = f"£{d['amount']}"

    st.header("🎉 Thank you for your donation!")
    st.markdown(f"""
### Thank you {d['first_name']} for your donation of {formatted_amount}.

Your gift also helps beyond the classroom — supporting young graduates with the training and resources they need to become economically independent leaders in their communities.

Thank you for being part of the **Campaign for Female Education**.
""")

    st.markdown("---")
    st.subheader("Your donation summary")
    st.markdown(f"""
- 💷 Amount: {formatted_amount} ({'Monthly' if d['recurring'] else 'One-off'})  
- 🎯 Appeal: {d['appeal']}  
- 💳 Payment: {d['payment']}  
- 🎁 Gift Aid: {"Yes" if d['gift_aid'] else "No"}  
- 📬 Name: {d['first_name']} {d['last_name']}  
- 🏠 Address: {d['address']}  
- 📧 Email: {d['email']}
""")
    st.info("Need to make a change? Email us at **hello@campaignforfemaleducation.org**.")
    st.balloons()







