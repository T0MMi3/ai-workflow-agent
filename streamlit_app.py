import streamlit as st
import requests

st.set_page_config(page_title="AI Workflow Agent", page_icon="🤖")

st.title("AI Workflow Agent")
st.write("Submit a request to test the AI workflow routing system.")

user_input = st.text_area(
    "Enter a request",
    placeholder="Example: Classify this support ticket: I was charged twice for my premium payment.",
    height=150
)

if st.button("Process Request"):
    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/process",
                json={"text": user_input},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()

                st.success("Request processed successfully.")

                st.subheader("Intent")
                st.json({"intent": data.get("intent")})

                st.subheader("Workflow")
                st.json({"workflow": data.get("workflow")})

                st.subheader("Result")
                result = data.get("result")

                if isinstance(result, dict) or isinstance(result, list):
                    st.json(result)
                else:
                    st.code(str(result))

            else:
                st.error(f"Request failed with status code {response.status_code}")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server. Make sure it is running on http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"Unexpected error: {e}")