import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import uuid

# header
st.title('Student Loan Repayment Calculator')

total_placeholder = st.empty()

# subheader
st.write('### Inputs')

# initialize input template - total loan and interest rate
col_debt, col_interest, _ = st.columns([6,6,2]) #creating columns
debt_input = col_debt.number_input("Your Loan Balance ($):", value=None, placeholder='Enter amount')
interest_rate = col_interest.number_input("Interest Rate (%):", value=None, placeholder='Enter rate')

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

# removing the row
if to_remove:
    st.session_state.input_ids.remove(to_remove)
    # Clean up associated keys
    st.session_state.pop(f"a_{to_remove}", None)
    st.session_state.pop(f"b_{to_remove}", None)
    st.rerun()

# button to dynamically add more inputs
if st.button("➕ Add Another Input"):
    st.session_state.input_ids.append(str(uuid.uuid4()))
    st.rerun()

# display total loans balance
total = debt_input
for idx in st.session_state.input_ids:
    val = st.session_state.get(f"a_{idx}")
    if val is not None:
        total += val

total_placeholder.metric(label="Total Loan Balance:", value=f"${total:,.2f}" if total is not None else f'$0')

# repayments calculation
st.write("### Repayments")
col_principal, col_interest_repay= st.columns(2)
total_interest = ((interest_rate if interest_rate is not None else 0)/100)*debt_input if debt_input is not None else 0

for idx in st.session_state.input_ids:
    loan = st.session_state.get(f"a_{idx}")
    interest = st.session_state.get(f"b_{idx}")
    total_interest += ((interest/100)*loan) if interest and loan is not None else 0

total_loan = total + total_interest

with col_principal:
    st.metric(label="Total Loan Paid:", value=f"${total_loan:,.2f}" if total_loan is not None else 0)
with col_interest_repay:
    st.metric(label="Total Interest Paid:", value=f"${total_interest:,.2f}" if total_interest is not None else 0)