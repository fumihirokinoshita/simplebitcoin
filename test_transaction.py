from tsx import Transaction
from tsx import TransactionInput
from tsx import TransactionOutput
from tsx import CoinbaseTransaction

def main():

    t1 = CoinbaseTransaction('Itsuki_pubkey')

    print(t1.to_dict())

    t2 = Transaction(
        [TransactionInput(t1, 0)],
        [TransactionOutput('Umika_pubkey', 10.0),
        TransactionOutput('Itsuki_pubkey', 20.0)]
    )

    print(t2.to_dict())

if __name__ == '__main__':
    main()