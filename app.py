from flask import Flask, render_template, request
import braintree

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    'qr7h9y9634y43hy3',
    '8wtdvybw5yht6crc',
    'c3bf46039e4b5589f65a5b1235c07857'
)

app = Flask(__name__)

@app.route("/")
def index():
    client_token = braintree.ClientToken.generate()
    # return client_token
    return render_template('index.html', client_token=client_token)

@app.route("/checkout", methods=["POST"])
def checkout():
    payment_method_nonce = request.form["payment_method_nonce"]
    first_name = request.form["first_name"]
    email = request.form["email"]
    amount = request.form["amount"]

    customer = braintree.Customer.create ({
        'payment_method_nonce': payment_method_nonce,
        'first_name': first_name,
        'email': email
    })

    token = customer.customer.payment_methods[0].token

    result = braintree.Transaction.sale({
        'amount': amount,
        'payment_method_token': token
    })

    if result.transaction.processor_response_text == "Processor Declined":
        return render_template("declined.html", result=result)

    # return payment_method_nonce
    # result = braintree.Transaction.sale({
    #     'amount':'10',
    #     'payment_method_nonce':payment_method_nonce,
    #     'customer': {
    #         'first_name':first_name,
    #         'email':email
    #     }
    # })

    return render_template('checkout.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
