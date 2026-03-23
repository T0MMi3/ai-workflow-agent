import streamlit as st
import requests

st.set_page_config(page_title="Clinical Workflow Engine", page_icon="🏥")

st.title("Clinical Workflow Engine")
st.write("Submit healthcare-related text to test the clinical workflow routing system.")

user_input = st.text_area(
    "Enter a healthcare workflow request",
    placeholder="Example: Claim denied due to missing prior authorization for MRI procedure. Please review and resubmit.",
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

                if data["workflow"] == "fallback_pipeline":
                    st.error(data["result"])
                else:
                    result = data["result"]

                    st.success("Classification complete")

                    st.subheader("Results")

                    st.write(f"**Category:** {result['category']}")
                    st.write(f"**Priority:** {result['priority']}")
                    st.write(f"**Recommended Action:** {result['recommended_action']}")

                    st.divider()

                    with st.expander("View Raw Response"):
                        st.json(data)

            else:
                st.error(f"Request failed with status code {response.status_code}")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server. Make sure it is running.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

st.divider()

st.subheader("Example Inputs")

st.code("Claim denied due to missing prior authorization for MRI procedure.")
st.code("Patient chart missing provider signature and incomplete documentation.")
st.code("Procedure code does not match diagnosis in chart.")
st.code("Patient billed twice and balance is incorrect.")
st.code("Portal login failing and document upload not working.")