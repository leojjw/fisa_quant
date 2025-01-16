import streamlit as st
import streamlit_authenticator as stauth
import inspect

import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'*{st.session_state["name"]}*님 환영합니다')
    st.title('기타 내용')
elif st.session_state['authentication_status'] is False:
    st.error('아이디 또는 비밀번호가 올바르지 않습니다.')
elif st.session_state['authentication_status'] is None:
    st.warning('아이디 및 비밀번호를 입력하세요')

try:
    email_of_registered_user, \
    username_of_registered_user, \
    name_of_registered_user = authenticator.register_user()
    if email_of_registered_user:
        st.success('회원가입 완료')
except Exception as e:
    st.error(e)

# config['credentials']['usernames']['joojungwoo']['password'] = '1234'
# stauth.Hasher.hash_passwords(config['credentials'])

with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
