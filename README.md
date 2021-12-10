# loancalculator

The loancalculator module written in python does the following core actions:
  * Calculates a loan ordinary annuity payment
  * Calculates the differentiated payments of a loan
  
 For each action above, the overpayment is also calculated

## annuity payment

For annuity payment which is fixed during the whole loan term the following formula is used:

A = P ∗ i ∗ ( 1 + i )**n ( 1 + i )**n − 1

Where:

A = annuity payment;

P = loan principal;

i = nominal (monthly) interest rate. Usually, it’s 1/12 of the annual interest rate, and usually, it’s a floating value, not a percentage. For example, if your annual interest rate = 12%, then i = 0.01;

n = number of payments. This is usually the number of months in which repayments will be made.

**You are interested in four values: the number of monthly payments required to repay the loan, the monthly payment amount, the loan principal, and the loan interest. Each of these values can be calculated if others are known:**

Loan principal:

P = A / ( i ∗ ( 1 + i )**n / ( 1 + i )**n − 1)

The number of payments:

n = log1 + i (A / A − i ∗ P)

Thus with annuity payment, given the provided variables, the loan principal (p) or the number of payments (n) or annuity payment (A) can be determined

## differentiated payment

For differentiated payments, the loan principal is reduced by a constant amount each month. The rest of the monthly payment goes toward interest repayment and it is gradually reduced over the term of the loan. This means that the payment is different each month.
The formula used:

Dm = (P / n) + i ∗ ( P − (P ∗ ( m − 1 )) / n)

Where:

Dm = mth differentiated payment;

P = the loan principal;

i = nominal interest rate. This is usually 1/12 of the annual interest rate, and it’s usually a float value, not a percentage. For example, if our annual interest rate = 12%, then i = 0.01.

n = number of payments. This is usually the number of months in which repayments will be made.

m = current repayment month.

Thus with differentiated payments, the respective different payments for each period in (n) is cakculated.

## Operation

To loancalculator module (creditcalc.py) is run from the command line with atleast four argument options as follows:

  * --type indicates the type of payment: "annuity" or "diff" (differentiated). If --type is specified neither as "annuity" nor as "diff" or not specified at all, the module run will fail
  
  * --payment is the monthly payment amount. For --type=diff, the payment is different each month, so we can't calculate months or principal, therefore a combination with --payment is invalid
  
  * --payment is the monthly payment amount. For --type=diff, the payment is different each month, so we can't calculate months or principal, therefore a combination with --payment is invalid
  
  * --principal is used for calculations of both types of payment. You can get its value if you know the interest, annuity payment, and number of months.
  
  * --periods denotes the number of months needed to repay the loan. It's calculated based on the interest, annuity payment, and principal.
  
  * --interest is specified without a percent sign. **Note that it can accept a floating-point value. The loancalculator can't calculate the interest, so it must always be provided**

The examples below demonstrate a couple cases of the creditcalc.py module run with arguments:

### Example 1: calculating differentiated payments

> python creditcalc.py --type=diff --principal=1000000 --periods=10 --interest=10

Month 1: payment is 108334

Month 2: payment is 107500

Month 3: payment is 106667

Month 4: payment is 105834

Month 5: payment is 105000

Month 6: payment is 104167

Month 7: payment is 103334

Month 8: payment is 102500

Month 9: payment is 101667

Month 10: payment is 100834

Overpayment = 45837

### Example 2: calculate the annuity payment for a 60-month (5-year) loan with a principal amount of 1,000,000 at 10% interest

> python creditcalc.py --type=annuity --principal=1000000 --periods=60 --interest=10

Your annuity payment = 21248!

Overpayment = 274880

### Example 3: calculate the principal for a user paying 8,722 per month for 120 months (10 years) at 5.6% interest

> python creditcalc.py --type=annuity --payment=8722 --periods=120 --interest=5.6

Your loan principal = 800018!

Overpayment = 246622

### Example 4: fewer than four arguments are given

> python creditcalc.py --type=diff --principal=1000000 --payment=104000

Incorrect Number of arguments provided



