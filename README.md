# Exercise project

# In case you have python3.8 already installed install requirements and you are ready to go:
```
pip install -r requirementse.txt
```

# In case you want to create virtual env
1. Install python venv
```
apt install python3.8-venv
```
2. Create new 3.8 environment
```
python3.8 -m venv ~/venvs/3.8_for_test
```
3. Activate env
```
source ~/venvs/3.8_for_test/bin/activate
```
4. Install requirements
```
pip install -r requirementse.txt
```
5. Don't forget to configure this env as project interpreter

# Shady csv:
All the transactions should be positive decimal values, in case negative value is introduced the code raises exception

Dispute of withdrawal (client saying the transaction did not arrive to his account) is not supported

Chargeback of withdrawal ( the company reversing the withdrawal ) is not supported

Resolved of withdrawal is not valid since that would need disputed

# Testing
Test files, expected results and results are provided, running the tests should pass by default

In case you want to create new result files use the following:
```
python3.8 payment_engine.py test_files/transactions_1.csv > transactions_1_result.csv
python3.8 payment_engine.py test_files/transactions_2.csv > transactions_2_result.csv
python3.8 payment_engine.py test_files/transactions_3.csv > transactions_3_result.csv
python3.8 payment_engine.py test_files/transactions.csv > transactions_result.csv
```

Testing can be done by running the test_transactions.py file
```
pytest test_transactions.py 
```
In case you want to add more test cases
1. create test file
2. create expected output file
3. add file name to the list in test_transactions

Note: The expected and the test file name should have similar names
