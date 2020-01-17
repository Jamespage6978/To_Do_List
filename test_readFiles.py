import pytest
from main import dateConvert

def date_test1():
    time = 0
    assert dateConvert(time,days=False) == '01-01-1970',"test failed"
    assert dateConvert(time,days=True) == '01',"test failed"