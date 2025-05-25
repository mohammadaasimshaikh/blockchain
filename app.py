from flask import Flask, render_template, request, redirect
from blockchain import Blockchain

app = Flask(__name__)
my_chain = Blockchain()

@app.route('/')
def home():
    return render_template('index.html', chain=my_chain.chain)

@app.route('/add', methods=['POST'])
def add_block():
    transactions = []
    transaction_data = request.form.getlist('transaction')
    for data in transaction_data:
        sender, receiver, amount = data.split(",")
        transactions.append({
            'sender': sender.strip(),
            'receiver': receiver.strip(),
            'amount': float(amount.strip())
        })
    my_chain.add_block(transactions)
    return redirect('/')

@app.route('/reset', methods=['GET'])
def reset_blockchain():
    global my_chain
    my_chain = Blockchain()
    return redirect('/')

@app.route('/block', methods=['GET'])
def search_block():
    index = int(request.args.get('index'))
    if index < len(my_chain.chain):
        block = my_chain.chain[index]
        return render_template('block_details.html', block=block)
    else:
        return "Block not found!"

@app.route('/tamper/<int:index>', methods=['GET'])
def tamper(index):
    success = my_chain.tamper_block(index)
    if success:
        return redirect('/')
    else:
        return "Cannot tamper with this block!", 400

if __name__ == "__main__":
    app.run(debug=True)
