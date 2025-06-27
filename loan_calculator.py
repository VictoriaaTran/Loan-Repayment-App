import streamlit as st
import pandas as pd
import plotly.express as px
import uuid

# set page config
st.set_page_config(page_title="Loan Repayment Calculator", layout='wide')
# header
st.title('Student Loan Repayment Calculator')

total_placeholder = st.empty()

# subheader
st.write('### Inputs')

# initialize input template - total loan and interest rate
col_debt, col_interest, _ = st.columns([6,6,2]) #creating columns
debt_input = col_debt.number_input("Your Loan Balance ($):", value=None, key='debt_input', placeholder='Enter amount')
interest_rate = col_interest.number_input("Interest Rate (%):", value=None, key='interest_rate',placeholder='Enter rate')

# initialize the number of inputs- based on ids
if 'input_ids' not in st.session_state:
    st.session_state.input_ids = [str(uuid.uuid4())] #start with one row

# display all the current inputs sets
to_remove = None #track which row to remove
for idx in st.session_state.input_ids:
    col1, col2, col3 = st.columns([6,6,2]) #2 inputs , 1 remove button
    with col1:
        st.number_input(f"Total Loan Balance ($):",value=None, placeholder='Enter amount', key=f"a_{idx}",label_visibility="collapsed")
    with col2:
        st.number_input(f"Interest rate (%):", value=None, placeholder="Enter rate", key=f"b_{idx}",label_visibility="collapsed")
    with col3:
        if st.button("Remove", key=f"remove_{idx}"):
            to_remove = idx

# button to dynamically add more inputs
if st.button("➕ Add Another Input"):
    st.session_state.input_ids.append(str(uuid.uuid4()))
    st.rerun()

# display total loans balance
total = debt_input
for idx in st.session_state.input_ids:
    val = st.session_state.get(f"a_{idx}")
    if val is not None:
        total += val #total principal 

# payment term
payment_term = st.number_input(label="Payment Term (Year):", min_value=0, max_value=50, placeholder="Enter term (year)")

# display total loan balance
total_placeholder.metric(label="Total Loan Balance:", value=f"${total:,.2f}" if total is not None else f'$0')

# repayments calculation
st.write("### Repayments")
col_loan_repay, col_interest_repay, col_monthly_pay= st.columns(3)

total_interest = debt_input * (interest_rate/100) * payment_term if (debt_input and interest_rate) is not None else 0

# step 1: calculate interest for each loan
for idx in st.session_state.input_ids:
    each_loan = st.session_state.get(f"a_{idx}")
    each_interest = st.session_state.get(f"b_{idx}")
    total_interest += each_loan * (each_interest/100) * payment_term if (each_loan and each_interest) is not None else 0

months = payment_term * 12
# step 2: Calculate monthly payment
total_payment = total + total_interest if (total and total_interest) is not None else 0
monthly_payment = (total_payment/ months) if months > 0 else 0

# display repayments metrics
with col_loan_repay:
    st.metric(label="Total Loan Paid:", value=f"${total_payment:,.2f}" if total_payment is not None else 0)
with col_interest_repay:
    st.metric(label="Total Interest Paid:", value=f"${total_interest:,.2f}" if total_interest is not None else 0)
with col_monthly_pay:
    st.metric(label="Monthly Payment:", value=f"${monthly_payment:,.2f}" if monthly_payment is not None else 0)

# create dataframe from repayment data
# pie chart
pie_data = {
    'Category': ['Total Payment', 'Total Interest'],
    'Value': [total_payment, total_interest]
}
df_pie = pd.DataFrame(pie_data)
fig = px.pie(df_pie, names='Category', values='Value', title='Loan Repayment Ratio')
st.plotly_chart(fig, on_select='rerun')

# removing the row 
if to_remove:
    st.session_state.input_ids.remove(to_remove)
    # Clean up associated keys
    st.session_state.pop(f"a_{to_remove}", None)
    st.session_state.pop(f"b_{to_remove}", None)
    st.rerun()
