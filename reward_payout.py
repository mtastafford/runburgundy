from steem.transactionbuilder import TransactionBuilder
from steembase import operations

# lets create 3 transfers, to 3 different people
transfers = [
    {
        'from': 'runburgundy',
        'to': 'mstafford',
        'amount': '0.001 SBD',
        'memo': 'Test Transfer 1'
    },
    {
        'from': 'runburgundy',
        'to': 'mstafford',
        'amount': '0.002 SBD',
        'memo': 'Test Transfer 2'
    },
    {
        'from': 'runburgundy',
        'to': 'mstafford',
        'amount': '0.003 SBD',
        'memo': 'Test Transfer 3'
    }

]
print(transfers)
# now we can construct the transaction
# we will set no_broadcast to True because
# we don't want to really send funds, just testing.
tb = TransactionBuilder()

# lets serialize our transfers into a format Steem can understand
operations = [operations.Transfer(**x) for x in transfers]

# tell TransactionBuilder to use our serialized transfers
tb.appendOps(operations)

# we need to tell TransactionBuilder about
# everyone who needs to sign the transaction.
# since all payments are made from `richguy`,
# we just need to do this once
tb.appendSigner('runburgundy', 'active')

# sign the transaction
tb.sign()

# broadcast the transaction (publish to steem)
# since we specified no_broadcast=True earlier
# this method won't actually do anything
tx = tb.broadcast()
