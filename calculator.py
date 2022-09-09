# Import models
import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_js
import locale

# Set theme
pywebio.config(theme="sketchy")

# Set currency
locale.setlocale( locale.LC_ALL, 'en_US.utf-8')

# Information to be displayed
DisclaimerInfo = "Yawdie Code DOES NOT guarantee that any information presented by this application is accurate, complete or up-to-date; and DOES NOT accept responsibility for any financial decisions made, including any financial losses incurred, based on the information in this application. For legal or financial advice, consult a qualified lawyer or financial adviser."
CalculatorInfo = "Use this simple calculator to get an estimate of your take-home pay and total tax deductions based on your gross annual salary in Jamaican Dollars. Please note that this calculator does not currently consider pro-rata salaries, pensions contributions, overtime, or bonuses."

def PAYEInfo():
    popup('What is PAYE?',[
        put_text("Individuals who legally live and work in Jamaica pay income tax through PAYE, which stands for ‘Pay As You Earn’. There’s an annual tax-free threshold of JM$1.5 million after which the rate is 25% on the excess up to JM$6 million. All excess over JM$6 million is charged at a rate of 30%."),
        put_link('Read more', 'https://taxsummaries.pwc.com/jamaica/individual/taxes-on-personal-income', new_window=True),
        put_buttons(['Close'], onclick=lambda _: close_popup())
    ])

def NHTInfo():
    popup('What are NHT contributions?',[
        put_text("NHT stands for National Housing Trust, an agency that provides low interest rate loans to contributors who wish to build, buy or repair their houses. Employees contribute at a rate of 2% on their gross income."),
        put_link('Read more', 'https://taxsummaries.pwc.com/jamaica/individual/other-taxes', new_window=True),
        put_buttons(['Close'], onclick=lambda _: close_popup())
    ])

def NISInfo():
    popup('What are NIS contributions?',[
        put_text("NIS stands for National Insurance Scheme, a compulsory contributory funded social security scheme that applies to all employed persons in Jamaica. As an employee, you are required to contribute at a rate of 3% on a maximum remuneration of JM$1.5 million per year therefore the most you could pay in one year is JM$45,000."),
        put_link('Read more', 'https://www.mlss.gov.jm/departments/national-insurance-scheme/#1558985883846-cbb93e25-bdb3', new_window=True),
        put_buttons(['Close'], onclick=lambda _: close_popup())
    ])

def EducationTaxInfo():
     popup('What is Education Tax?',[
        put_text("Education Tax, as the name suggests, is levied to advance education in Jamaica. Employees are charged at a rate of 2.25% after NIS and pension deductions."),
        put_link('Read more', 'https://taxsummaries.pwc.com/jamaica/individual/other-taxes', new_window=True),
        put_buttons(['Close'], onclick=lambda _: close_popup())
    ])

# Tax rates
paye_threshold1 = 1500000
paye_threshold2 = 6000000
nis_rate = 0.03
nis_threshold = paye_threshold1 * nis_rate
nht_rate = 0.02
education_rate = 0.0225
paye_rate1 = 0.25
paye_rate2 = 0.30

# Function to calculate take-home pay and salary deductions
def RunCalculator():
    clear('B')
    with use_scope('B'):
        # Retrieve user input
        gross = input("Input your gross annual salary (JMD): ", type=FLOAT)
        
        # Make calculations
        taxable_income = gross - paye_threshold1
        nis_amount = gross * nis_rate
        nht = gross * nht_rate

        if nis_amount >= nis_threshold:
            nis = nis_threshold
        
        else:
            nis = nis_amount

        education = (gross - nis) * education_rate

        if taxable_income >= paye_threshold2:
            paye = taxable_income * paye_rate2

        elif taxable_income > 0:
            paye = taxable_income * paye_rate1
        
        else:
            paye = 0

        total_deductions = nht + nis + education + paye
        net_income = gross - total_deductions
        monthly_income = net_income/12
 
        # Display info to user
        put_table([
            [span('RESULTS (JMD)', col=2)],
            ['Gross', put_text(locale.currency(gross, grouping=True))],
            ['Net', put_text(locale.currency(net_income, grouping=True))],
            ['Monthly Take-home', put_text(locale.currency(monthly_income, grouping=True))]
            ])
            
        put_table([
            [span('DEDUCTIONS (JMD)', col=2)],
            ['Income Tax', put_text(locale.currency(paye, grouping=True))],
            ['NIS', put_text(locale.currency(nis, grouping=True))],
            ['NHT', put_text(locale.currency(nht, grouping=True))],
            ['Education', put_text(locale.currency(education, grouping=True))],
            ['Total Deductions', put_text(locale.currency(total_deductions, grouping=True))]
            ])
        
        put_text(f'DISCLAIMER: {DisclaimerInfo}')

# Function to perform calculation in app
def calculator():
    with use_scope('A'):
        put_image(open('ja_salary_calculator.jpg', 'rb').read())
        
        put_tabs([
                    {'title': 'CALCULATOR', 'content': [
                    put_text(CalculatorInfo),
                    put_button('Start', color='success', onclick=RunCalculator)
                    ]},
                    {'title': 'ABOUT', 'content': [
                    put_text("Learn about the tax deductions applicable to individuals in Jamaica:"),
                    put_buttons(
                        ['PAYE','NHT', 'NIS', 'Education Tax'],
                        onclick=[PAYEInfo, NHTInfo, NISInfo, EducationTaxInfo])
                    ]},
                    {'title': 'MORE INFO', 'content': [
                    put_text("For more information about this project, visit my GitHub profile:"),
                    put_link('MlleGeorgette', 'https://github.com/MlleGeorgette/Jamaica-Salary-Calculator', new_window=True)
                ]},
                ])

if __name__ == '__main__':
    pywebio.start_server(calculator, port=8080, debug=True, remote_access=False)
