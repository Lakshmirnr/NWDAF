from app.algorithms.entropy_metrics import shannon_entropy, numeric_entropy

def test_entropy_basic():
    assert shannon_entropy(['a','a','b']) > 0
    assert numeric_entropy([1,2,3,4,5], bins=5) >= 0
