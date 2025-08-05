import streamlit as st
from datetime import datetime
from simple_salesforce import Salesforce

# --- Salesforce setup using secrets ---
def connect_to_salesforce():
    return Salesforce(
        username=st.secrets["SF_USERNAME"],
        password=st.secrets["SF_PASSWORD"],
        security_token=st.secrets["SF_TOKEN"],
        domain="login"
    )

def save_to_sf(sf, data):
    contact = sf.Contact.create({
        'FirstName': data['first_name'],
        'LastName': data['last_name'],
        'Email': data['email'],
        'MailingStreet': data['address'],
        'Salutation': data['title']
    })
    opp = sf.Opportunity.create({
        'Name': f"Donation – {data['first_name']} {data['last_name']}",
        'Amount': float(data['amount']),
        'CloseDate': datetime.today().strftime('%Y-%m-%d'),
        'StageName': 'Received',
        'Type': 'Donation',
        'ContactId': contact['id'],
        'Description': data.get('dedication', ''),
    })
    return contact, opp

st.set_page_config(page_title="Donate Chat", layout="centered")
st.title("👋 Hey there! Let's get started")

st.markdown("🔒 _Your info is safe & encrypted. We never share it._")

TOTAL = 12
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.data = {}

st.progress((st.session_state.step -1) / TOTAL)

if st.session_state.step == 1:
    st.markdown("💰 **How much would you like to chip in today?** 🔒")
    amt = st.text_input("Pop in a number, e.g. 25")
    if st.button("Next"):
        st.session_state.data['amount'] = amt
        st.session_state.step += 1

elif st.session_state.step == 2:
    ded = st.text_input("📝 Is this in honour of someone or in memory of someone?")
    st.session_state.data['dedication'] = ded
    if st.button("Got it"):
        st.session_state.step += 1

elif st.session_state.step == 3:
    st.markdown("📦 **Why unrestricted donations matter**")
    st.caption("Unrestricted gifts give charities flexibility to respond to emergencies, cover everyday core needs, and invest in staff and equipment as needed. They’re vital for sustainability and resilience. :contentReference[oaicite:8]{index=8}")
    choose = st.radio("Do you want your donation to be unrestricted (where it's needed most)?", ["Yes, please", "No, I'd like to pick"])
    if choose == "Yes, please":
        st.session_state.data['appeal'] = "Where most needed"
    else:
        appeal = st.selectbox("🎯 Which area would you like to support?", [
            "Emergency Relief", "Children’s Education", "Climate Work", "Health Access"
        ])
        st.session_state.data['appeal'] = appeal
    if st.button("Next up"):
        st.session_state.step += 1

elif st.session_state.step == 4:
    see = st.radio("💡 Want to see how your donation might be used?", ["Yes, show me", "No thanks"])
    st.session_state.data['see_usage'] = (see == "Yes, show me")
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 5:
    if st.session_state.data.get('see_usage'):
        st.info("For every £1 donated: 84p for programmes, 11p for fundraising, 5p for admin and management.")
    if st.button("Cool, next"):
        st.session_state.step += 1

elif st.session_state.step == 6:
    see = st.radio("📖 Want to hear a real-life story of someone helped?", ["Yes, please", "No thanks"])
    st.session_state.data['see_story'] = (see == "Yes, please")
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 7:
    if st.session_state.data.get('see_story'):
        st.image(st.session_state.get('story_img') or 
                 "https://via.placeholder.com/400", caption="A beneficiary helped by your donation")
        st.markdown("### Emma’s Journey\n**Emma**, aged 9, lives in a region that was hit by flooding. Thanks to unrestricted funding, the charity responded immediately with clean water, shelter and schooling. Within days, Emma was back in class. Today she dreams of becoming a teacher. Your gift made that possible.")
        # image preloaded from web search; using placeholder; would set story_img from image_query
    if st.button("Moving on"):
        st.session_state.step += 1

elif st.session_state.step == 8:
    monthly = st.radio("🔁 Fancy giving monthly? It helps charities plan ahead and costs them less to process.", ["Yes, happy to", "Just this once"])
    st.session_state.data['recurring'] = (monthly == "Yes, happy to")
    if st.session_state.data['recurring']:
        st.caption("Monthly donations increase lifetime value, reduce admin costs, and deepen impact. :contentReference[oaicite:9]{index=9}")
        new = st.text_input("Enter your monthly amount (£)", value=st.session_state.data['amount'])
        st.session_state.data['amount'] = new
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 9:
    method = st.selectbox("💳 How would you like to pay?", ["Credit/Debit Card", "PayPal", "Apple Pay", "Bank Transfer"])
    st.session_state.data['payment'] = method
    if st.button("Next"):
        st.session_state.step += 1

elif st.session_state.step == 10:
    title = st.selectbox("🙋 What should we call you?", ["Mr","Ms","Dr","Mx","Other"])
    fn = st.text_input("First name")
    ln = st.text_input("Last name")
    st.markdown("📧 **Your email** 🔒 (we’ll send a receipt)")
    email = st.text_input("you@example.com")
    st.markdown("🏡 **Your address** 🛡️ (needed for Gift Aid or thank‑you letters)")
    addr = st.text_area("Street, city, postcode")
    st.session_state.data.update({'title': title, 'first_name': fn, 'last_name': ln, 'email': email, 'address': addr})
    if st.button("Almost there"):
        st.session_state.step += 1

elif st.session_state.step == 11:
    gift = st.radio("🎁 UK taxpayer? Add Gift Aid so we get 25% more at no cost to you!", ["Yes please", "No thanks"])
    st.session_state.data['gift_aid'] = (gift == "Yes please")
    if st.button("Submit donation"):
        try:
            sf = connect_to_salesforce()
            save_to_sf(sf, st.session_state.data)
            st.session_state.step += 1
        except Exception as e:
            st.error(f"Could not save – {e}")

elif st.session_state.step == 12:
    d = st.session_state.data
    st.success(f"🎉 Thanks, {d['first_name']}! Here’s what you chose:")
    st.write(f"- **Amount**: £{d['amount']} {'monthly' if d['recurring'] else 'one‑off'}")
    st.write(f"- **Dedication**: {d.get('dedication') or 'None'}")
    st.write(f"- **Support area**: {d['appeal']}")
    if d.get('see_usage'): st.write("- You opted to **view how we spend donations**")
    if d.get('see_story'): st.write("- You opted to **read Emma’s story**")
    st.write(f"- **Payment method**: {d['payment']}")
    if d['gift_aid']: st.write("- **Gift Aid** added (UK tax boost!)")
    st.write(f"- **Name & address**: {d['title']} {d['first_name']} {d['last_name']}, {d['address']}")
    st.markdown("Need to make a change? Just get in touch at **hello@examplecharity.org.uk** and we'll sort it out.")
    st.balloons()

