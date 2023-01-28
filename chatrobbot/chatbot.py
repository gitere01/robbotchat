import openai
import streamlit as st

# Add a privacy policy link
st.markdown("By using this website, you agree to our [Privacy Policy](https://yourwebsite.com/privacy).")

# Add Adsense code to head
adsense_code = '''
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
  (adsbygoogle = window.adsbygoogle || []).push({
    google_ad_client: "ca-pub-6750087449030029",
    enable_page_level_ads: true
  });
</script>
'''
st.markdown(adsense_code, unsafe_allow_html=True)

# Add a stylesheet
st.markdown(
    """
    <style>
        .message {{
            color: blue;
            font-size: 18px;
            background-color: lightgray;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

openai.api_key = st.secrets["api_secret"]

def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message_text = completions.choices[0].text
    return message_text

st.title("Chatbot")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []  
    
def get_text():
    input_text = st.text_input("You:", "Hello, how are you,you can ask any question which is in your mind? and i will answer", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"])-1, -1, -1):
        st.markdown("<div class='message'>{}</div>".format(st.session_state["generated"][i]),unsafe_allow_html=True, key=str(i))
        st.markdown("<div class='message'>{}</div>".format(st.session_state['past'][i]),unsafe_allow_html=True, key=str(i)+'_user')
