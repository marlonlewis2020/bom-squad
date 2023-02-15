import pytest

from test_data import data

class TestClass:
    
    def test_one(self):
        assert data['func'](3) == 4
        
    def test_two(self):
        assert sum(range(5))==10
        
    def my_test(self):
        with pytest.raises(SystemExit):
            raise SystemExit()