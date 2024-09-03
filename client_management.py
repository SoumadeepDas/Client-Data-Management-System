# client_data_portal.py
import streamlit as st
import pandas as pd

# Load the dataset
file_path = 'Client - Sheet1.csv'  # Ensure the file path is correct
try:
    data = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Error loading the data: {e}")
    st.stop()

# Set the page configuration
st.set_page_config(page_title="Client Data Management Portal", layout="wide")


# Function to add a new client
def add_client(data, new_client):
    new_data = pd.concat([data, pd.DataFrame([new_client])], ignore_index=True)
    return new_data


# Sidebar Filters
st.sidebar.header("Filter Options")

# Sidebar filter options
company_name = st.sidebar.multiselect(
    "Select Company Name:", options=data['Company Name'].unique(), default=data['Company Name'].unique()
)
requirement = st.sidebar.multiselect(
    "Select Requirement:", options=data['Requirement'].unique(), default=data['Requirement'].unique()
)
status = st.sidebar.multiselect(
    "Select Status:", options=data['Status'].unique(), default=data['Status'].unique()
)
month = st.sidebar.multiselect(
    "Select Month:", options=data['Month'].unique(), default=data['Month'].unique()
)

# Filter the data based on selections
filtered_data = data[
    (data['Company Name'].isin(company_name) if company_name else True) &
    (data['Requirement'].isin(requirement) if requirement else True) &
    (data['Status'].isin(status) if status else True) &
    (data['Month'].isin(month) if month else True)
    ]

# Main Dashboard
st.title("Client Data Management Portal")
st.markdown("### Explore and manage your client data with ease.")

# Show filtered data
if not filtered_data.empty:
    st.write(f"Displaying {len(filtered_data)} records:")
    st.dataframe(filtered_data)
else:
    st.write("No records found.")

# Search functionality
search_term = st.text_input("Search by Client Name, Email, or Mobile No.:", "")
if search_term:
    search_results = data[
        data.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)
    ]
    if not search_results.empty:
        st.write(f"Search Results for '{search_term}': {len(search_results)} records found.")
        st.dataframe(search_results)
    else:
        st.write(f"No results found for '{search_term}'.")

# Download filtered data
if not filtered_data.empty:
    st.markdown("### Download Filtered Data")
    st.download_button(
        label="Download as CSV",
        data=filtered_data.to_csv(index=False).encode('utf-8'),
        file_name='filtered_client_data.csv',
        mime='text/csv',
    )

# Form to Add a New Client
st.markdown("### Add a New Client")
with st.form("add_client_form"):
    new_company = st.text_input("Company Name")
    new_client_name = st.text_input("Client Name")
    new_mail_id = st.text_input("Mail Id")
    new_mobile_no = st.text_input("Mobile No.")
    new_requirement = st.selectbox("Requirement", options=['WP', 'RCS', 'SMS', 'EMAIL'])
    new_status = st.selectbox("Status", options=['yes', 'no'])
    new_month = st.text_input("Month")  # Change to text_input to allow any month

    submitted = st.form_submit_button("Add Client")

    if submitted:
        if new_company and new_client_name and new_mail_id and new_mobile_no:
            new_client = {
                'Company Name': new_company,
                'Client Name': new_client_name,
                'Mail Id': new_mail_id,
                'Mobile No.': new_mobile_no,
                'Requirement': new_requirement,
                'Status': new_status,
                'Month': new_month  # Use the new_month value as entered by the user
            }
            data = add_client(data, new_client)
            st.success("New client added successfully!")
            st.write("Updated Client List:")
            st.dataframe(data)
        else:
            st.error("Please fill in all fields to add a new client.")
