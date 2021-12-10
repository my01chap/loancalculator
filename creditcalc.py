import math
import argparse


def type_diff(arr):
    principal = arr.get('principal', None)
    periods = arr.get('periods', None)
    interest = arr.get('interest', None)
    return calculate(arr['type'], interest, principal, periods)


def type_annuity(arr):
    action = determine_action(arr)
    principal = arr.get('principal', None)
    periods = arr.get('periods', None)
    interest = arr.get('interest', None)
    payment = arr.get('payment', None)
    return calculate(arr['type'], interest, principal, periods,
                     payment, action)


def determine_action(arr):
    if 'periods' not in arr:
        action = 'n'
        return action
    elif 'payment' not in arr:
        action = 'a'
        return action
    else:
        action = 'p'
        return action


def argument_correct(arr):
    negative = False

    for arg, v in arr.items():
        if arg != 'type' and v is not None:
            if float(v) < 0:
                negative = True
                break

    if len(arr) != 4:
        return False, "Incorrect Number of arguments provided"
    # Omitted type option
    elif arr['type'] is None:
        return False, "Provide --type option e.g --type=annuity" \
                      " or --type=diff"
    # Incorrect type value
    elif arr['type'].lower() != "annuity" and arr['type'].lower()\
            != "diff":
        return False, "Incorrect --type option value"
    # Omitted interest argument or interest value provided as percentage
    elif 'interest' not in arr or float(arr['interest']) < 1:
        return False, "Provide correct interest argument value"
    # Negative arguments
    elif negative:
        return False, "Provide positive argument values"
    # Incompatible option combination e.g type=diff and payment
    elif args['type'].lower() == 'diff' and 'payment' in args:
        return False, "Incompatible argument combination"
    # Incomplete options provided for type = diff
    elif args['type'].lower() == 'diff' and \
            (args['principal'] is None or args['periods'] is None):
        return False, "Incorrect Number of arguments provided"
    else:
        return True, " "


def calculate(types, interest, principal=None,
              periods=None, payment=None, action=None):
    def overpayment(p, n, i):
        aggregate = 0
        for y in range(n):
            differentiated_payment = math.ceil(
                (p / n) + i *
                (p - ((p * (y + 1 - 1)) /
                      n)))
            aggregate += differentiated_payment

        return aggregate - p

    def print_overpayment(amount):
        print("Overpayment = {0}".format(amount))

    i = (interest * .01) / 12

    if action is None:
        overpayments = overpayment(principal, periods, i)

    if types == 'diff':

        for x in range(periods):
            d_payment = math.ceil(
                (principal / periods) + i *
                (principal - ((principal * (x + 1 - 1)) / periods)))
            print("Month {0}: payment is {1}".format(
                x + 1, d_payment))

        print_overpayment(overpayments)
    else:
        if action == 'n':
            loan_p = principal
            monthly_p = payment

            base = 1 + i
            power = monthly_p / (monthly_p - i * loan_p)
            n = math.ceil(math.log(abs(power), base))
            overpayments = math.ceil((monthly_p * n) - loan_p)
            # n a factor of 12
            if n % 12 == 0:
                year = n // 12
                if year > 1:
                    print("It will take {0} years to repay this "
                          "loan!".format(year))
                    print_overpayment(overpayments)
                else:
                    print("It will take {0} year to repay this "
                          "loan".format(year))
                    print_overpayment(overpayments)
            elif n < 12:
                if n == 1:
                    print("It will take {0} month to repay this "
                          "loan!".format(n))
                    print_overpayment(overpayments)
                else:
                    print("It will take {0} months to repay this "
                          "loan".format(n))
                    print_overpayment(overpayments)
            else:
                years = n // 12
                months = n - (years * 12)
                if years > 1:
                    if months > 1:
                        print("It will take {0} years and {1} months "
                              "to repay this loan!".format(
                               years, months))
                        print_overpayment(overpayments)
                    else:
                        print("It will take {0} years and {1} month "
                              "to repay this loan!".format(
                               years, months))
                        print_overpayment(overpayments)
                else:
                    if months > 1:
                        print("It will take {0} year and {1} months "
                              "to repay this loan!".format(
                               years, months))
                        print_overpayment(overpayments)
                    else:
                        print("It will take {0} year and {1} month to "
                              "repay this loan".format(
                               years, months))
                        print_overpayment(overpayments)
        elif action == 'a':
            loan_p = principal
            periods = periods

            numerator = i * math.pow(1 + i, periods)
            denominator = math.pow(1 + i, periods) - 1
            annuity = math.ceil(loan_p * (numerator / denominator))

            print("Your annuity payment = {0}!".format(annuity))
            print_overpayment(
                math.ceil((annuity * periods) - loan_p))
        else:
            annuity = payment
            periods = periods

            numerator = i * math.pow(1 + i, periods)
            denominator = math.pow(1 + i, periods) - 1
            principal = math.floor(annuity / (
                    numerator / denominator))

            print("Your loan principal = {0}!".format(principal))
            print_overpayment(
                math.ceil((annuity * periods) - principal))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This program allows you calculate annuity"
                    " information based on provided inputs. "
                    "Annuity information to calculate could be "
                    "any of: Annuity payments, "
                    "differentiated annuity payments, the number "
                    "of monthly payments and the loan principal "
                    "amount.")

    # Add positional arguments; --type and --interest, which are required
    parser.add_argument("-it", "--type",
                        choices=["annuity", "diff"],
                        help="You need to choose only one "
                             "option from the list.")
    parser.add_argument("-iy", "--interest",
                        help='a float value used as the '
                             'interest rate', type=float)

    # Add optional arguments for annuity type. Note that these are not optional
    # for diff type
    parser.add_argument("-ip", "--principal",
                        help='an integer value used as '
                             'the principal amount', type=int)
    parser.add_argument("-in", "--periods",
                        help='an integer used as the number '
                             'of months', type=int)
    parser.add_argument("-ia", "--payment",
                        help='a float value used as the '
                             'annuity amount paid each period',
                        type=float)

    # Parse and collect arguments
    raw_args = vars(parser.parse_args())
    args = {}
    for k, v in raw_args.items():
        if v is not None:
            args[k] = v

    error_eval, error_val = argument_correct(args)
    if not error_eval:
        print("{}".format(error_val))
    else:
        if args['type'].lower() == 'diff':
            type_diff(args)
        else:
            type_annuity(args)
