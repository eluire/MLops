"""
Author: Mateus Eloi da Silva Bastos
Author: Rafael Garcia
Date: Nov. 2021
Test File
"""

from exchange_analyses import read_data


def test_read_data():
    data = read_data("data/euro-daily-hist_1999_2020.csv")
    assert data is None

def test_columns_data():
    data = read_data("data/euro-daily-hist_1999_2020.csv")
    assert len(data.columns) > 0

def test_has_data():
    data = read_data("data/euro-daily-hist_1999_2020.csv")
    assert len(data) > 0


