import streamlit as st
from datetime import datetime
from simple_salesforce import Salesforce

# Salesforce setup (replace with st.secrets in production)
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

# UI logic
st.set_page_config(page_title="Donate", layout="centered")
st.title("💖 Start Your Donation")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.donor_data = {}

if st.session_state.step == 1:
    amount = st.text_input("How much would you like to donate today? (£)")
    if st.button("Next"):
        st.session_state.donor_data['amount'] = amount
        st.session_state.step += 1

elif st.session_state.step == 2:
    dedication = st.text_input("Is this a dedication or in memory of someone? (Leave blank to skip)")
    st.session_state.donor_data['dedication'] = dedication
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 3:
    where_needed = st.radio("Would you like to donate where most needed?", ["Yes", "No"])
    if where_needed == "Yes":
        st.session_state.donor_data['appeal'] = "Where most needed"
    else:
        appeal = st.selectbox("Choose a specific appeal", [
            "Emergency Relief Fund",
            "Children’s Education",
            "Climate Resilience",
            "Healthcare Access"
        ])
        st.session_state.donor_data['appeal'] = appeal
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 4:
    if st.radio("Would you like to know how your donation is used?", ["Yes", "No"]) == "Yes":
        st.info("84p to programmes, 11p to fundraising, 5p to admin.")
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 5:
    if st.radio("Would you like to read a case study?", ["Yes", "No"]) == "Yes":
        st.success("Fatima's family rebuilt after floods with your support.")
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 6:
    if st.radio("Would you like to make this monthly?", ["Yes", "No"]) == "Yes":
        amount = st.text_input("New monthly amount (£)", value=st.session_state.donor_data['amount'])
        st.session_state.donor_data['amount'] = amount
        st.session_state.donor_data['recurring'] = True
    else:
        st.session_state.donor_data['recurring'] = False
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 7:
    method = st.selectbox("Choose a payment method", [
        "Credit/Debit Card", "PayPal", "Apple Pay", "Bank Transfer"
    ])
    st.session_state.donor_data['payment_method'] = method
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 8:
    title = st.selectbox("Title", ["Mr", "Ms", "Mrs", "Dr", "Mx", "Other"])
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    address = st.text_area("Postal Address")
    st.session_state.donor_data.update({
        'title': title,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'address': address
    })
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 9:
    gift_aid = st.radio("Would you like to add Gift Aid?", ["Yes", "No"])
    st.session_state.donor_data['gift_aid'] = gift_aid == "Yes"
    if st.button("Submit Donation"):
        try:
            sf = connect_to_salesforce()
            save_donation_to_salesforce(sf, st.session_state.donor_data)
            st.session_state.step += 1
        except Exception as e:
            st.error(f"Salesforce error: {e}")

elif st.session_state.step == 10:
    donor = st.session_state.donor_data
    st.success(f"🎉 Thank you, {donor['title']} {donor['last_name']}! Your donation of £{donor['amount']} has been received.")
    if donor['gift_aid']:
        st.info("✔️ Gift Aid added. Your impact just grew by 25%!")
    st.balloons()
