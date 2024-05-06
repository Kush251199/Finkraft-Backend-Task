import csv
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('postgresql://username:password@localhost/db_name')
Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    TransactionID = Column(String, primary_key=True)
    CustomerName = Column(String)
    TransactionDate = Column(Date)
    Amount = Column(Float)
    Status = Column(String)
    InvoiceURL = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        transactions = csv.DictReader(file)
        session = Session()
        existing_ids = set()
        for row in transactions:
            transaction_id = row['TransactionID']
            if transaction_id in existing_ids:
                continue
            existing_ids.add(transaction_id)
            transaction = Transaction(
                TransactionID=transaction_id,
                CustomerName=row['CustomerName'],
                TransactionDate=row['TransactionDate'],
                Amount=row['Amount'],
                Status=row['Status'],
                InvoiceURL=row['InvoiceURL']
            )
            session.add(transaction)
        session.commit()
        session.close()
        return 'File uploaded successfully'


@app.route('/transactions', methods=['GET'])
def get_transactions():
    session = Session()
    transactions = session.query(Transaction).all()
    session.close()
    transaction_list = []
    for transaction in transactions:
        transaction_dict = {
            'TransactionID': transaction.TransactionID,
            'CustomerName': transaction.CustomerName,
            'TransactionDate': str(transaction.TransactionDate),
            'Amount': transaction.Amount,
            'Status': transaction.Status,
            'InvoiceURL': transaction.InvoiceURL
        }
        transaction_list.append(transaction_dict)
    return jsonify(transaction_list)

@app.route('/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    session = Session()
    transaction = session.query(Transaction).filter_by(TransactionID=transaction_id).first()
    session.close()
    if transaction:
        transaction_dict = {
            'TransactionID': transaction.TransactionID,
            'CustomerName': transaction.CustomerName,
            'TransactionDate': str(transaction.TransactionDate),
            'Amount': transaction.Amount,
            'Status': transaction.Status,
            'InvoiceURL': transaction.InvoiceURL
        }
        return jsonify(transaction_dict)
    else:
        return jsonify({'error': 'Transaction not found'}), 404

@app.route('/transactions/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    session = Session()
    transaction = session.query(Transaction).filter_by(TransactionID=transaction_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    data = request.json
    transaction.CustomerName = data.get('CustomerName', transaction.CustomerName)
    transaction.TransactionDate = data.get('TransactionDate', transaction.TransactionDate)
    transaction.Amount = data.get('Amount', transaction.Amount)
    transaction.Status = data.get('Status', transaction.Status)
    transaction.InvoiceURL = data.get('InvoiceURL', transaction.InvoiceURL)
    
    session.commit()
    session.close()
    
    return jsonify({'message': 'Transaction updated successfully'}), 200

@app.route('/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    session = Session()
    transaction = session.query(Transaction).filter_by(TransactionID=transaction_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    session.delete(transaction)
    session.commit()
    session.close()
    
    return jsonify({'message': 'Transaction deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
