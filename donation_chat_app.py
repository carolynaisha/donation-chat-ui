import streamlit as st
from datetime import datetime
from simple_salesforce import Salesforce

# --- Salesforce setup (secure with Streamlit secrets) ---
def connect_to_salesforce():
    return Salesforce(
        username=st.secrets["SF_USERNAME"],
        password=st.secrets["SF_PASSWORD"],
        security_token=st.secrets["SF_TOKEN"],
        domain="login"
    )

def save_donation_to_salesforce(sf, donor_data):
    contact = sf.Contact.create({
        'FirstName': donor_data['first_name'],
        'LastName': donor_data['last_name'],
        'Email': donor_data['email'],
        'MailingStreet': donor_data['address'],
        'Salutation': donor_data['title']
    })

    opportunity = sf.Opportunity.create({
        'Name': f"Donation from {donor_data['first_name']} {donor_data['last_name']}",
        'Amount': float(donor_data['amount']),
        'CloseDate': datetime.today().strftime('%Y-%m-%d'),
        'StageName': "Received",
        'Type': "Donation",
        'ContactId': contact['id'],
        'Description': donor_data.get('dedication', ''),
    })
    return contact, opportunity

# --- UI Setup ---
st.set_page_config(page_title="Donate Chat", layout="centered")
st.title("👋 Hey there! Let’s get your donation started.")

# Global trust message
st.markdown("🔒 _Your info is secure and encrypted. We never share it._")

TOTAL_STEPS = 10
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.donor_data = {}

# Progress bar
progress = (st.session_state.step - 1) / TOTAL_STEPS
st.progress(progress)

# --- Chat Flow ---

if st.session_state.step == 1:
    st.markdown("💰 **How much would you like to chip in today?** 🔒")
    amount = st.text_input("Just pop in a number (e.g. 25)")
    if st.button("Cool, next!"):
        st.session_state.donor_data['amount'] = amount
        st.session_state.step += 1

elif st.session_state.step == 2:
    dedication = st.text_input("📝 Is this in honour of someone? Maybe a friend or loved one?")
    st.session_state.donor_data['dedication'] = dedication
    if st.button("Got it"):
        st.session_state.step += 1

elif st.session_state.step == 3:
    choice = st.radio("✨ Want to let us use your gift where it’s needed most?", ["Yes, go for it", "I'd like to choose"])
    if choice == "Yes, go for it":
        st.session_state.donor_data['appeal'] = "Where most needed"
    else:
        appeal = st.selectbox("🎯 Choose something you care about", [
            "Emergency Relief", "Children’s Education", "Climate Help", "Health Access"
        ])
        st.session_state.donor_data['appeal'] = appeal
    if st.button("Next up"):
        st.session_state.step += 1

elif st.session_state.step == 4:
    info = st.radio("💡 Curious how your donation gets used?", ["Yeah, tell me", "Nah, I'm good"])
    if info == "Yeah, tell me":
        st.info("Out of every £1: 84p helps people directly, 11p spreads the word, 5p keeps the lights on.")
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 5:
    case = st.radio("📖 Want to hear a quick story about someone you’re helping?", ["Sure", "Skip it"])
    if case == "Sure":
        st.success("Fatima’s home was flooded. Your donations helped her rebuild with clean water and shelter.")
    if st.button("Keep going"):
        st.session_state.step += 1

elif st.session_state.step == 6:
    monthly = st.radio("🔁 Would you consider giving monthly? It helps us plan ahead!", ["Yes, happy to", "Just this once"])
    if monthly == "Yes, happy to":
        amount = st.text_input("New monthly amount (£)", value=st.session_state.donor_data['amount'])
        st.session_state.donor_data['amount'] = amount
        st.session_state.donor_data['recurring'] = True
    else:
        st.session_state.donor_data['recurring'] = False
    if st.button("Let’s do it"):
        st.session_state.step += 1

elif st.session_state.step == 7:
    method = st.selectbox("💳 How would you like to pay?", [
        "Credit/Debit Card", "PayPal", "Apple Pay", "Bank Transfer"
    ])
    st.session_state.donor_data['payment_method'] = method
    if st.button("Next step"):
        st.session_state.step += 1

elif st.session_state.step == 8:
    title = st.selectbox("🙋 What should we call you?", ["Mr", "Ms", "Mrs", "Dr", "Mx", "Other"])
    first_name = st.text_input("Your first name?")
    last_name = st.text_input("Your last name?")
    st.markdown("📧 **Your email** 🔒 _(Just for receipts)_")
    email = st.text_input("you@example.com")
    st.markdown("🏡 **Where can we send a thank-you?** 🛡️")
    address = st.text_area("Street address, city, postcode")
    st.session_state.donor_data.update({
        'title': title,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'address': address
    })
    if st.button("Almost there!"):
        st.session_state.step += 1

elif st.session_state.step == 9:
    gift_aid = st.radio("🎁 UK taxpayer? Add Gift Aid so we get 25% more (for free!)", ["Yes please", "No thanks"])
    st.session_state.donor_data['gift_aid'] = gift_aid == "Yes please"
    if st.button("Send my donation"):
        try:
            sf = connect_to_salesforce()
            save_donation_to_salesforce(sf, st.session_state.donor_data)
            st.session_state.step += 1
        except Exception as e:
            st.error(f"Oops! Something went wrong saving to Salesforce: {e}")

elif st.session_state.step == 10:
    donor = st.session_state.donor_data
    st.success(f"🎉 Huge thanks, {donor['first_name']}! You’ve just donated £{donor['amount']}.")
    if donor['gift_aid']:
        st.info("And we’ll claim Gift Aid too – that’s 25% extra impact!")
    st.balloons()
