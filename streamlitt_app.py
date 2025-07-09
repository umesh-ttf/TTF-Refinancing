import google.generativeai as genai
import json
import requests
import streamlit as st
from datetime import datetime
import numpy as np
import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import io

st.set_page_config(layout="wide")

tab1, tab2, tab3 = st.tabs(["Input values", "Graph", "Report Assistance"])

with tab1:
    # Title of the app
    st.title("Interactive Financial Table")
    col1, col2, col3, col4, col5 = st.columns(5)
    # Display the inputs in the respective columns
    with col1: 
        # User input cells for editable values
        st.markdown("<h3 style='font-size:18px; text-align:left;'>Fill in the Required Fields</h3>",unsafe_allow_html=True,)
        # Input fields
        revenue = st.number_input("Revenue", value=0.0, step=1.0, key="revenue")
        cost_of_goods_sold = st.number_input("Cost of Goods Sold or Services", value=0.0, step=1.0, key="cogs")
        operating_expenses = st.number_input("Operating Expenses", value=0.0, step=1.0, key="opex")
        depreciation = st.number_input("Depreciation & Amortization", value=0.0, step=1.0, key="depreciation")
        interest_expense = st.number_input("Interest Expense", value=0.0, step=1.0, key="interest")
        income_tax_expense = st.number_input("Income Tax Expense", value=0.0, step=1.0, key="tax")
    # Calculations
    gross_profit = revenue + cost_of_goods_sold
    ebitda = gross_profit + operating_expenses
    net_income_before_tax = ebitda + depreciation + interest_expense
    net_income = net_income_before_tax + income_tax_expense
    with col2:
        # Display the table
        # st.write("### Statement of Profit and Loss")
        # st.write(
        #     f"""
        #     | Particulars                         | Amount        |
        #     |-------------------------------------|---------------|
        #     | Revenue                             | {revenue:.2f}  |
        #     | Cost of Goods Sold or Services      | {cost_of_goods_sold:.2f}  |
        #     | **Gross Profit**                    | **{gross_profit:.2f}**  |
        #     | Operating Expenses                  | {operating_expenses:.2f}  |
        #     | **EBITDA**                          | **{ebitda:.2f}**  |
        #     | Depreciation & Amortization         | {depreciation:.2f}  |
        #     | Interest Expense                    | {interest_expense:.2f}  |
        #     | **Net Income Before Tax**           | **{net_income_before_tax:.2f}**  |
        #     | Income Tax Expense                  | {income_tax_expense:.2f}  |
        #     | **Net Income**                      | **{net_income:.2f}**  |
        #     """
        # )


        # Build the table data
        pl_data = [
            {"Particulars": "Revenue", "Amount": f"{revenue:.2f}"},
            {"Particulars": "Cost of Goods Sold or Services", "Amount": f"{cost_of_goods_sold:.2f}"},
            {"Particulars": "Gross Profit", "Amount": f"{gross_profit:.2f}"},
            {"Particulars": "Operating Expenses", "Amount": f"{operating_expenses:.2f}"},
            {"Particulars": "EBITDA", "Amount": f"{ebitda:.2f}"},
            {"Particulars": "Depreciation & Amortization", "Amount": f"{depreciation:.2f}"},
            {"Particulars": "Interest Expense", "Amount": f"{interest_expense:.2f}"},
            {"Particulars": "Net Income Before Tax", "Amount": f"{net_income_before_tax:.2f}"},
            {"Particulars": "Income Tax Expense", "Amount": f"{income_tax_expense:.2f}"},
            {"Particulars": "Net Income", "Amount": f"{net_income:.2f}"}
        ]

        # Create DataFrame
        pl_df = pd.DataFrame(pl_data)

        # Display in Streamlit
        st.write("### Statement of Profit and Loss")
        # st.table(pl_df)
        st.dataframe(pl_df, use_container_width=True)

    with col3: 
        # Balance Sheet Inputs
        st.markdown("<h3 style='font-size:18px; text-align:left;'>Fill in the Balance Sheet Fields</h3>", unsafe_allow_html=True)
        # Input fields for Assets
        cash = st.number_input("Cash", value=0.0, step=1.0, key="cash")
        accounts_receivable = st.number_input("Accounts Receivable", value=0.0, step=1.0, key="accounts_receivable")
        inventory = st.number_input("Inventory", value=0.0, step=1.0, key="inventory")
        other_current_assets = st.number_input("Other Current Assets", value=0.0, step=1.0, key="other_current_assets")
        ppe = st.number_input("Property, Plant & Equipment (Net)", value=0.0, step=1.0, key="ppe")
        other_assets = st.number_input("Other Assets/DTA", value=0.0, step=1.0, key="other_assets")
    # Calculate Total Assets (Sum1)
    total_assets = cash + accounts_receivable + inventory + other_current_assets + ppe + other_assets
    with col4:
        # Input fields for Liabilities and Equity
        accounts_payable = st.number_input("Accounts Payable/Provisions", value=0.0, step=1.0, key="accounts_payable")
        senior_secured = st.number_input("Senior Secured", value=0.0, step=1.0, key="senior_secured")
        debt_tranche1 = st.number_input("Debt 1 - Tranche 1", value=0.0, step=1.0, key="debt_tranche1")
        equity = st.number_input("Equity", value=0.0, step=1.0, key="equity")
        retained_earning = st.number_input("Retained Earning", value=0.0, step=1.0, key="retained_earning")
    # Calculate Total Equity and Liability (Sum2)
    total_equity_and_liability = (
        accounts_payable
        + senior_secured
        + debt_tranche1
        + equity
        + retained_earning
    )
    # Calculate Check (Sum3)
    check = total_equity_and_liability - total_assets
    with col5:
        # Display Balance Sheet Table
        # st.write("### Balance Sheet")
        # st.write(
        #     f"""
        #     | Particulars                                   | Amount        |
        #     |----------------------------------------------|---------------|
        #     | Cash                                         | {cash:.2f}    |
        #     | Accounts Receivable                          | {accounts_receivable:.2f}    |
        #     | Inventory                                    | {inventory:.2f}    |
        #     | Other Current Assets                         | {other_current_assets:.2f}    |
        #     | Property, Plant & Equipment (Net)           | {ppe:.2f}    |
        #     | Other Assets/DTA                             | {other_assets:.2f}    |
        #     | **Total Assets**                      | **{total_assets:.2f}**    |
        #     | *Short Term Debt*                              |  |
        #     | Accounts Payable/Provisions                  | {accounts_payable:.2f}   |
        #     | *Long Term Debt*                               |   |
        #     | Senior Secured                               | {senior_secured:.2f}    |
        #     | Debt 1 - Tranche 1                           | {debt_tranche1:.2f}    |
        #     | Equity                                       | {equity:.2f}    |
        #     | Retained Earning                             | {retained_earning:.2f}    |
        #     | **Total Equity and Liability**        | **{total_equity_and_liability:.2f}**    |
        #     | **Check**                             | **{check:.2f}**    |
        #     """
        # )

        # Define data for DataFrame
        balance_sheet_data = [
            {"Particulars": "Cash", "Amount": f"{cash:.2f}"},
            {"Particulars": "Accounts Receivable", "Amount": f"{accounts_receivable:.2f}"},
            {"Particulars": "Inventory", "Amount": f"{inventory:.2f}"},
            {"Particulars": "Other Current Assets", "Amount": f"{other_current_assets:.2f}"},
            {"Particulars": "Property, Plant & Equipment (Net)", "Amount": f"{ppe:.2f}"},
            {"Particulars": "Other Assets/DTA", "Amount": f"{other_assets:.2f}"},
            {"Particulars": "Total Assets", "Amount": f"{total_assets:.2f}"},
            {"Particulars": "*Short Term Debt*", "Amount": ""},
            {"Particulars": "Accounts Payable/Provisions", "Amount": f"{accounts_payable:.2f}"},
            {"Particulars": "*Long Term Debt*", "Amount": ""},
            {"Particulars": "Senior Secured", "Amount": f"{senior_secured:.2f}"},
            {"Particulars": "Debt 1 - Tranche 1", "Amount": f"{debt_tranche1:.2f}"},
            {"Particulars": "Equity", "Amount": f"{equity:.2f}"},
            {"Particulars": "Retained Earning", "Amount": f"{retained_earning:.2f}"},
            {"Particulars": "Total Equity and Liability", "Amount": f"{total_equity_and_liability:.2f}"},
            {"Particulars": "Check", "Amount": f"{check:.2f}"}
        ]

        # Create DataFrame
        balance_df = pd.DataFrame(balance_sheet_data)

        # Display
        st.write("### Balance Sheet")
        # st.table(balance_df, use_container_width=True)

        st.dataframe(balance_df, use_container_width=True)

    ###########
    # User input for editable cells
    st.markdown("<h3 style='font-size:18px; text-align:left;'>Fill in the Required Fields</h3>", unsafe_allow_html=True)
    # Input fields
    # Create two columns
    col1, col2, col3 = st.columns(3)
    # Dropdown list options
    options_IndivDebt = ["Individual", "Consolidated"]
    # Display the inputs in the respective columns
    with col1:
        # Create a dropdown list and store the user's choice
        IndivDebt_SenSec = st.selectbox("Please select an option:", options_IndivDebt, key="IndivDebt_SenSec")
        Additional_Loan_on_restructuring_SenSec = st.number_input("Additional Loan on restructuring (Senior Secured)",
            value=0.0, step=1.0, key="additional loan on restructuring sensec")
        Bank_Base_Rate_SenSec = st.number_input("Bank Base Rate (Senior Secured, in %)", 
        value=0.0, step=1.0, key="bank base rate sensec")
        Liquidity_Premiums_SenSec = st.number_input("Liquidity Premiums (Senior Secured, in %)", 
        value=0.0, step=1.0, key="liquidity premiums sensec")
        Credit_Risk_Premiums_SenSec = st.number_input("Credit Risk Premiums (Senior Secured, in %)", 
        value=0.0, step=1.0, key="credit risk premiums sensec")
        Maturity_Y_SenSec = st.number_input("Maturity Y (Senior Secured)", 
        value=0.0, step=1.0, key="maturity y premiums sensec")
        Amortization_Y_SenSec = st.number_input("Amortization Y (Senior Secured)", 
        value=0.0, step=1.0, key="amortization y premiums sensec")
    with col2:
        # Create a dropdown list and store the user's choice
        IndivDebt_StTerm = st.selectbox("Please select an option:", options_IndivDebt, key="IndivDebt_StTerm")
        Additional_Loan_on_restructuring_StTerm = st.number_input("Additional Loan on restructuring (Short Term)",
        value=0.0, step=1.0, key="additional loan on restructuring_stterm")
        Bank_Base_Rate_StTerm = st.number_input("Bank Base Rate (Short Term, in %)", 
        value=0.0, step=1.0, key="bank base rate stterm")
        Liquidity_Premiums_StTerm = st.number_input("Liquidity Premiums (Short Term, in %)", 
        value=0.0, step=1.0, key="liquidity premiums stterm")
        Credit_Risk_Premiums_StTerm = st.number_input("Credit Risk Premiums (Short Term, in %)", 
        value=0.0, step=1.0, key="credit risk premiums stterm")
        Maturity_Y_StTerm = st.number_input("Maturity Y (Short Term)", 
        value=0.0, step=1.0, key="maturity y premiums stterm")
        Amortization_Y_StTerm = st.number_input("Amortization Y (Short Term)", 
        value=0.0, step=1.0, key="amortization y premiums stterm")
    Bank_Base_Rate_SenSec /= 100
    Bank_Base_Rate_StTerm /= 100
    Liquidity_Premiums_SenSec /= 100
    Liquidity_Premiums_StTerm /= 100
    Credit_Risk_Premiums_SenSec /= 100
    Credit_Risk_Premiums_StTerm /= 100
    # Calculations
    Interest_Rate_per_annum_SenSec = Bank_Base_Rate_SenSec + Liquidity_Premiums_SenSec + Credit_Risk_Premiums_SenSec
    Interest_Rate_per_annum_StTerm = Bank_Base_Rate_StTerm + Liquidity_Premiums_StTerm + Credit_Risk_Premiums_StTerm
    Interest_Rate_per_month_SenSec = Interest_Rate_per_annum_SenSec / 12
    Interest_Rate_per_month_StTerm = Interest_Rate_per_annum_StTerm / 12
    Maturity_M_SenSec = Maturity_Y_SenSec * 12
    Maturity_M_StTerm = Maturity_Y_StTerm * 12
    Amortization_M_SenSec = Amortization_Y_SenSec * 12
    Amortization_M_StTerm = Amortization_Y_StTerm * 12
    if Maturity_Y_SenSec == Amortization_Y_SenSec:
        Repayment_Over_Y_SenSec = Amortization_Y_SenSec
    else:
        Repayment_Over_Y_SenSec = Maturity_Y_SenSec - Amortization_Y_SenSec
    Repayment_Over_Y_StTerm = Maturity_Y_StTerm - Amortization_Y_StTerm
    Repayment_Over_M_SenSec = Repayment_Over_Y_SenSec * 12
    Repayment_Over_M_StTerm = Repayment_Over_Y_StTerm * 12
    ##################To Remove
    # IndivDebt_SenSec = "Individual"
    # senior_secured = 12000
    # Repayment_Over_M_SenSec = 48
    # Interest_Rate_per_month_SenSec = 0.07/12
    # Amortization_M_SenSec = 48
    # Maturity_M_SenSec = 96
    # Additional_Loan_on_restructuring_SenSec = 60000
    # Amortization_Y_SenSec = 4
    # IndivDebt_StTerm = "Individual"
    # debt_tranche1 = 1000
    # Repayment_Over_M_StTerm = 72
    # Interest_Rate_per_month_StTerm = 0.075/12
    # Amortization_M_StTerm = 12
    # Maturity_M_StTerm = 84
    # Additional_Loan_on_restructuring_StTerm = 100000
    # Amortization_Y_StTerm = 1
    ####################
    ################Debt Calculation
    mc = 1
    y = 1
    mym = []
    while y < 11:
        for m in range(1, 13):
            mym.append([mc, y, datetime.strptime(str(m), "%m").strftime("%B"), np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
            mc += 1
        y += 1
    debtCalcLst = ['MonthCum', 'Year', 'Month', 'Opening', 'Additional Loan', 'Amortisation', 'Interest', 'Repayment', 'Closing']
    debtCalc_SenSec = pd.DataFrame(mym, columns=debtCalcLst)
    debtCalc_SenSec = debtCalc_SenSec.set_index('MonthCum')
    debtCalc_StTerm = pd.DataFrame(mym, columns=debtCalcLst)
    debtCalc_StTerm = debtCalc_StTerm.set_index('MonthCum')
    repaymentInit_SenSec = 0 # This is for cell C30
    outAftAmortization_SenSec = senior_secured + Additional_Loan_on_restructuring_SenSec
    flgAmort_SenSec = 0
    # outAftAmortization_SenSec = 0
    for i in debtCalc_SenSec.index:
        if i == 1:
            if IndivDebt_SenSec != "Consolidated":
                debtCalc_SenSec.loc[i, 'Opening'] = senior_secured
                debtCalc_SenSec.loc[i, 'Additional Loan'] = Additional_Loan_on_restructuring_SenSec
            else:
                debtCalc_SenSec.loc[i, 'Opening'] = 0.0
                debtCalc_SenSec.loc[i, 'Additional Loan'] = 0.0
            if debtCalc_SenSec.index[i-1] <= Amortization_M_SenSec:
                debtCalc_SenSec.loc[i, 'Amortisation'] = debtCalc_SenSec.loc[i, 'Opening'] * Interest_Rate_per_month_SenSec
            else:
                debtCalc_SenSec.loc[i, 'Amortisation'] = 0.0
            if debtCalc_SenSec.index[i-1] <= Maturity_M_SenSec and debtCalc_SenSec.index[i-1] > Amortization_M_SenSec:
                debtCalc_SenSec.loc[i, 'Interest'] = (debtCalc_SenSec.loc[i, 'Opening'] + debtCalc_SenSec.loc[i, 'Additional Loan']) * Interest_Rate_per_month_SenSec
            else:
                debtCalc_SenSec.loc[i, 'Interest'] = 0.0
            if Amortization_M_SenSec != 0:
                debtCalc_SenSec.loc[i, 'Repayment'] = 0.0
            else:
                if debtCalc_SenSec.index[i-1] > Amortization_M_SenSec and repaymentInit_SenSec == 0.0:
                    # debtCalc_SenSec.loc[i, 'Repayment'] = npf.pmt(Interest_Rate_per_month_SenSec, Repayment_Over_M_SenSec, debtCalc_SenSec.loc[i, 'Opening']) #Is it correct
                    debtCalc_SenSec.loc[i, 'Repayment'] = npf.pmt(Interest_Rate_per_month_SenSec, Repayment_Over_M_SenSec, outAftAmortization_SenSec) #Is it correct
                else:
                    debtCalc_SenSec.loc[i, 'Repayment'] = repaymentInit_SenSec
            debtCalc_SenSec.loc[i, 'Closing'] = debtCalc_SenSec.loc[i, ['Opening', 'Additional Loan', 'Amortisation', 'Interest', 'Repayment']].sum()
            if abs(debtCalc_SenSec.loc[i, 'Closing']) < 1:
                debtCalc_SenSec.loc[i, 'Closing'] = 0.0
        else:
            debtCalc_SenSec.loc[i, 'Opening'] = debtCalc_SenSec.loc[i-1, 'Closing']
            debtCalc_SenSec.loc[i, 'Additional Loan'] = 0.0
            if debtCalc_SenSec.index[i-1] <= Amortization_M_SenSec:
                debtCalc_SenSec.loc[i, 'Amortisation'] = debtCalc_SenSec.loc[i, 'Opening'] * Interest_Rate_per_month_SenSec
            else:
                debtCalc_SenSec.loc[i, 'Amortisation'] = 0.0
            if debtCalc_SenSec.index[i-1] <= Maturity_M_SenSec and debtCalc_SenSec.index[i-1] > Amortization_M_SenSec:
                debtCalc_SenSec.loc[i, 'Interest'] = debtCalc_SenSec.loc[i, 'Opening'] * Interest_Rate_per_month_SenSec
            else:
                debtCalc_SenSec.loc[i, 'Interest'] = 0.0
            if debtCalc_SenSec.loc[i-1, 'Closing'] < 1:
                debtCalc_SenSec.loc[i, 'Repayment'] = 0.0
            else:
                if debtCalc_SenSec.index[i-1] > Amortization_M_SenSec and debtCalc_SenSec.loc[i-1, 'Repayment'] == 0.0:
                    if flgAmort_SenSec == 0:
                        outAftAmortization_SenSec = debtCalc_SenSec.loc[i-1, 'Closing']
                        # st.write(outAftAmortization_SenSec)
                        flgAmort_SenSec = 1
                    debtCalc_SenSec.loc[i, 'Repayment'] = npf.pmt(Interest_Rate_per_month_SenSec, Repayment_Over_M_SenSec, outAftAmortization_SenSec)
                else:
                    debtCalc_SenSec.loc[i, 'Repayment'] = debtCalc_SenSec.loc[i-1, 'Repayment']
            debtCalc_SenSec.loc[i, 'Closing'] = debtCalc_SenSec.loc[i, ['Opening', 'Additional Loan', 'Amortisation', 'Interest', 'Repayment']].sum()
            if abs(debtCalc_SenSec.loc[i, 'Closing']) < 1:
                debtCalc_SenSec.loc[i, 'Closing'] = 0.0
    repaymentInit_StTerm = 0
    outAftAmortization_StTerm = debt_tranche1 + Additional_Loan_on_restructuring_StTerm
    # outAftAmortization_StTerm = 108172
    flgAmort_StTerm = 0
    for i in debtCalc_StTerm.index:
        if i == 1:
            if IndivDebt_StTerm != "Consolidated":
                debtCalc_StTerm.loc[i, 'Opening'] = debt_tranche1
                debtCalc_StTerm.loc[i, 'Additional Loan'] = Additional_Loan_on_restructuring_StTerm
            else:
                debtCalc_StTerm.loc[i, 'Opening'] = 0.0
                debtCalc_StTerm.loc[i, 'Additional Loan'] = 0.0
            if debtCalc_StTerm.index[i-1] <= Amortization_M_StTerm:
                debtCalc_StTerm.loc[i, 'Amortisation'] = debtCalc_StTerm.loc[i, 'Opening'] * Interest_Rate_per_month_StTerm
            else:
                debtCalc_StTerm.loc[i, 'Amortisation'] = 0.0
            if debtCalc_StTerm.index[i-1] <= Maturity_M_StTerm and debtCalc_StTerm.index[i-1] > Amortization_M_StTerm:
                debtCalc_StTerm.loc[i, 'Interest'] = (debtCalc_StTerm.loc[i, 'Opening'] + debtCalc_StTerm.loc[i, 'Additional Loan']) * Interest_Rate_per_month_StTerm
            else:
                debtCalc_StTerm.loc[i, 'Interest'] = 0.0
            if Amortization_M_StTerm != 0:
                debtCalc_StTerm.loc[i, 'Repayment'] = 0.0
            else:
                if debtCalc_StTerm.index[i-1] > Amortization_M_StTerm and repaymentInit_StTerm == 0.0:
                    # debtCalc_StTerm.loc[i, 'Repayment'] = npf.pmt(Interest_Rate_per_month_StTerm, Repayment_Over_M_StTerm, debtCalc_StTerm.loc[i, 'Opening']) #Is it correct
                    debtCalc_StTerm.loc[i, 'Repayment'] = npf.pmt(Interest_Rate_per_month_StTerm, Repayment_Over_M_StTerm, outAftAmortization_StTerm)
                else:
                    debtCalc_StTerm.loc[i, 'Repayment'] = repaymentInit_StTerm
            debtCalc_StTerm.loc[i, 'Closing'] = debtCalc_StTerm.loc[i, ['Opening', 'Additional Loan', 'Amortisation', 'Interest', 'Repayment']].sum()
            if abs(debtCalc_StTerm.loc[i, 'Closing']) < 1:
                debtCalc_StTerm.loc[i, 'Closing'] = 0.0
        else:
            debtCalc_StTerm.loc[i, 'Opening'] = debtCalc_StTerm.loc[i-1, 'Closing']
            debtCalc_StTerm.loc[i, 'Additional Loan'] = 0.0
            if debtCalc_StTerm.index[i-1] <= Amortization_M_StTerm:
                debtCalc_StTerm.loc[i, 'Amortisation'] = debtCalc_StTerm.loc[i, 'Opening'] * Interest_Rate_per_month_StTerm
            else:
                debtCalc_StTerm.loc[i, 'Amortisation'] = 0.0
            if debtCalc_StTerm.index[i-1] <= Maturity_M_StTerm and debtCalc_StTerm.index[i-1] > Amortization_M_StTerm:
                debtCalc_StTerm.loc[i, 'Interest'] = debtCalc_StTerm.loc[i, 'Opening'] * Interest_Rate_per_month_StTerm
            else:
                debtCalc_StTerm.loc[i, 'Interest'] = 0.0
            if debtCalc_StTerm.loc[i-1, 'Closing'] < 1:
                debtCalc_StTerm.loc[i, 'Repayment'] = 0.0
            else:
                if debtCalc_StTerm.index[i-1] > Amortization_M_StTerm and debtCalc_StTerm.loc[i-1, 'Repayment'] == 0.0:
                    if flgAmort_StTerm == 0:
                        outAftAmortization_StTerm = debtCalc_StTerm.loc[i-1, 'Closing']
                        # st.write(outAftAmortization_StTerm)
                        flgAmort_StTerm = 1
                    debtCalc_StTerm.loc[i, 'Repayment'] = npf.pmt(Interest_Rate_per_month_StTerm, Repayment_Over_M_StTerm, outAftAmortization_StTerm)
                else:
                    debtCalc_StTerm.loc[i, 'Repayment'] = debtCalc_StTerm.loc[i-1, 'Repayment']
            debtCalc_StTerm.loc[i, 'Closing'] = debtCalc_StTerm.loc[i, ['Opening', 'Additional Loan', 'Amortisation', 'Interest', 'Repayment']].sum()
            if abs(debtCalc_StTerm.loc[i, 'Closing']) < 1:
                debtCalc_StTerm.loc[i, 'Closing'] = 0.0
    totDebtCalcLst = ['Year', 'Additional Loan', 'Total Repayment', 'Total Interest']
    totDebtCalc = pd.DataFrame(np.nan, index=debtCalc_SenSec.index, columns=totDebtCalcLst)
    totDebtCalc['Year'] = debtCalc_SenSec['Year'].copy()
    totDebtCalc['Additional Loan'] = debtCalc_SenSec['Additional Loan'] + debtCalc_StTerm['Additional Loan']
    totDebtCalc['Total Repayment'] = debtCalc_SenSec['Repayment'] + debtCalc_StTerm['Repayment']
    totDebtCalc['Total Interest'] = debtCalc_SenSec['Interest'] + debtCalc_StTerm['Interest'] + debtCalc_SenSec['Amortisation'] + debtCalc_StTerm['Amortisation']
    # if Amortization_Y_SenSec == 0:
        # outAftAmortization_SenSec = senior_secured + Additional_Loan_on_restructuring_SenSec
    # else:
        # outAftAmortization_SenSec = debtCalc_SenSec[debtCalc_SenSec['Year']==Amortization_Y_SenSec + 1]['Opening'].values[0]

    # if Amortization_Y_StTerm == 0:
        # outAftAmortization_StTerm = debt_tranche1 + Additional_Loan_on_restructuring_StTerm
    # else:
        # outAftAmortization_StTerm = debtCalc_StTerm[debtCalc_StTerm['Year']==Amortization_Y_StTerm + 1]['Opening'].values[0]
    Repayment_SenSec = npf.pmt(Interest_Rate_per_month_SenSec, Repayment_Over_M_SenSec, outAftAmortization_SenSec)
    Repayment_StTerm = npf.pmt(Interest_Rate_per_month_StTerm, Repayment_Over_M_StTerm, outAftAmortization_StTerm)
    with col3:
        # Display the table
        # st.write("### Result Table")
        # st.write(
        #     f"""
        #     | Particulars                     | Senior Secured            | Short Term               |
        #     |---------------------------------|---------------------------|--------------------------|
        #     | Individual Debt                | {IndivDebt_SenSec}                | {IndivDebt_StTerm}     |
        #     | Loan Amount                    | {senior_secured:.2f}   | {debt_tranche1:.2f}  |
        #     | Additional Loan on restructuring | {Additional_Loan_on_restructuring_SenSec:.2f} | {Additional_Loan_on_restructuring_StTerm:.2f}|
        #     | Bank's Base Rate               | {Bank_Base_Rate_SenSec:.3f} | {Bank_Base_Rate_StTerm:.3f}|
        #     | Liquidity Premiums             | {Liquidity_Premiums_SenSec:.3f} | {Liquidity_Premiums_StTerm:.3f}|
        #     | Credit Risk Premium            | {Credit_Risk_Premiums_SenSec:.3f} | {Credit_Risk_Premiums_StTerm:.3f}|
        #     | Interest Rate per annum        | {Interest_Rate_per_annum_SenSec:.3f} | {Interest_Rate_per_annum_StTerm:.3f}|
        #     | Interest Rate per month        | {Interest_Rate_per_month_SenSec:.4f} | {Interest_Rate_per_month_StTerm:.4f}|
        #     | Maturity (Years)               | {Maturity_Y_SenSec:.2f} | {Maturity_Y_StTerm:.2f}|
        #     | Maturity (Months)              | {Maturity_M_SenSec:.2f} | {Maturity_M_StTerm:.2f}|
        #     | Amortization (Years)           | {Amortization_Y_SenSec:.2f} | {Amortization_Y_StTerm:.2f}|
        #     | Amortization (Months)          | {Amortization_M_SenSec:.2f} | {Amortization_M_StTerm:.2f}|
        #     | Repayment Over (Years)         | {Repayment_Over_Y_SenSec:.2f} | {Repayment_Over_Y_StTerm:.2f}|
        #     | Repayment Over (Months)        | {Repayment_Over_M_SenSec:.2f} | {Repayment_Over_M_StTerm:.2f}|
        #     | Outstanding after Amortization | {outAftAmortization_SenSec:.2f}  | {outAftAmortization_StTerm:.2f} |
        #     | Repayment                      | {Repayment_SenSec:.2f}  | {Repayment_StTerm:.2f} |
        #     """
        # )

        # Create the DataFrame
        result_table = pd.DataFrame({
            "Particulars": [
                "Individual Debt",
                "Loan Amount",
                "Additional Loan on restructuring",
                "Bank's Base Rate",
                "Liquidity Premiums",
                "Credit Risk Premium",
                "Interest Rate per annum",
                "Interest Rate per month",
                "Maturity (Years)",
                "Maturity (Months)",
                "Amortization (Years)",
                "Amortization (Months)",
                "Repayment Over (Years)",
                "Repayment Over (Months)",
                "Outstanding after Amortization",
                "Repayment"
            ],
            "Senior Secured": [
                IndivDebt_SenSec,
                f"{senior_secured:.2f}",
                f"{Additional_Loan_on_restructuring_SenSec:.2f}",
                f"{Bank_Base_Rate_SenSec:.3f}",
                f"{Liquidity_Premiums_SenSec:.3f}",
                f"{Credit_Risk_Premiums_SenSec:.3f}",
                f"{Interest_Rate_per_annum_SenSec:.3f}",
                f"{Interest_Rate_per_month_SenSec:.4f}",
                f"{Maturity_Y_SenSec:.2f}",
                f"{Maturity_M_SenSec:.2f}",
                f"{Amortization_Y_SenSec:.2f}",
                f"{Amortization_M_SenSec:.2f}",
                f"{Repayment_Over_Y_SenSec:.2f}",
                f"{Repayment_Over_M_SenSec:.2f}",
                f"{outAftAmortization_SenSec:.2f}",
                f"{Repayment_SenSec:.2f}"
            ],
            "Short Term": [
                IndivDebt_StTerm,
                f"{debt_tranche1:.2f}",
                f"{Additional_Loan_on_restructuring_StTerm:.2f}",
                f"{Bank_Base_Rate_StTerm:.3f}",
                f"{Liquidity_Premiums_StTerm:.3f}",
                f"{Credit_Risk_Premiums_StTerm:.3f}",
                f"{Interest_Rate_per_annum_StTerm:.3f}",
                f"{Interest_Rate_per_month_StTerm:.4f}",
                f"{Maturity_Y_StTerm:.2f}",
                f"{Maturity_M_StTerm:.2f}",
                f"{Amortization_Y_StTerm:.2f}",
                f"{Amortization_M_StTerm:.2f}",
                f"{Repayment_Over_Y_StTerm:.2f}",
                f"{Repayment_Over_M_StTerm:.2f}",
                f"{outAftAmortization_StTerm:.2f}",
                f"{Repayment_StTerm:.2f}"
            ]
        })

        # Display table
        st.write("### Result Table")
        st.dataframe(result_table, use_container_width=True)        
    # Input fields for Assets
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        projections_year = int(st.number_input("Projections Year", value=12.0, step=1.0, key="projections_year"))
        capital_expenditure_additions1 = st.number_input("Capital Expenditure Additions", value=0.0, step=1.0, key="capital_expenditure_additions1")
        asset_depreciated_over_years = st.number_input("Asset Depreciated over years", value=0.0, step=1.0, key="asset_depreciated_over_years")
        tax_rates = st.number_input("Tax Rates (in %)", value=0.0, step=1.0, key="tax_rates")
    tax_rates /= 100
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Growth Rate (GR, in %)</h3>", unsafe_allow_html=True)
    # Create two columns
    col1, col2, col3, col4 = st.columns(4)
    growth_rate_rev_Dict = {}
    growth_rate_cost_Dict = {}
    growth_rate_cost_ope_Dict = {}
    growth_rate_capex_Dict = {}
    for i in range(projections_year):
        with col1:
            growth_rate_rev_Dict[i+1] = st.number_input(f"GR of Revenue p.a {i+1}", value=0.0, step=1.0, key=f"growth_rate_revenue_p_a_{i+1}")
        with col2:
            growth_rate_cost_Dict[i+1] = st.number_input(f"GR in Cost p.a {i+1}", value=0.0, step=1.0, key=f"growth_rate_cost_p_a_{i+1}")
        with col3:
            growth_rate_cost_ope_Dict[i+1] = st.number_input(f"GR in Cost p.a (Oper) {i+1}", value=0.0, step=1.0, key=f"growth_rate_cost_p_a_Operating{i+1}")
        with col4:
            if i == 0:
                growth_rate_capex_Dict[i+1] = st.number_input(f"GR in Capex p.a {i+1}", value=0.0, step=1.0, key=f"growth_rate_capex_p_a_{i+1}", disabled=True)
            else:
                growth_rate_capex_Dict[i+1] = st.number_input(f"GR in Capex p.a {i+1}", value=0.0, step=1.0, key=f"growth_rate_capex_p_a_{i+1}")

    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Revenue Seasonality (in %)</h3>", unsafe_allow_html=True)
    Rev_Seas_Dict = {}
    cpt = 1
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    for elt in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
        if cpt == 1 or cpt == 7:
            with col1:
                Rev_Seas_Dict[cpt] = st.number_input(elt, value=0.0, step=1.0, key=f"revenue_seasonality_{cpt}")
        elif cpt == 2 or cpt == 8:
            with col2:
                Rev_Seas_Dict[cpt] = st.number_input(elt, value=0.0, step=1.0, key=f"revenue_seasonality_{cpt}")
        elif cpt == 3 or cpt == 9:
            with col3:
                Rev_Seas_Dict[cpt] = st.number_input(elt, value=0.0, step=1.0, key=f"revenue_seasonality_{cpt}")
        elif cpt == 4 or cpt == 10:
            with col4:
                Rev_Seas_Dict[cpt] = st.number_input(elt, value=0.0, step=1.0, key=f"revenue_seasonality_{cpt}")
        elif cpt == 5 or cpt == 11:
            with col5:
                Rev_Seas_Dict[cpt] = st.number_input(elt, value=0.0, step=1.0, key=f"revenue_seasonality_{cpt}")
        else:
            with col6:
                Rev_Seas_Dict[cpt] = st.number_input(elt, value=0.0, step=1.0, key=f"revenue_seasonality_{cpt}")
        cpt += 1
    Rev_Seas_Dict = {key: value / 100 for key, value in Rev_Seas_Dict.items()}
    # Calculate Total Assets (Sum1)
    nb_Months = projections_year * 12
    ##################To Remove
    # projections_year = 10
    # growth_rate_rev_Dict = {}
    # growth_rate_cost_Dict = {}
    # growth_rate_cost_ope_Dict = {}
    # growth_rate_capex_Dict = {}
    # for i in range(projections_year):
        # growth_rate_rev_Dict[i+1] = i/100
        # growth_rate_cost_Dict[i+1] = i+i
        # growth_rate_cost_ope_Dict[i+1] = i-2
        # growth_rate_capex_Dict[i+1] = i*5
    # revenue = 35000
    # cost_of_goods_sold = -26000
    # operating_expenses = -5000
    # capital_expenditure_additions1 = 20000
    #################################
    colLst = ["Revenue per annum", "GR of Revenue p.a", "COGS or COS", "GR in Cost p.a", 
    "Operating Cost", "GR in Cost p.a (Oper)", "Capital Expenditure Additions", "GR in Capex p.a"]
    projectionDF = pd.DataFrame(np.nan, index=range(1, projections_year + 1), columns=colLst)
    projectionDF["GR of Revenue p.a"] = growth_rate_rev_Dict
    projectionDF["GR in Cost p.a"] = growth_rate_cost_Dict
    projectionDF["GR in Cost p.a (Oper)"] = growth_rate_cost_ope_Dict
    projectionDF["GR in Capex p.a"] = growth_rate_capex_Dict
    projectionDF = projectionDF.astype(float)
    # User enters values that are now converted to percent
    projectionDF["GR of Revenue p.a"] /= 100
    projectionDF["GR in Cost p.a"] /= 100
    projectionDF["GR in Cost p.a (Oper)"] /= 100
    projectionDF["GR in Capex p.a"] /= 100
    ##################To Remove
    # projectionDF.loc[1, "GR of Revenue p.a"] = 1
    # projectionDF.loc[2, "GR of Revenue p.a"] = 0.3
    # projectionDF.loc[3, "GR of Revenue p.a"] = 0.2
    # projectionDF.loc[4, "GR of Revenue p.a"] = 0.2
    # projectionDF.loc[1, "GR in Cost p.a"] = -0.03
    # projectionDF.loc[2, "GR in Cost p.a"] = -0.03
    # projectionDF.loc[3, "GR in Cost p.a"] = -0.03
    # projectionDF.loc[4, "GR in Cost p.a"] = -0.02
    # projectionDF.loc[1, "GR in Cost p.a (Oper)"] = -0.04
    # projectionDF.loc[2, "GR in Cost p.a (Oper)"] = -0.04
    # projectionDF.loc[3, "GR in Cost p.a (Oper)"] = -0.04
    # projectionDF.loc[4, "GR in Cost p.a (Oper)"] = 0.0
    # projectionDF.loc[2, "GR in Capex p.a"] = 0.0
    # projectionDF.loc[3, "GR in Capex p.a"] = 0.03
    # projectionDF.loc[4, "GR in Capex p.a"] = 0.03
    # projectionDF.loc[5, "GR in Capex p.a"] = 0.03
    #########################
    for elt in projectionDF.index:
        if elt > projections_year:
            projectionDF.loc[elt, "Revenue per annum"] = 0.0
            projectionDF.loc[elt, "COGS or COS"] = 0.0
            projectionDF.loc[elt, "Operating Cost"] = 0.0
            projectionDF.loc[elt, "Capital Expenditure Additions"] = 0.0
        elif elt == 1:
            projectionDF.loc[elt, "Revenue per annum"] = revenue * (1 + projectionDF.loc[elt, "GR of Revenue p.a"])
            projectionDF.loc[elt, "COGS or COS"] = -cost_of_goods_sold * (1 + projectionDF.loc[elt, "GR in Cost p.a"])
            projectionDF.loc[elt, "Operating Cost"] = -operating_expenses * (1 + projectionDF.loc[elt, "GR in Cost p.a (Oper)"])
            projectionDF.loc[elt, "Capital Expenditure Additions"] = capital_expenditure_additions1
        else:
            projectionDF.loc[elt, "Revenue per annum"] = projectionDF.loc[elt - 1, "Revenue per annum"] * (1 + projectionDF.loc[elt, "GR of Revenue p.a"])
            projectionDF.loc[elt, "COGS or COS"] = projectionDF.loc[elt - 1, "COGS or COS"] * (1 + projectionDF.loc[elt, "GR in Cost p.a"])
            projectionDF.loc[elt, "Operating Cost"] = projectionDF.loc[elt - 1, "Operating Cost"] * (1 + projectionDF.loc[elt, "GR in Cost p.a (Oper)"])
            projectionDF.loc[elt, "Capital Expenditure Additions"] = projectionDF.loc[elt - 1, "Capital Expenditure Additions"] * (1 + projectionDF.loc[elt, "GR in Capex p.a"])
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Working Capital Assumptions</h3>", unsafe_allow_html=True)
    # Create two columns
    col1, col2 = st.columns(2)
    with col1:
        AR_pct = st.number_input(f"Account Receivable as a % of 12 Months Forward Revenue (in %)", value=0.0, step=1.0, key=f"AR_pct")
        Inventory_pct = st.number_input(f"Inventory % of 12 Months Forward COGS (in %)", value=0.0, step=1.0, key=f"Inventory_pct")
    with col2:
        oCA_pct = st.number_input(f"Other Current Assets % of 12 Months Forward Revenue (in %)", value=0.0, step=1.0, key=f"oCA_pct")
        AP_pct = st.number_input(f"Accounts Payable as a % of 12 Months Forward COGS/OPEX (in %)", value=0.0, step=1.0, key=f"AP_pct")
    AR_pct /= 100
    Inventory_pct /= 100
    oCA_pct /= 100
    AP_pct /= 100
    mc = 1
    y = 1
    mym = []
    while y < 11:
        for m in range(1, 13):
            mym.append([mc, y, datetime.strptime(str(m), "%m").strftime("%B"), np.nan, np.nan, np.nan, np.nan])
            mc += 1
        y += 1
    depSchedCalcLst = ['MonthCum', 'Year', 'Month', 'Opening', 'Capex Addition', 'Depreciation', 'Closing']
    depSchedCalcTbl = pd.DataFrame(mym, columns=depSchedCalcLst)
    depSchedCalcTbl = depSchedCalcTbl.set_index('MonthCum')    
    ##################To Remove
    # total_assets = 15000
    # nb_Months = 120
    # asset_depreciated_over_years = 10
    #################
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Depreciation Schedule DEBT CALC</h3>", unsafe_allow_html=True)
    st.dataframe(debtCalc_SenSec.T)
    st.dataframe(debtCalc_StTerm.T)
    st.dataframe(totDebtCalc.T)
    st.dataframe(projectionDF.T)
    # DEPRECIATION
    for i in depSchedCalcTbl.index:
        if i == 1:
            depSchedCalcTbl.loc[i, 'Opening'] = ppe
            depSchedCalcTbl.loc[i, 'Capex Addition'] = projectionDF.loc[depSchedCalcTbl.loc[i, 'Year'], "Capital Expenditure Additions"] / 12
            if i > nb_Months:
                depSchedCalcTbl.loc[i, 'Depreciation'] = 0
            else:
                depSchedCalcTbl.loc[i, 'Depreciation'] = (depSchedCalcTbl.loc[i, 'Opening'] + depSchedCalcTbl.loc[i, 'Capex Addition']) / (asset_depreciated_over_years * 12)
            depSchedCalcTbl.loc[i, 'Closing'] = (depSchedCalcTbl.loc[i, 'Opening'] + depSchedCalcTbl.loc[i, 'Capex Addition']) - depSchedCalcTbl.loc[i, 'Depreciation']
        else:
            depSchedCalcTbl.loc[i, 'Opening'] = depSchedCalcTbl.loc[i-1, 'Closing']
            depSchedCalcTbl.loc[i, 'Capex Addition'] = projectionDF.loc[depSchedCalcTbl.loc[i, 'Year'], "Capital Expenditure Additions"] / 12
            if i > nb_Months:
                depSchedCalcTbl.loc[i, 'Depreciation'] = 0
            else:
                depSchedCalcTbl.loc[i, 'Depreciation'] = (depSchedCalcTbl.loc[i, 'Opening'] + depSchedCalcTbl.loc[i, 'Capex Addition']) / (asset_depreciated_over_years * 12)
            depSchedCalcTbl.loc[i, 'Closing'] = (depSchedCalcTbl.loc[i, 'Opening'] + depSchedCalcTbl.loc[i, 'Capex Addition']) - depSchedCalcTbl.loc[i, 'Depreciation']
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Depreciation Schedule</h3>", unsafe_allow_html=True)
    depSchedCalcTbl_Disp = depSchedCalcTbl.copy()
    depSchedCalcTbl_Disp = depSchedCalcTbl_Disp.round({col: 1 for col in depSchedCalcTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(depSchedCalcTbl_Disp.T)
    ################Debt Calculation
    mc = 1
    y = 1
    PnLStatLst = ['MonthCum', 'Seasonality', 'Year', 'Month', 'Revenue', 'Restructured Cost', 
    'Gross Profit', 'Indirect Cost', 'EBITDA', 'Depreciation and Amortisation', 'EBIT', 
    'Interest', 'EBT', 'Tax', 'Net Profit']
    mym = []
    while y < 11:
        for m in range(1, 13):
            mymSub = [mc, Rev_Seas_Dict[m], y, datetime.strptime(str(m), "%m").strftime("%B")]
            mymSub.extend([np.nan] * (len(PnLStatLst) - 4))
            mym.append(mymSub)
            mc += 1
        y += 1
    PnLStatTbl = pd.DataFrame(mym, columns=PnLStatLst)
    PnLStatTbl = PnLStatTbl.set_index('MonthCum')
    for i in PnLStatTbl.index:
        PnLStatTbl.loc[i, 'Revenue'] = projectionDF.loc[PnLStatTbl.loc[i, 'Year'], "Revenue per annum"] * PnLStatTbl.loc[i, 'Seasonality']
        PnLStatTbl.loc[i, 'Restructured Cost'] = -projectionDF.loc[PnLStatTbl.loc[i, 'Year'], "COGS or COS"] * PnLStatTbl.loc[i, 'Seasonality']
        PnLStatTbl.loc[i, 'Gross Profit'] = PnLStatTbl.loc[i, 'Revenue'] + PnLStatTbl.loc[i, 'Restructured Cost']
        PnLStatTbl.loc[i, 'Indirect Cost'] = -projectionDF.loc[PnLStatTbl.loc[i, 'Year'], "Operating Cost"] * PnLStatTbl.loc[i, 'Seasonality']
        PnLStatTbl.loc[i, 'EBITDA'] = PnLStatTbl.loc[i, 'Gross Profit'] + PnLStatTbl.loc[i, 'Indirect Cost']
        PnLStatTbl.loc[i, 'Depreciation and Amortisation'] = -depSchedCalcTbl.loc[i, 'Depreciation']
        PnLStatTbl.loc[i, 'EBIT'] = PnLStatTbl.loc[i, 'EBITDA'] + PnLStatTbl.loc[i, 'Depreciation and Amortisation']
        PnLStatTbl.loc[i, 'Interest'] = -debtCalc_SenSec.loc[i, 'Interest'] - debtCalc_StTerm.loc[i, 'Interest'] - debtCalc_SenSec.loc[i, 'Amortisation'] - debtCalc_StTerm.loc[i, 'Amortisation']
        PnLStatTbl.loc[i, 'EBT'] = PnLStatTbl.loc[i, 'EBIT'] + PnLStatTbl.loc[i, 'Interest']
        PnLStatTbl.loc[i, 'Tax'] = 0.3 * PnLStatTbl.loc[i, 'Indirect Cost']
        PnLStatTbl.loc[i, 'Net Profit'] = PnLStatTbl.loc[i, 'EBT'] + PnLStatTbl.loc[i, 'Tax']
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Debt Calculations</h3>", unsafe_allow_html=True)
    PnLStatTbl_Disp = PnLStatTbl.copy()
    PnLStatTbl_Disp = PnLStatTbl_Disp.round({col: 1 for col in PnLStatTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(PnLStatTbl_Disp.T)
    # Monthly - BS,PL,CFS
    # Monthly Table A
    mc = 1
    y = 1
    PnLStatMtlyLst = ['MonthCum', 'Year', 'Month', 'Revenue', 'Cost of Goods Sold', 'Gross Profit', 
    'Operating Expenses', 'EBITDA', 'Depreciation and Amortisation', 'Interest Expense', 
    'Net Income Before Tax', 'Income Tax Expense', 'Net Income']
    PnLStatMtlySr = pd.Series(np.nan, index=PnLStatMtlyLst[3:])
    PnLStatMtlySr['Revenue'] = revenue
    PnLStatMtlySr['Cost of Goods Sold'] = cost_of_goods_sold
    PnLStatMtlySr['Gross Profit'] = revenue + cost_of_goods_sold
    PnLStatMtlySr['Operating Expenses'] = operating_expenses
    PnLStatMtlySr['EBITDA'] = revenue + cost_of_goods_sold + operating_expenses
    PnLStatMtlySr['Depreciation and Amortisation'] = depreciation
    PnLStatMtlySr['Interest Expense'] = interest_expense
    PnLStatMtlySr['Net Income Before Tax'] = revenue + cost_of_goods_sold + operating_expenses + depreciation + interest_expense
    PnLStatMtlySr['Income Tax Expense'] = income_tax_expense
    PnLStatMtlySr['Net Income'] = revenue + cost_of_goods_sold + operating_expenses + depreciation + interest_expense + income_tax_expense
    mym = []
    while y < 11:
        for m in range(1, 13):
            mymSub = [mc, y, datetime.strptime(str(m), "%m").strftime("%B")]
            mymSub.extend([np.nan] * (len(PnLStatMtlyLst) - 3))
            mym.append(mymSub)
            mc += 1
        y += 1
    PnLStatMtlyTbl = pd.DataFrame(mym, columns=PnLStatMtlyLst)
    PnLStatMtlyTbl = PnLStatMtlyTbl.set_index('MonthCum')
    for i in PnLStatMtlyTbl.index:
        PnLStatMtlyTbl.loc[i, 'Revenue'] = PnLStatTbl.loc[i, 'Revenue']
        PnLStatMtlyTbl.loc[i, 'Cost of Goods Sold'] = PnLStatTbl.loc[i, 'Restructured Cost']
        PnLStatMtlyTbl.loc[i, 'Gross Profit'] = PnLStatTbl.loc[i, 'Gross Profit']
        PnLStatMtlyTbl.loc[i, 'Operating Expenses'] = PnLStatTbl.loc[i, 'Indirect Cost']
        PnLStatMtlyTbl.loc[i, 'EBITDA'] = PnLStatTbl.loc[i, 'EBITDA']
        PnLStatMtlyTbl.loc[i, 'Depreciation and Amortisation'] = PnLStatTbl.loc[i, 'Depreciation and Amortisation']
        PnLStatMtlyTbl.loc[i, 'Interest Expense'] = PnLStatTbl.loc[i, 'Interest']
        PnLStatMtlyTbl.loc[i, 'Net Income Before Tax'] = PnLStatMtlyTbl.loc[i, 'EBITDA'] + PnLStatMtlyTbl.loc[i, 'Depreciation and Amortisation'] + PnLStatMtlyTbl.loc[i, 'Interest Expense']
        PnLStatMtlyTbl.loc[i, 'Income Tax Expense'] = PnLStatTbl.loc[i, 'Tax']
        PnLStatMtlyTbl.loc[i, 'Net Income'] = PnLStatMtlyTbl.loc[i, 'Net Income Before Tax'] + PnLStatMtlyTbl.loc[i, 'Income Tax Expense']
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Monthly - BS,PL,CFS: Table A</h3>", unsafe_allow_html=True)
    PnLStatMtlyTbl_Disp = PnLStatMtlyTbl.copy()
    nan_row = pd.DataFrame([[np.nan] * PnLStatMtlyTbl_Disp.shape[1]], columns=PnLStatMtlyTbl_Disp.columns)
    PnLStatMtlyTbl_Disp = pd.concat([nan_row, PnLStatMtlyTbl_Disp], ignore_index=True)
    for col in PnLStatMtlySr.index:
        PnLStatMtlyTbl_Disp.loc[0, col] = PnLStatMtlySr[col]
    PnLStatMtlyTbl_Disp = PnLStatMtlyTbl_Disp.round({col: 1 for col in PnLStatMtlyTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(PnLStatMtlyTbl_Disp.T)
    # Monthly Table C
    mc = 1
    y = 1
    CFSMtlyLst = ['MonthCum', 'Year', 'Month', 'Net Income', 'Depreciation and Amortisation', 'Change in Working Capital', 'Interest Paid', 
    'Net Cash from Operating Activities', 'Capital Expenditures', 'Net Cash from Investing Activities', 'Proceeds from Long-term Debt', 
    'Repayment of Long-term Debt', 'Net Cash from Financing Activities', 'Net Cash flow', 'Opening', 'Closing']
    mym = []
    while y < 11:
        for m in range(1, 13):
            mymSub = [mc, y, datetime.strptime(str(m), "%m").strftime("%B")]
            mymSub.extend([np.nan] * (len(CFSMtlyLst) - 3))
            mym.append(mymSub)
            mc += 1
        y += 1
    CFSMtlyTbl = pd.DataFrame(mym, columns=CFSMtlyLst)
    CFSMtlyTbl = CFSMtlyTbl.set_index('MonthCum')
    # for i in CFSMtlyTbl.index:
        # CFSMtlyTbl.loc[i, 'Net Income'] = PnLStatTbl.loc[i, 'Net Profit']
        # CFSMtlyTbl.loc[i, 'Depreciation and Amortisation'] = -PnLStatTbl.loc[i, 'Depreciation and Amortisation']
        ####MODIF
        # CFSMtlyTbl.loc[i, 'Change in Working Capital'] = np.nan
        # CFSMtlyTbl.loc[i, 'Interest Paid'] = -PnLStatTbl.loc[i, 'Interest']
        # CFSMtlyTbl.loc[i, 'Net Cash from Operating Activities'] = CFSMtlyTbl.loc[i, 'Net Income'] + CFSMtlyTbl.loc[i, 'Depreciation and Amortisation'] + CFSMtlyTbl.loc[i, 'Change in Working Capital'] + CFSMtlyTbl.loc[i, 'Interest Paid']
        # CFSMtlyTbl.loc[i, 'Capital Expenditures'] = -depSchedCalcTbl.loc[i, 'Capex Addition']
        # CFSMtlyTbl.loc[i, 'Net Cash from Investing Activities'] = CFSMtlyTbl.loc[i, 'Capital Expenditures']
        # CFSMtlyTbl.loc[i, 'Proceeds from Long-term Debt'] = totDebtCalc.loc[i, 'Additional Loan']
        # CFSMtlyTbl.loc[i, 'Repayment of Long-term Debt'] = totDebtCalc.loc[i, 'Total Repayment']
        # CFSMtlyTbl.loc[i, 'Net Cash from Financing Activities'] = CFSMtlyTbl.loc[i, 'Proceeds from Long-term Debt'] + CFSMtlyTbl.loc[i, 'Repayment of Long-term Debt']
        # CFSMtlyTbl.loc[i, 'Net Cash flow'] = CFSMtlyTbl.loc[i, 'Net Cash from Operating Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Investing Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Financing Activities']
        # if i == 1:
            # CFSMtlyTbl.loc[i, 'Opening'] = cash
        # else:
            # CFSMtlyTbl.loc[i, 'Opening'] = CFSMtlyTbl.loc[i-1, 'Closing']
        # CFSMtlyTbl.loc[i, 'Closing'] = CFSMtlyTbl.loc[i, 'Net Cash flow'] + CFSMtlyTbl.loc[i, 'Opening']
    # Monthly Table B
    mc = 1
    y = 1
    BSMtlyLst = ['MonthCum', 'Year', 'Month', 'Cash', 'Accounts Receivable', 'Inventory', 'Other Current Assets', 'Property, Plant & Equipment (Net)', 
    'Other Assets/DTA', 'Total Assets', 'Short Term Debt', 'Accounts payable/Provisions', 'Long Term Debt', 'Senior Secured', 'Debt 1 - Tranche 1', 'Equity', 'Retained Earning', 
    'Total Equity and Liability', 'Difference', 'Working Capital', 'Change in working capital']
    BSMtlySr = pd.Series(np.nan, index=BSMtlyLst[3:])
    BSMtlySr['Cash'] = cash
    BSMtlySr['Accounts Receivable'] = accounts_receivable
    BSMtlySr['Inventory'] = inventory
    BSMtlySr['Other Current Assets'] = other_current_assets
    BSMtlySr['Property, Plant & Equipment (Net)'] = ppe
    BSMtlySr['Other Assets/DTA'] = other_assets
    BSMtlySr['Total Assets'] = cash + accounts_receivable + inventory + other_current_assets + ppe + other_assets
    BSMtlySr['Short Term Debt'] = np.nan
    BSMtlySr['Accounts payable/Provisions'] = accounts_payable
    BSMtlySr['Long Term Debt'] = np.nan
    BSMtlySr['Senior Secured'] = senior_secured
    BSMtlySr['Debt 1 - Tranche 1'] = debt_tranche1
    BSMtlySr['Equity'] = equity
    BSMtlySr['Retained Earning'] = retained_earning
    BSMtlySr['Total Equity and Liability'] = accounts_payable + senior_secured + debt_tranche1 + equity + retained_earning
    BSMtlySr['Difference'] = BSMtlySr['Total Equity and Liability'] - BSMtlySr['Total Assets']
    BSMtlySr['Working Capital'] = accounts_receivable + inventory + other_current_assets + other_assets - accounts_payable
    BSMtlySr['Change in working capital'] = np.nan
    mym = []
    while y < 11:
        for m in range(1, 13):
            mymSub = [mc, y, datetime.strptime(str(m), "%m").strftime("%B")]
            mymSub.extend([np.nan] * (len(BSMtlyLst) - 3))
            mym.append(mymSub)
            mc += 1
        y += 1
    BSMtlyTbl = pd.DataFrame(mym, columns=BSMtlyLst)
    BSMtlyTbl = BSMtlyTbl.set_index('MonthCum')
    for i in BSMtlyTbl.index:
        CFSMtlyTbl.loc[i, 'Net Income'] = PnLStatTbl.loc[i, 'Net Profit']
        CFSMtlyTbl.loc[i, 'Depreciation and Amortisation'] = -PnLStatTbl.loc[i, 'Depreciation and Amortisation']
        #####MODIF
        # CFSMtlyTbl.loc[i, 'Change in Working Capital'] = np.nan
        CFSMtlyTbl.loc[i, 'Interest Paid'] = -PnLStatTbl.loc[i, 'Interest']
        # CFSMtlyTbl.loc[i, 'Net Cash from Operating Activities'] = CFSMtlyTbl.loc[i, 'Net Income'] + CFSMtlyTbl.loc[i, 'Depreciation and Amortisation'] + CFSMtlyTbl.loc[i, 'Change in Working Capital'] + CFSMtlyTbl.loc[i, 'Interest Paid']
        CFSMtlyTbl.loc[i, 'Capital Expenditures'] = -depSchedCalcTbl.loc[i, 'Capex Addition']
        CFSMtlyTbl.loc[i, 'Net Cash from Investing Activities'] = CFSMtlyTbl.loc[i, 'Capital Expenditures']
        CFSMtlyTbl.loc[i, 'Proceeds from Long-term Debt'] = totDebtCalc.loc[i, 'Additional Loan']
        CFSMtlyTbl.loc[i, 'Repayment of Long-term Debt'] = totDebtCalc.loc[i, 'Total Repayment']
        CFSMtlyTbl.loc[i, 'Net Cash from Financing Activities'] = CFSMtlyTbl.loc[i, 'Proceeds from Long-term Debt'] + CFSMtlyTbl.loc[i, 'Repayment of Long-term Debt']
        # CFSMtlyTbl.loc[i, 'Net Cash flow'] = CFSMtlyTbl.loc[i, 'Net Cash from Operating Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Investing Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Financing Activities']
        # if i == 1:
        #     CFSMtlyTbl.loc[i, 'Opening'] = cash
        # else:
        #     CFSMtlyTbl.loc[i, 'Opening'] = CFSMtlyTbl.loc[i-1, 'Closing']
        # CFSMtlyTbl.loc[i, 'Closing'] = CFSMtlyTbl.loc[i, 'Net Cash flow'] + CFSMtlyTbl.loc[i, 'Opening']
        # BSMtlyTbl.loc[i, 'Cash'] = CFSMtlyTbl.loc[i, 'Closing']
        BSMtlyTbl.loc[i, 'Accounts Receivable'] = AR_pct * PnLStatMtlyTbl.loc[i:i+11, 'Revenue'].sum()
        BSMtlyTbl.loc[i, 'Inventory'] = -Inventory_pct * PnLStatMtlyTbl.loc[i:i+11, 'Cost of Goods Sold'].sum()
        BSMtlyTbl.loc[i, 'Other Current Assets'] = oCA_pct * PnLStatMtlyTbl.loc[i:i+11, 'Revenue'].sum()
        BSMtlyTbl.loc[i, 'Property, Plant & Equipment (Net)'] = depSchedCalcTbl.loc[i, 'Closing']
        BSMtlyTbl.loc[i, 'Other Assets/DTA'] = oCA_pct * PnLStatMtlyTbl.loc[i:i+11, 'Revenue'].sum()
        # BSMtlyTbl.loc[i, 'Total Assets'] = BSMtlyTbl.loc[i, 'Cash'] + BSMtlyTbl.loc[i, 'Accounts Receivable'] + BSMtlyTbl.loc[i, 'Inventory'] + BSMtlyTbl.loc[i, 'Other Current Assets'] + BSMtlyTbl.loc[i, 'Property, Plant & Equipment (Net)'] + BSMtlyTbl.loc[i, 'Other Assets/DTA']
        BSMtlyTbl.loc[i, 'Short Term Debt'] = np.nan
        BSMtlyTbl.loc[i, 'Accounts payable/Provisions'] = -AP_pct * (PnLStatMtlyTbl.loc[i:i+11, 'Cost of Goods Sold'].sum() + PnLStatMtlyTbl.loc[i:i+11, 'Operating Expenses'].sum())
        BSMtlyTbl.loc[i, 'Long Term Debt'] = np.nan
        BSMtlyTbl.loc[i, 'Senior Secured'] = debtCalc_SenSec.loc[i, 'Closing']
        BSMtlyTbl.loc[i, 'Debt 1 - Tranche 1'] = debtCalc_StTerm.loc[i, 'Closing']
        if i == 1:
            BSMtlyTbl.loc[i, 'Equity'] = BSMtlySr['Equity']
    # RESTART HERE
            BSMtlyTbl.loc[i, 'Retained Earning'] = retained_earning + PnLStatTbl.loc[i, 'Net Profit']
        else:
            BSMtlyTbl.loc[i, 'Equity'] = BSMtlyTbl.loc[i-1, 'Equity']
            BSMtlyTbl.loc[i, 'Retained Earning'] = BSMtlyTbl.loc[i-1, 'Retained Earning'] + PnLStatTbl.loc[i, 'Net Profit']
        BSMtlyTbl.loc[i, 'Total Equity and Liability'] = BSMtlyTbl.loc[i, 'Accounts payable/Provisions'] + BSMtlyTbl.loc[i, 'Senior Secured'] + BSMtlyTbl.loc[i, 'Debt 1 - Tranche 1'] + BSMtlyTbl.loc[i, 'Equity'] + BSMtlyTbl.loc[i, 'Retained Earning']
        # BSMtlyTbl.loc[i, 'Difference'] = BSMtlyTbl.loc[i, 'Total Equity and Liability'] - BSMtlyTbl.loc[i, 'Total Assets']
        BSMtlyTbl.loc[i, 'Working Capital'] = BSMtlyTbl.loc[i, 'Accounts Receivable'] + BSMtlyTbl.loc[i, 'Inventory'] + BSMtlyTbl.loc[i, 'Other Current Assets'] + BSMtlyTbl.loc[i, 'Other Assets/DTA'] - BSMtlyTbl.loc[i, 'Accounts payable/Provisions']
        if i == 1:
            BSMtlyTbl.loc[i, 'Change in working capital'] = BSMtlyTbl.loc[i, 'Working Capital'] - BSMtlySr['Working Capital']
        else:
            BSMtlyTbl.loc[i, 'Change in working capital'] = BSMtlyTbl.loc[i, 'Working Capital'] - BSMtlyTbl.loc[i-1, 'Working Capital']
        CFSMtlyTbl.loc[i, 'Change in Working Capital'] = -BSMtlyTbl.loc[i, 'Change in working capital']
        CFSMtlyTbl.loc[i, 'Net Cash from Operating Activities'] = CFSMtlyTbl.loc[i, 'Net Income'] + CFSMtlyTbl.loc[i, 'Depreciation and Amortisation'] + CFSMtlyTbl.loc[i, 'Change in Working Capital'] + CFSMtlyTbl.loc[i, 'Interest Paid']
        CFSMtlyTbl.loc[i, 'Net Cash flow'] = CFSMtlyTbl.loc[i, 'Net Cash from Operating Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Investing Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Financing Activities']
        if i == 1:
            CFSMtlyTbl.loc[i, 'Opening'] = cash
        else:
            CFSMtlyTbl.loc[i, 'Opening'] = CFSMtlyTbl.loc[i-1, 'Closing']
        CFSMtlyTbl.loc[i, 'Closing'] = CFSMtlyTbl.loc[i, 'Net Cash flow'] + CFSMtlyTbl.loc[i, 'Opening']
        BSMtlyTbl.loc[i, 'Cash'] = CFSMtlyTbl.loc[i, 'Closing']
        BSMtlyTbl.loc[i, 'Total Assets'] = BSMtlyTbl.loc[i, 'Cash'] + BSMtlyTbl.loc[i, 'Accounts Receivable'] + BSMtlyTbl.loc[i, 'Inventory'] + BSMtlyTbl.loc[i, 'Other Current Assets'] + BSMtlyTbl.loc[i, 'Property, Plant & Equipment (Net)'] + BSMtlyTbl.loc[i, 'Other Assets/DTA']
        BSMtlyTbl.loc[i, 'Difference'] = BSMtlyTbl.loc[i, 'Total Equity and Liability'] - BSMtlyTbl.loc[i, 'Total Assets']
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Monthly - BS,PL,CFS: Table B</h3>", unsafe_allow_html=True)
    BSMtlyTbl_Disp = BSMtlyTbl.copy()
    nan_row = pd.DataFrame([[np.nan] * BSMtlyTbl_Disp.shape[1]], columns=BSMtlyTbl_Disp.columns)
    BSMtlyTbl_Disp = pd.concat([nan_row, BSMtlyTbl_Disp], ignore_index=True)
    for col in BSMtlySr.index:
        BSMtlyTbl_Disp.loc[0, col] = BSMtlySr[col]
    BSMtlyTbl_Disp = BSMtlyTbl_Disp.round({col: 1 for col in BSMtlyTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(BSMtlyTbl_Disp.T)
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Monthly - BS,PL,CFS: Table C</h3>", unsafe_allow_html=True)
    CFSMtlyTbl_Disp = CFSMtlyTbl.copy()
    CFSMtlyTbl_Disp = CFSMtlyTbl_Disp.round({col: 1 for col in CFSMtlyTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(CFSMtlyTbl_Disp.T)
    # Monthly KPIs
    mc = 1
    y = 1
    KPIMtlyLst = ['MonthCum', 'Year', 'Month', 'Debt to EBITDA', 'Debt Service Coverage Ratio', 'Loan to Value (Tangible Asset) Ratio', 'Interest Coverage Ratio', 
    'Current Ratio', 'Quick Ratio (Acid Test Ratio)', 'Debt to Equity Ratio', 'Operating Margin', 'FCFF', 'FCFE']

    mym = []
    while y < 11:
        for m in range(1, 13):
            mymSub = [mc, y, datetime.strptime(str(m), "%m").strftime("%B")]
            mymSub.extend([np.nan] * (len(KPIMtlyLst) - 3))
            mym.append(mymSub)
            mc += 1
        y += 1
    KPIMtlyTbl = pd.DataFrame(mym, columns=KPIMtlyLst)
    KPIMtlyTbl = KPIMtlyTbl.set_index('MonthCum')
    for i in KPIMtlyTbl.index:
        KPIMtlyTbl.loc[i, 'Debt to EBITDA'] = (BSMtlyTbl.loc[i, 'Senior Secured'] + BSMtlyTbl.loc[i, 'Debt 1 - Tranche 1']) / PnLStatMtlyTbl.loc[i, 'EBITDA']
        if CFSMtlyTbl.loc[i, 'Repayment of Long-term Debt'] == 0:
            KPIMtlyTbl.loc[i, 'Debt Service Coverage Ratio'] = 0
        else:
            KPIMtlyTbl.loc[i, 'Debt Service Coverage Ratio'] = PnLStatMtlyTbl.loc[i, 'EBITDA'] / -CFSMtlyTbl.loc[i, 'Repayment of Long-term Debt']
        KPIMtlyTbl.loc[i, 'Loan to Value (Tangible Asset) Ratio'] = (BSMtlyTbl.loc[i, 'Senior Secured'] + BSMtlyTbl.loc[i, 'Debt 1 - Tranche 1']) / BSMtlyTbl.loc[i, 'Property, Plant & Equipment (Net)']
        KPIMtlyTbl.loc[i, 'Interest Coverage Ratio'] = (PnLStatMtlyTbl.loc[i, 'EBITDA'] + PnLStatMtlyTbl.loc[i, 'Depreciation and Amortisation']) / -PnLStatMtlyTbl.loc[i, 'Interest Expense']
        KPIMtlyTbl.loc[i, 'Current Ratio'] = (BSMtlyTbl.loc[i, 'Cash'] + BSMtlyTbl.loc[i, 'Accounts Receivable'] + BSMtlyTbl.loc[i, 'Inventory']+ BSMtlyTbl.loc[i, 'Other Current Assets'] + BSMtlyTbl.loc[i, 'Other Assets/DTA']) / BSMtlyTbl.loc[i, 'Accounts payable/Provisions']
        KPIMtlyTbl.loc[i, 'Quick Ratio (Acid Test Ratio)'] = (BSMtlyTbl.loc[i, 'Cash'] + BSMtlyTbl.loc[i, 'Accounts Receivable'] + BSMtlyTbl.loc[i, 'Other Current Assets'] + BSMtlyTbl.loc[i, 'Other Assets/DTA']) / BSMtlyTbl.loc[i, 'Accounts payable/Provisions']
        KPIMtlyTbl.loc[i, 'Debt to Equity Ratio'] = (BSMtlyTbl.loc[i, 'Senior Secured'] + BSMtlyTbl.loc[i, 'Debt 1 - Tranche 1']) / (BSMtlyTbl.loc[i, 'Equity'] + BSMtlyTbl.loc[i, 'Retained Earning'])
        KPIMtlyTbl.loc[i, 'Operating Margin'] = PnLStatMtlyTbl.loc[i, 'EBITDA'] / PnLStatMtlyTbl.loc[i, 'Revenue']
        KPIMtlyTbl.loc[i, 'FCFF'] = CFSMtlyTbl.loc[i, 'Net Cash from Operating Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Investing Activities']
        KPIMtlyTbl.loc[i, 'FCFE'] = CFSMtlyTbl.loc[i, 'Net Cash from Operating Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Investing Activities'] + CFSMtlyTbl.loc[i, 'Net Cash from Financing Activities']
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Monthly - BS,PL,CFS: KPIS - Key Financial Ratios</h3>", unsafe_allow_html=True)
    KPIMtlyTbl_Disp = KPIMtlyTbl.copy()
    KPIMtlyTbl_Disp = KPIMtlyTbl_Disp.round({col: 2 for col in KPIMtlyTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(KPIMtlyTbl_Disp.T)
    # Annual - BS,PL,CFS
    # Yearly Table A
    y = 1
    PnLStatMtlyLst = ['Year', 'Revenue', 'Cost of Goods Sold', 'Gross Profit', 
    'Operating Expenses', 'EBITDA', 'Depreciation and Amortisation', 'Interest Expense', 
    'Net Income Before Tax', 'Income Tax Expense', 'Net Income']
    PnLStatYlySr = PnLStatMtlySr.copy()
    yLst = []
    while y < 11:
        ySub= [y]
        ySub.extend([np.nan] * (len(PnLStatMtlyLst) - 1))
        yLst.append(ySub)
        y += 1
    PnLStatYlyTbl = pd.DataFrame(yLst, columns=PnLStatMtlyLst)
    PnLStatYlyTbl = PnLStatYlyTbl.set_index('Year')
    for i in PnLStatYlyTbl.index:
        # PnLStatYlyTbl.loc[i, 'Revenue'] = PnLStatMtlyTbl.loc[i, 'Revenue'][PnLStatMtlyTbl.loc['Year'] == i].sum()
        PnLStatYlyTbl.loc[i, 'Revenue'] = PnLStatMtlyTbl[PnLStatMtlyTbl['Year'] == i]['Revenue'].sum()
        # PnLStatYlyTbl.loc[i, 'Cost of Goods Sold'] = PnLStatMtlyTbl.loc[i, 'Cost of Goods Sold'][PnLStatMtlyTbl.loc['Year'] == i].sum()
        PnLStatYlyTbl.loc[i, 'Cost of Goods Sold'] = PnLStatMtlyTbl[PnLStatMtlyTbl['Year'] == i]['Cost of Goods Sold'].sum()
        PnLStatYlyTbl.loc[i, 'Gross Profit'] = PnLStatYlyTbl.loc[i, 'Revenue'] + PnLStatYlyTbl.loc[i, 'Cost of Goods Sold']
        # PnLStatYlyTbl.loc[i, 'Operating Expenses'] = PnLStatMtlyTbl.loc[i, 'Operating Expenses'][PnLStatMtlyTbl.loc['Year'] == i].sum()
        PnLStatYlyTbl.loc[i, 'Operating Expenses'] = PnLStatMtlyTbl[PnLStatMtlyTbl['Year'] == i]['Operating Expenses'].sum()
        PnLStatYlyTbl.loc[i, 'EBITDA'] = PnLStatYlyTbl.loc[i, 'Gross Profit'] + PnLStatYlyTbl.loc[i, 'Operating Expenses']
        # PnLStatYlyTbl.loc[i, 'Depreciation and Amortisation'] = PnLStatMtlyTbl.loc[i, 'Depreciation and Amortisation'][PnLStatMtlyTbl.loc['Year'] == i].sum()
        PnLStatYlyTbl.loc[i, 'Depreciation and Amortisation'] = PnLStatMtlyTbl[PnLStatMtlyTbl['Year'] == i]['Depreciation and Amortisation'].sum()
        # PnLStatYlyTbl.loc[i, 'Interest Expense'] = PnLStatMtlyTbl.loc[i, 'Interest Expense'][PnLStatMtlyTbl.loc['Year'] == i].sum()
        PnLStatYlyTbl.loc[i, 'Interest Expense'] = PnLStatMtlyTbl[PnLStatMtlyTbl['Year'] == i]['Interest Expense'].sum()
        PnLStatYlyTbl.loc[i, 'Net Income Before Tax'] = PnLStatYlyTbl.loc[i, 'EBITDA'] + PnLStatYlyTbl.loc[i, 'Depreciation and Amortisation'] + PnLStatYlyTbl.loc[i, 'Interest Expense']
        # PnLStatYlyTbl.loc[i, 'Income Tax Expense'] = PnLStatMtlyTbl.loc[i, 'Income Tax Expense'][PnLStatMtlyTbl.loc['Year'] == i].sum()
        PnLStatYlyTbl.loc[i, 'Income Tax Expense'] = PnLStatMtlyTbl[PnLStatMtlyTbl['Year'] == i]['Income Tax Expense'].sum()
        PnLStatYlyTbl.loc[i, 'Net Income'] = PnLStatYlyTbl.loc[i, 'Net Income Before Tax'] + PnLStatYlyTbl.loc[i, 'Income Tax Expense']
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Annual - BS,PL,CFS: Table A</h3>", unsafe_allow_html=True)
    PnLStatYlyTbl_Disp = PnLStatYlyTbl.copy()
    nan_row = pd.DataFrame([[np.nan] * PnLStatYlyTbl_Disp.shape[1]], columns=PnLStatYlyTbl_Disp.columns)
    PnLStatYlyTbl_Disp = pd.concat([nan_row, PnLStatYlyTbl_Disp], ignore_index=True)
    for col in PnLStatYlySr.index:
        PnLStatYlyTbl_Disp.loc[0, col] = PnLStatYlySr[col]
    PnLStatYlyTbl_Disp = PnLStatYlyTbl_Disp.round({col: 1 for col in PnLStatYlyTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(PnLStatYlyTbl_Disp.T)
    # Yearly Table B
    y = 1
    BSYlyLst = ['Year', 'Month', 'Cash', 'Accounts Receivable', 'Inventory', 'Other Current Assets', 'Property, Plant & Equipment (Net)', 
    'Other Assets/DTA', 'Total Assets', 'Short Term Debt', 'Accounts payable/Provisions', 'Long Term Debt', 'Senior Secured', 'Debt 1 - Tranche 1', 'Equity', 
    'Retained Earning', 'Total Equity and Liability', 'Difference', 'Working Capital', 'Change in working capital']
    BSYlySr = BSMtlySr.copy()
    yLst = []
    while y < 11:
        ySub= [y]
        ySub.extend([np.nan] * (len(BSYlyLst) - 1))
        yLst.append(ySub)
        y += 1
    BSYlyTbl = pd.DataFrame(yLst, columns=BSYlyLst)
    BSYlyTbl = BSYlyTbl.set_index('Year')
    BSYlyTbl['Month'] = 'December'
    for i in BSYlyTbl.index:
        # BSYlyTbl.loc[i, 'Cash'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Cash']
        BSYlyTbl.loc[i, 'Cash'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Cash'].values[0]
        # BSYlyTbl.loc[i, 'Accounts Receivable'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Accounts Receivable']
        BSYlyTbl.loc[i, 'Accounts Receivable'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Accounts Receivable'].values[0]
        # BSYlyTbl.loc[i, 'Inventory'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Inventory']
        BSYlyTbl.loc[i, 'Inventory'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Inventory'].values[0]
        # BSYlyTbl.loc[i, 'Other Current Assets'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Other Current Assets']
        BSYlyTbl.loc[i, 'Other Current Assets'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Other Current Assets'].values[0]
        # BSYlyTbl.loc[i, 'Property, Plant & Equipment (Net)'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Property, Plant & Equipment (Net)']
        BSYlyTbl.loc[i, 'Property, Plant & Equipment (Net)'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Property, Plant & Equipment (Net)'].values[0]
        # BSYlyTbl.loc[i, 'Other Assets/DTA'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Other Assets/DTA']
        BSYlyTbl.loc[i, 'Other Assets/DTA'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Other Assets/DTA'].values[0]
        BSYlyTbl.loc[i, 'Total Assets'] = BSYlyTbl.loc[i, 'Cash'] + BSYlyTbl.loc[i, 'Accounts Receivable'] + BSYlyTbl.loc[i, 'Inventory'] + BSYlyTbl.loc[i, 'Other Current Assets'] + BSYlyTbl.loc[i, 'Property, Plant & Equipment (Net)'] + BSYlyTbl.loc[i, 'Other Assets/DTA']
        # BSYlyTbl.loc[i, 'Short Term Debt'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Short Term Debt']
        BSYlyTbl.loc[i, 'Short Term Debt'] = np.nan
        # BSYlyTbl.loc[i, 'Accounts payable/Provisions'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Accounts payable/Provisions']
        BSYlyTbl.loc[i, 'Accounts payable/Provisions'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Accounts payable/Provisions'].values[0]
        # BSYlyTbl.loc[i, 'Long Term Debt'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Long Term Debt']
        BSYlyTbl.loc[i, 'Long Term Debt'] = np.nan
        # BSYlyTbl.loc[i, 'Senior Secured'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Senior Secured']
        BSYlyTbl.loc[i, 'Senior Secured'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Senior Secured'].values[0]
        # BSYlyTbl.loc[i, 'Debt 1 - Tranche 1'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Debt 1 - Tranche 1']
        BSYlyTbl.loc[i, 'Debt 1 - Tranche 1'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Debt 1 - Tranche 1'].values[0]
        # BSYlyTbl.loc[i, 'Equity'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Equity']
        BSYlyTbl.loc[i, 'Equity'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Equity'].values[0]
        # BSYlyTbl.loc[i, 'Retained Earning'] = BSMtlyTbl.loc[(BSMtlyTbl.loc['Year'] == i) & (BSMtlyTbl.loc['Month'] == 'December'), 'Retained Earning']
        BSYlyTbl.loc[i, 'Retained Earning'] = BSMtlyTbl[(BSMtlyTbl['Year'] == i) & (BSMtlyTbl['Month'] == 'December')]['Retained Earning'].values[0]
        BSYlyTbl.loc[i, 'Total Equity and Liability'] = BSYlyTbl.loc[i, 'Accounts payable/Provisions'] + BSYlyTbl.loc[i, 'Senior Secured'] + BSYlyTbl.loc[i, 'Debt 1 - Tranche 1'] + BSYlyTbl.loc[i, 'Equity'] + BSYlyTbl.loc[i, 'Retained Earning']
        BSYlyTbl.loc[i, 'Difference'] = BSYlyTbl.loc[i, 'Total Equity and Liability'] - BSYlyTbl.loc[i, 'Total Assets']
        BSYlyTbl.loc[i, 'Working Capital'] = BSYlyTbl.loc[i, 'Accounts Receivable'] + BSYlyTbl.loc[i, 'Inventory'] + BSYlyTbl.loc[i, 'Other Current Assets'] + BSYlyTbl.loc[i, 'Other Assets/DTA'] - BSYlyTbl.loc[i, 'Accounts payable/Provisions']
        if i == 1:
            BSYlyTbl.loc[i, 'Change in working capital'] = BSYlyTbl.loc[i, 'Working Capital'] - BSYlySr['Working Capital']
        else:
            BSYlyTbl.loc[i, 'Change in working capital'] = BSYlyTbl.loc[i, 'Working Capital'] - BSYlyTbl.loc[i-1, 'Working Capital']
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Annual - BS,PL,CFS: Table B</h3>", unsafe_allow_html=True)
    BSYlyTbl_Disp = BSYlyTbl.copy()
    nan_row = pd.DataFrame([[np.nan] * BSYlyTbl_Disp.shape[1]], columns=BSYlyTbl_Disp.columns)
    BSYlyTbl_Disp = pd.concat([nan_row, BSYlyTbl_Disp], ignore_index=True)
    for col in BSYlySr.index:
        BSYlyTbl_Disp.loc[0, col] = BSYlySr[col]
    BSYlyTbl_Disp = BSYlyTbl_Disp.round({col: 1 for col in BSYlyTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(BSYlyTbl_Disp.T)
    # Yearly Table C
    y = 1
    CFSYlyLst = ['Year', 'Month', 'Net Income', 'Depreciation and Amortisation', 'Change in Working Capital', 'Interest Paid', 
    'Net Cash from Operating Activities', 'Capital Expenditures', 'Net Cash from Investing Activities', 'Proceeds from Long-term Debt', 
    'Repayment of Long-term Debt', 'Net Cash from Financing Activities', 'Net Cash flow', 'Opening', 'Closing']
    yLst = []
    while y < 11:
        ySub= [y]
        ySub.extend([np.nan] * (len(CFSYlyLst) - 1))
        yLst.append(ySub)
        y += 1
    CFSYlyTbl = pd.DataFrame(yLst, columns=CFSYlyLst)
    CFSYlyTbl = CFSYlyTbl.set_index('Year')
    CFSYlyTbl['Month'] = 'December'
    for i in CFSYlyTbl.index:
        CFSYlyTbl.loc[i, 'Net Income'] = PnLStatYlyTbl.loc[i, 'Net Income']
        CFSYlyTbl.loc[i, 'Depreciation and Amortisation'] = -PnLStatYlyTbl.loc[i, 'Depreciation and Amortisation']
        CFSYlyTbl.loc[i, 'Change in Working Capital'] = -BSYlyTbl.loc[i, 'Change in working capital']
        CFSYlyTbl.loc[i, 'Interest Paid'] = -PnLStatYlyTbl.loc[i, 'Interest Expense']
        CFSYlyTbl.loc[i, 'Net Cash from Operating Activities'] = CFSYlyTbl.loc[i, 'Net Income'] + CFSYlyTbl.loc[i, 'Depreciation and Amortisation'] + CFSYlyTbl.loc[i, 'Change in Working Capital'] + CFSYlyTbl.loc[i, 'Interest Paid']
        CFSYlyTbl.loc[i, 'Capital Expenditures'] = -projectionDF.loc[i, "Capital Expenditure Additions"]
        CFSYlyTbl.loc[i, 'Net Cash from Investing Activities'] = CFSYlyTbl.loc[i, 'Capital Expenditures']
        # CFSYlyTbl.loc[i, 'Proceeds from Long-term Debt'] = totDebtCalc.loc[i, 'Additional Loan'][totDebtCalc.loc['Year'] == i].sum()
        CFSYlyTbl.loc[i, 'Proceeds from Long-term Debt'] = totDebtCalc[totDebtCalc['Year'] == i]['Additional Loan'].sum()
        # CFSYlyTbl.loc[i, 'Repayment of Long-term Debt'] = totDebtCalc.loc[i, 'Total Repayment'][totDebtCalc.loc['Year'] == i].sum()
        CFSYlyTbl.loc[i, 'Repayment of Long-term Debt'] = totDebtCalc[totDebtCalc['Year'] == i]['Total Repayment'].sum()
        CFSYlyTbl.loc[i, 'Net Cash from Financing Activities'] = CFSYlyTbl.loc[i, 'Proceeds from Long-term Debt'] + CFSYlyTbl.loc[i, 'Repayment of Long-term Debt']
        CFSYlyTbl.loc[i, 'Net Cash flow'] = CFSYlyTbl.loc[i, 'Net Cash from Operating Activities'] + CFSYlyTbl.loc[i, 'Net Cash from Investing Activities'] + CFSYlyTbl.loc[i, 'Net Cash from Financing Activities']
        if i == 1:
            # CFSYlyTbl.loc[i, 'Opening'] = BSYlyTbl.loc[i, 'Cash']
            CFSYlyTbl.loc[i, 'Opening'] = BSMtlySr['Cash']
        else:
            CFSYlyTbl.loc[i, 'Opening'] = CFSYlyTbl.loc[i-1, 'Closing']
        CFSYlyTbl.loc[i, 'Closing'] = CFSYlyTbl.loc[i, 'Net Cash flow'] + CFSYlyTbl.loc[i, 'Opening']
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Annual - BS,PL,CFS: Table C</h3>", unsafe_allow_html=True)
    CFSYlyTbl_Disp = CFSYlyTbl.copy()
    CFSYlyTbl_Disp = CFSYlyTbl_Disp.round({col: 2 for col in CFSYlyTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(CFSYlyTbl_Disp.T)
    # Yearly KPIs
    y = 1
    KPIYlyLst = ['Year', 'Month', 'Debt to EBITDA', 'Debt Service Coverage Ratio', 'Loan to Value (Tangible Asset) Ratio', 'Interest Coverage Ratio', 
    'Current Ratio', 'Quick Ratio (Acid Test Ratio)', 'Debt to Equity Ratio', 'Operating Margin']
    yLst = []
    while y < 11:
        ySub= [y]
        ySub.extend([np.nan] * (len(KPIYlyLst) - 1))
        yLst.append(ySub)
        y += 1
    KPIYlyTbl = pd.DataFrame(yLst, columns=KPIYlyLst)
    KPIYlyTbl = KPIYlyTbl.set_index('Year')
    KPIYlyTbl['Month'] = 'December'
    for i in KPIYlyTbl.index:
        if BSYlyTbl.loc[i, 'Senior Secured'] < 1 and BSYlyTbl.loc[i, 'Debt 1 - Tranche 1'] < 1:
            KPIYlyTbl.loc[i, 'Debt to EBITDA'] = 0
        else:
            KPIYlyTbl.loc[i, 'Debt to EBITDA'] = (BSYlyTbl.loc[i, 'Senior Secured'] + BSYlyTbl.loc[i, 'Debt 1 - Tranche 1']) / PnLStatYlyTbl.loc[i, 'EBITDA']
        if CFSYlyTbl.loc[i, 'Repayment of Long-term Debt'] == 0:
            if i == 1:
                KPIYlyTbl.loc[i, 'Debt Service Coverage Ratio'] = 0
            else:
                KPIYlyTbl.loc[i, 'Debt Service Coverage Ratio'] = KPIYlyTbl.loc[i-1, 'Debt Service Coverage Ratio']
        else:
            KPIYlyTbl.loc[i, 'Debt Service Coverage Ratio'] = PnLStatYlyTbl.loc[i, 'EBITDA'] / -CFSYlyTbl.loc[i, 'Repayment of Long-term Debt']
        KPIYlyTbl.loc[i, 'Loan to Value (Tangible Asset) Ratio'] = (BSYlyTbl.loc[i, 'Senior Secured'] + BSYlyTbl.loc[i, 'Debt 1 - Tranche 1']) / BSYlyTbl.loc[i, 'Property, Plant & Equipment (Net)']
        if PnLStatYlyTbl.loc[i, 'EBITDA'] == 0:
            KPIYlyTbl.loc[i, 'Interest Coverage Ratio'] = 0
        else:
            KPIYlyTbl.loc[i, 'Interest Coverage Ratio'] = (PnLStatYlyTbl.loc[i, 'EBITDA'] + PnLStatYlyTbl.loc[i, 'Depreciation and Amortisation']) / -PnLStatYlyTbl.loc[i, 'Interest Expense']
        if BSYlyTbl.loc[i, 'Accounts payable/Provisions'] == 0:
            KPIYlyTbl.loc[i, 'Current Ratio'] = 0
            KPIYlyTbl.loc[i, 'Quick Ratio (Acid Test Ratio)'] = 0
        else:
            KPIYlyTbl.loc[i, 'Current Ratio'] = (BSYlyTbl.loc[i, 'Cash'] + BSYlyTbl.loc[i, 'Accounts Receivable'] + BSYlyTbl.loc[i, 'Inventory']+ BSYlyTbl.loc[i, 'Other Current Assets'] + BSYlyTbl.loc[i, 'Other Assets/DTA']) / BSYlyTbl.loc[i, 'Accounts payable/Provisions']
            KPIYlyTbl.loc[i, 'Quick Ratio (Acid Test Ratio)'] = (BSYlyTbl.loc[i, 'Cash'] + BSYlyTbl.loc[i, 'Accounts Receivable'] + BSYlyTbl.loc[i, 'Other Current Assets'] + BSYlyTbl.loc[i, 'Other Assets/DTA']) / BSYlyTbl.loc[i, 'Accounts payable/Provisions']
        if BSYlyTbl.loc[i, 'Senior Secured'] < 1 and BSYlyTbl.loc[i, 'Debt 1 - Tranche 1'] < 1:
            KPIYlyTbl.loc[i, 'Debt to Equity Ratio'] = 0
        else:
            KPIYlyTbl.loc[i, 'Debt to Equity Ratio'] = (BSYlyTbl.loc[i, 'Senior Secured'] + BSYlyTbl.loc[i, 'Debt 1 - Tranche 1']) / (BSYlyTbl.loc[i, 'Equity'] + BSYlyTbl.loc[i, 'Retained Earning'])
        if PnLStatYlyTbl.loc[i, 'Revenue'] == 0:
            KPIYlyTbl.loc[i, 'Operating Margin'] = np.nan
        else:
            KPIYlyTbl.loc[i, 'Operating Margin'] = PnLStatYlyTbl.loc[i, 'EBITDA'] / PnLStatYlyTbl.loc[i, 'Revenue']  
    ###Added
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>Annual - BS,PL,CFS: KPIS - Key Financial Ratios</h3>", unsafe_allow_html=True)
    KPIYlyTbl_Disp = KPIYlyTbl.copy()
    KPIYlyTbl_Disp = KPIYlyTbl_Disp.round({col: 2 for col in KPIYlyTbl_Disp.select_dtypes(include='number').columns})
    st.dataframe(KPIYlyTbl_Disp.T)

with tab2:
    st.markdown("<br><h3 style='font-size:14px; text-align:left;'>CHARTS</h3>", unsafe_allow_html=True)
    st.title("Charts")
    dpi = 150
    col1, col2, col3 = st.columns(3)
    with col1:
        # FIG1: Debt to Equity, DSCR
        # st.subheader("Debt to Equity, DSCR")
        fig1, ax1 = plt.subplots(figsize=(6, 2.5))
        fig1.patch.set_facecolor('lightblue')  # Background of the figure
        ax1.set_facecolor('lightblue')         # Background of the plot area
        # Plotting the lines
        ax1.plot(KPIYlyTbl.index, KPIYlyTbl['Debt to EBITDA'], marker='', linestyle='-', label="Debt to EBITDA")
        ax1.plot(KPIYlyTbl.index, KPIYlyTbl['Debt Service Coverage Ratio'], marker='', linestyle='-', label="Debt Service Coverage Ratio")
        # Add value labels for each point
        for i, year in enumerate(KPIYlyTbl.index):
            ax1.text(year, KPIYlyTbl['Debt to EBITDA'].iloc[i] + 0.1, f"{KPIYlyTbl['Debt to EBITDA'].iloc[i]:.2f}", fontsize=5, ha='center', va='bottom')   # Adjust +0.1 to move the label slightly above the marker
            ax1.text(year, KPIYlyTbl['Debt Service Coverage Ratio'].iloc[i] + 0.1, f"{KPIYlyTbl['Debt Service Coverage Ratio'].iloc[i]:.2f}", fontsize=5, ha='center', va='bottom')
        # Axes and formatting
        ax1.set_xlabel("Year", fontsize=8)
        ax1.set_ylabel("D2E, DSCR", fontsize=8)
        ax1.set_title("Debt to Equity, DSCR", fontsize=9)
        # Legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        ax1.legend(lines1, labels1, loc='lower right', bbox_to_anchor=(1.0, -0.29), fontsize=6)
        # ax1.legend(lines1, labels1, loc='upper right', fontsize=6)
        # Ticks and grid
        ax1.tick_params(axis='both', labelsize=6)
        ax1.grid(True, axis='y')
        # fig1.tight_layout(pad=0)
        fig1.subplots_adjust(top=0.9, bottom=0.2, left=0.1, right=0.95)
        # st.pyplot(fig1)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig1, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig1.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
        # FIG2: LTV and Interest Coverage Ratio
        # st.subheader("LTV and Interest Coverage Ratio")
        fig2, ax2 = plt.subplots(figsize=(6, 2.5))
        fig2.patch.set_facecolor('lightblue')  # Background of the figure
        ax2.set_facecolor('lightblue')         # Background of the plot area
        # Plot Interest Coverage Ratio on left y-axis
        ax2.plot(KPIYlyTbl.index, KPIYlyTbl['Interest Coverage Ratio'], marker='', linestyle='-', color='tab:orange', label="Interest Coverage Ratio")
        ax2.set_xlabel("Year", fontsize=8)
        ax2.set_ylabel("Interest Coverage Ratio", color='tab:orange', fontsize=8)
        # Create second y-axis for LTV
        ax22 = ax2.twinx()
        ax22.plot(KPIYlyTbl.index, KPIYlyTbl['Loan to Value (Tangible Asset) Ratio'], marker='', linestyle='-', color='tab:blue', label="Loan to Value (Tangible Asset) Ratio")
        ax22.set_ylabel("Loan to Value (Tangible Asset) Ratio", color='tab:blue', fontsize=8)
        # Add value labels for Interest Coverage Ratio
        for i, year in enumerate(KPIYlyTbl.index):
            val = KPIYlyTbl['Interest Coverage Ratio'].iloc[i]
            ax2.text(year, val + 0.1, f"{val:.2f}", fontsize=5, color='black', ha='center', va='bottom')
        # Add value labels for LTV
        for i, year in enumerate(KPIYlyTbl.index):
            val = KPIYlyTbl['Loan to Value (Tangible Asset) Ratio'].iloc[i]
            ax22.text(year, val + 0.1, f"{val:.2f}", fontsize=5, color='black', ha='center', va='bottom')
        # Title and legend
        ax2.set_title("LTV and Interest Coverage Ratio", fontsize=9)
        lines2, labels2 = ax2.get_legend_handles_labels()
        lines22, labels22 = ax22.get_legend_handles_labels()
        ax2.legend(lines2 + lines22, labels2 + labels22, loc='lower right', bbox_to_anchor=(1.0, -0.29), fontsize=6)
        # ax2.legend(lines2 + lines22, labels2 + labels22, loc='upper right', fontsize=6)
        # Axis formatting
        ax2.tick_params(axis='both', labelsize=6)
        ax22.tick_params(axis='y', labelsize=6)
        ax2.grid(True, axis='y')
        # fig2.tight_layout(pad=0)
        fig2.subplots_adjust(top=0.9, bottom=0.2, left=0.09, right=0.92)
        # st.pyplot(fig2)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig2, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig2.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
        # FIG3: Debt to Equity Ratio, Operating Margin
        # st.subheader("Debt to Equity Ratio, Operating Margin")
        fig3, ax3 = plt.subplots(figsize=(6, 2.5))
        fig3.patch.set_facecolor('lightblue')  # Background of the figure
        ax3.set_facecolor('lightblue')         # Background of the plot area
        # Plot Operating Margin on primary y-axis
        ax3.plot(KPIYlyTbl.index, KPIYlyTbl['Operating Margin'], marker='', linestyle='-', color='tab:orange', label="Operating Margin")
        ax3.set_xlabel("Year", fontsize=8)
        ax3.set_ylabel("Operating Margin", color='tab:orange', fontsize=8)
        ax3.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))  # Convert to percentage format
        # Plot Debt to Equity Ratio on secondary y-axis
        ax32 = ax3.twinx()
        ax32.plot(KPIYlyTbl.index, KPIYlyTbl['Debt to Equity Ratio'], marker='', linestyle='-', color='tab:blue', label="Debt to Equity Ratio")
        ax32.set_ylabel("Debt to Equity Ratio", color='tab:blue', fontsize=8)
        # Add value labels for Operating Margin
        for i, year in enumerate(KPIYlyTbl.index):
            val = KPIYlyTbl['Operating Margin'].iloc[i]
            ax3.text(year, val + 0.01, f"{val * 100:.1f}%", fontsize=5, color='black', ha='center', va='bottom')
        # Add value labels for Debt to Equity Ratio
        for i, year in enumerate(KPIYlyTbl.index):
            val = KPIYlyTbl['Debt to Equity Ratio'].iloc[i]
            ax32.text(year, val + 0.1, f"{val:.2f}", fontsize=5, color='black', ha='center', va='bottom')
        # Title and legend
        ax3.set_title("Debt to Equity Ratio, Operating Margin", fontsize=9)
        lines3, labels3 = ax3.get_legend_handles_labels()
        lines32, labels32 = ax32.get_legend_handles_labels()
        ax3.legend(lines3 + lines32, labels3 + labels32, loc='lower right', bbox_to_anchor=(1.0, -0.29), fontsize=6)
        # ax3.legend(lines3 + lines32, labels3 + labels32, loc='upper right', fontsize=6)
        # Tick labels and grid
        ax3.tick_params(axis='both', labelsize=6)
        ax32.tick_params(axis='y', labelsize=6)
        ax3.grid(True, axis='y')
        # fig3.tight_layout(pad=0)
        fig3.subplots_adjust(top=0.9, bottom=0.2, left=0.09, right=0.92)
        # st.pyplot(fig3)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig3, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig3.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
    with col2:
        # FIG4: Bar Chart for Revenue and EBITDA
        bar_width = 0.35
        x_indices = np.arange(len(PnLStatYlyTbl.index))
        fig4, ax4 = plt.subplots(figsize=(6, 2.5))
        fig4.patch.set_facecolor('lightblue')
        ax4.set_facecolor('lightblue')
        ax4.set_axisbelow(True)
        ax4.grid(True, axis='y', zorder=0)
        # Plot bars with zorder > grid
        revenue_bars = ax4.bar(x_indices - bar_width / 2, PnLStatYlyTbl['Revenue'], bar_width, label="Revenue", color='blue', zorder=1)
        ebitdaLst = [PnLStatYlySr['EBITDA']]
        for i in range(len(PnLStatYlyTbl['EBITDA']) - 1):
            ebitdaLst.append(PnLStatYlyTbl['EBITDA'].iloc[i])
        ebitda_bars = ax4.bar(x_indices + bar_width / 2, np.array(ebitdaLst), bar_width, label="EBITDA", color='orange', zorder=1)
        # Add value labels
        for bar in revenue_bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.0f}', ha='center', va='bottom', fontsize=3)
        for bar in ebitda_bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.0f}', ha='center', va='bottom', fontsize=3)
        # Formatting
        ax4.set_xlabel("Year", fontsize=8)
        ax4.set_ylabel("Revenue, EBITDA", fontsize=8)
        ax4.set_title("Revenue and EBITDA", fontsize=9)
        ax4.set_xticks(x_indices)
        ax4.set_xticklabels(PnLStatYlyTbl.index)
        lines4, labels4 = ax4.get_legend_handles_labels()
        ax4.legend(lines4, labels4, loc='lower right', bbox_to_anchor=(1.0, -0.29), fontsize=6)
        # ax4.legend(lines4, labels4, loc='upper right', fontsize=6)
        ax4.tick_params(axis='both', labelsize=6)
        # fig4.tight_layout(pad=0)
        fig4.subplots_adjust(top=0.9, bottom=0.2, left=0.12, right=0.95)
        # st.pyplot(fig4)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig4, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig4.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
        # FIG5: Outstanding Debt Balance and Interest Paid
        x = np.arange(len(BSYlyTbl.index))  # Numeric x positions
        fig5, ax5 = plt.subplots(figsize=(6, 2.5))
        fig5.patch.set_facecolor('lightblue')
        ax5.set_facecolor('lightblue')
        bar_width = 0.35
        # Line plots (Primary y-axis)
        ax5.plot(x, BSYlyTbl['Senior Secured'], label='Senior Secured', marker='', color='blue', linewidth=2)
        ax5.plot(x, BSYlyTbl['Debt 1 - Tranche 1'], label='Debt 1 - Tranche 1', marker='', color='orange', linewidth=2)
        # Secondary y-axis for the bar chart
        ax52 = ax5.twinx()
        bars = ax52.bar(x, CFSYlyTbl['Interest Paid'], width=bar_width, label='Interest Paid', color='green')
        # Set both y-axes to start at 0
        ax5.set_ylim(bottom=0)
        ax52.set_ylim(bottom=0)
        # Axes formatting
        ax5.tick_params(axis='both', labelsize=6)
        ax52.tick_params(axis='y', labelsize=6)
        ax5.set_xticks(x)
        ax5.set_xticklabels(BSYlyTbl.index)
        ax5.set_xlabel("Year", fontsize=8)
        ax5.set_ylabel("Senior Secured/Debt Tranche")
        ax52.set_ylabel("Interest Paid", color='tab:green')
        # Combine legends from both axes
        lines1, labels1 = ax5.get_legend_handles_labels()
        lines2, labels2 = ax52.get_legend_handles_labels()
        ax5.legend(lines1 + lines2, labels1 + labels2, loc='lower right', bbox_to_anchor=(1.0, -0.39), fontsize=6)
        # ax5.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=6)
        ax5.grid(True, axis='y')
        ax5.set_title("Outstanding Debt Balance and Interest Paid", fontsize=9)
        fig5.subplots_adjust(top=0.9, bottom=0.25, left=0.1, right=0.91)
        # st.pyplot(fig5)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig5, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig5.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
        # FIG6: Cash, PPE and Total Equity Balance
        fig6, ax6 = plt.subplots(figsize=(6, 2.5)) 
        fig6.patch.set_facecolor('lightblue')
        ax6.set_facecolor('lightblue')
        bar_width = 0.35
        eqtyEarnLst = BSYlyTbl['Equity'] + BSYlyTbl['Retained Earning']
        # Secondary y-axis
        ax62 = ax6.twinx()
        ax62.set_axisbelow(True)
        ax62.grid(True, axis='y', zorder=0)
        bars = ax62.bar(x, BSYlyTbl['Cash'], width=bar_width, label='Cash', color='blue', zorder=1)
        # Bring ax6 to the front and hide its background patch
        ax6.set_zorder(2)
        ax6.patch.set_visible(False)
        # Plot lines on ax6 — these now appear in front
        ax6.plot(x, eqtyEarnLst, label='Total Equity (with retained earnings)', color='orange', linewidth=2, zorder=3)
        ax6.plot(x, BSYlyTbl['Property, Plant & Equipment (Net)'], label='Property, Plant & Equipment (Net)', color='red', linewidth=2, zorder=3)
        # Axes formatting
        ax6.set_xticks(x)
        ax6.set_xticklabels(BSYlyTbl.index)
        ax6.set_xlabel("Year", fontsize=8)
        ax6.set_ylabel("Total Equity/PPE")
        ax62.set_ylabel("Cash", color='tab:blue')
        ax6.tick_params(axis='both', labelsize=6)
        ax62.tick_params(axis='y', labelsize=6)
        ax6.set_ylim(bottom=0)
        ax62.set_ylim(bottom=0)
        # Combine legends
        lines1, labels1 = ax6.get_legend_handles_labels()
        lines2, labels2 = ax62.get_legend_handles_labels()
        ax6.legend(lines1 + lines2, labels1 + labels2, loc='lower right', bbox_to_anchor=(1.0, -0.39), fontsize=6)
        # ax6.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=6)
        ax6.set_title("Cash, PPE and Total Equity Balance", fontsize=9)
        fig6.subplots_adjust(top=0.9, bottom=0.25, left=0.12, right=0.88)
        # st.pyplot(fig6)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig6, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig6.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
    with col3:
        # FIG7: Gross Profit, EBITDA, Net Profit - as % of Revenue
        fig7, ax7 = plt.subplots(figsize=(6, 2.5))
        fig7.patch.set_facecolor('lightblue')  # Background of the figure
        ax7.set_facecolor('lightblue')         # Background of the plot area
        gpft2revLst = PnLStatYlyTbl['Gross Profit'] / PnLStatYlyTbl['Revenue']
        ebitda2revLst = PnLStatYlyTbl['EBITDA'] / PnLStatYlyTbl['Revenue']
        ninc2revLst = PnLStatYlyTbl['Net Income'] / PnLStatYlyTbl['Revenue']
        # Plot Interest Coverage Ratio on left y-axis
        ax7.plot(PnLStatYlyTbl.index, gpft2revLst, marker='', linestyle='-', color='tab:blue', label="Gross Profit (% of Revenue)")
        ax7.plot(PnLStatYlyTbl.index, ebitda2revLst, marker='', linestyle='-', color='tab:orange', label="EBITDA (% of Revenue)")
        ax7.plot(PnLStatYlyTbl.index, ninc2revLst, marker='', linestyle='-', color='tab:green', label="Net Income (% of Revenue)")
        ax7.set_xlabel("Year", fontsize=8)
        ax7.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))  # Convert to percentage format
        # Title and legend
        ax7.set_title("Gross Profit, EBITDA, Net Profit - as % of Revenue", fontsize=9)
        lines7, labels7 = ax7.get_legend_handles_labels()
        ax7.legend(lines7, labels7, loc='lower right', bbox_to_anchor=(1.0, -0.39), fontsize=6)
        # Axis formatting
        ax7.tick_params(axis='both', labelsize=6)
        ax7.grid(True, axis='y')
        fig7.subplots_adjust(top=0.9, bottom=0.25, left=0.06, right=0.96)
        # st.pyplot(fig7)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig7, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig7.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
        # FIG8: AR and Inventory Cycle Days
        fig8, ax8 = plt.subplots(figsize=(6, 2.5))
        fig8.patch.set_facecolor('lightblue')
        ax8.set_facecolor('lightblue')
        ar2revLst = 365 * BSYlyTbl['Accounts Receivable'] / PnLStatYlyTbl['Revenue']
        inv2cogs = 365 * BSYlyTbl['Inventory'] / -PnLStatYlyTbl['Cost of Goods Sold']
        cogsLst = -PnLStatYlyTbl['Cost of Goods Sold']
        # Secondary y-axis for bars
        ax82 = ax8.twinx()
        # ax82.grid(True, axis='y', zorder=1)
        bar_width = 0.35
        x_indices = PnLStatYlyTbl.index
        # Plot bars on ax82 with zorder=1
        ax82.bar(x_indices - bar_width/2, PnLStatYlyTbl['Revenue'], bar_width, label="Revenue", color='green', zorder=3)
        ax82.bar(x_indices + bar_width/2, np.array(cogsLst), bar_width, label="COGS", color='blue', zorder=3)
        ax82.set_ylabel("Revenue / COGS", fontsize=8)
        ax82.set_ylim(bottom=0)
        # Plot lines on ax8 with zorder=3
        ax8.plot(PnLStatYlyTbl.index, ar2revLst, linestyle='-', color='tab:blue', label="AR Cycle Days")
        ax8.plot(PnLStatYlyTbl.index, inv2cogs, linestyle='-', color='tab:orange', label="Inventory Cycle Days")
        ax8.set_xlabel("Year", fontsize=8)
        ax8.set_ylabel("AR/Inventory Cycle Days", fontsize=8)
        ax8.set_ylim(bottom=0)
        # Bring ax8 forward, hide background so bars stay visible
        ax8.set_zorder(2)
        ax8.patch.set_visible(False)
        # Title and legend
        ax8.set_title("AR and Inventory Cycle Days", fontsize=9)
        lines8, labels8 = ax8.get_legend_handles_labels()
        lines82, labels82 = ax82.get_legend_handles_labels()
        ax8.legend(lines8 + lines82, labels8 + labels82, loc='lower right', bbox_to_anchor=(1.0, -0.52), fontsize=6)
        # Formatting
        ax8.tick_params(axis='both', labelsize=6)
        ax82.tick_params(axis='y', labelsize=6)
        fig8.subplots_adjust(top=0.9, bottom=0.3, left=0.07, right=0.9)
        # st.pyplot(fig8)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig8, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig8.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
        # FIG9: Key Ratios
        fig9, ax9 = plt.subplots(figsize=(6, 2.5))
        fig9.patch.set_facecolor('lightblue')
        ax9.set_facecolor('lightblue')
        bar_width = 0.35  # Define bar width if not already done
        ax9.grid(True, axis='y', zorder=0)
        ax9.bar(KPIYlyTbl.index - bar_width / 2, KPIYlyTbl['Debt Service Coverage Ratio'], bar_width, label="Debt Service Coverage Ratio", color='orange', zorder=2)
        # Axis labels and limits
        ax9.set_xlabel("Year", fontsize=8)
        ax9.set_ylabel("Debt Service Coverage Ratio", fontsize=8)
        ax9.set_ylim(bottom=0)
        ax92 = ax9.twinx()
        ax92.plot(KPIYlyTbl.index, KPIYlyTbl['Debt to EBITDA'], linestyle='-', color='tab:blue', label="Debt to EBITDA",zorder=3)
        ax92.plot(KPIYlyTbl.index, KPIYlyTbl['Debt to Equity Ratio'], linestyle='-', color='tab:green', label="Debt to Equity Ratio", zorder=3)
        ax92.set_ylabel("Debt to EBITDA / Debt to Equity", fontsize=8)
        ax92.set_ylim(bottom=0)
        ax92.patch.set_visible(False)
        # Title and combined legend
        ax9.set_title("Key Ratios", fontsize=9)
        lines9, labels9 = ax9.get_legend_handles_labels()
        lines92, labels92 = ax92.get_legend_handles_labels()
        ax9.legend(lines9 + lines92, labels9 + labels92, loc='lower right', bbox_to_anchor=(1.0, -0.39), fontsize=6)
        # Formatting
        ax9.tick_params(axis='both', labelsize=6)
        ax92.tick_params(axis='y', labelsize=6)
        fig9.subplots_adjust(top=0.9, bottom=0.25, left=0.08, right=0.92)
        # st.pyplot(fig9)
        # st.markdown("<div style='height:300px;'>", unsafe_allow_html=True)
        # st.pyplot(fig9, use_container_width=True)
        # st.markdown("</div>", unsafe_allow_html=True)
        buf = io.BytesIO()
        fig9.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        st.image(buf, use_container_width=True)
    
with tab3:
    st.title("Refinancing Model Report")
    try:
        user_api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError as e:
        user_api_key =  st.text_input("Enter your Gemini API Key", type="password")

    dataframes = []
    tables = [pl_df,balance_df,result_table,debtCalc_SenSec.T,debtCalc_StTerm.T,totDebtCalc.T,projectionDF.T,depSchedCalcTbl_Disp.T,PnLStatTbl_Disp.T,PnLStatMtlyTbl_Disp.T,BSYlyTbl_Disp.T,CFSMtlyTbl_Disp.T,KPIMtlyTbl_Disp.T,PnLStatYlyTbl_Disp.T,BSYlyTbl_Disp.T,CFSYlyTbl_Disp.T,KPIYlyTbl_Disp.T]
    table_names= ['Statement of Profit and Loss','Balance Sheet','Result Table'
    ,'Depreciation Schedule DEBT CALC','Depreciation Schedule DEBT CALC','Depreciation Schedule DEBT CALC','Depreciation Schedule DEBT CALC'
    ,'Depreciation Schedule','Debt Calculations'
    ,'Monthly - BS,PL,CFS: Table A','Monthly - BS,PL,CFS: Table B','Monthly - BS,PL,CFS: Table C'
    ,'Monthly - BS,PL,CFS: KPIS - Key Financial Ratios'
    ,'Annual - BS,PL,CFS: Table A','Annual - BS,PL,CFS: Table B','Annual - BS,PL,CFS: Table C'
    ,'Annual - BS,PL,CFS: KPIS - Key Financial Ratios']

    result_set = dict(zip(table_names, tables))
    for x,y in result_set.items():
        dataframes.append({"name": x, "data": y.to_dict(orient="records")})

    json_output = json.dumps(dataframes, indent=2)

    if user_api_key:
        genai.configure(api_key=user_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        # prompt = st.text_area("Enter your question or prompt for Flash")
        prompt = f"Give a Refinancing advisory report based the below tables {json_output}"

        if st.button("Generate Report"):
            if prompt:
                with st.spinner("Your Report is being generated..."):
                    try:
                        response = model.generate_content(prompt)
                        st.success("Report generation successful!")
                        st.write(response.text)
                    except requests.exceptions.HTTPError as http_err:
                        if response.status_code == 400 and "API_KEY_INVALID" in response.text:
                            st.error("❌ Invalid API key. Please check your key and try again.")
                        else:
                            st.error(f"HTTP error occurred: {http_err}")

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                st.session_state.loading = False
                                            
            else:
                st.warning("Please enter a prompt.")
