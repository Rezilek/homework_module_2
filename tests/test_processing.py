import pytest
from src.processing import process_bank_search, process_bank_operations

@pytest.fixture
def sample_transactions():
    return [
        {'description': 'Payment for services', 'amount': 100},
        {'description': 'Grocery shopping', 'amount': 50},
        {'description': 'Monthly salary', 'amount': 2000},
        {'description': 'Service fee', 'amount': 10}
    ]

def test_process_bank_search(sample_transactions):
    result = process_bank_search(sample_transactions, r'service')
    assert len(result) == 2
    assert result[0]['description'] == 'Payment for services'
    assert result[1]['description'] == 'Service fee'

def test_process_bank_operations(sample_transactions):
    categories = ['Grocery shopping', 'Monthly salary', 'Bonus']
    result = process_bank_operations(sample_transactions, categories)
    assert result == {'Grocery shopping': 1, 'Monthly salary': 1}
