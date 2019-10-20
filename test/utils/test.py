from __future__ import division

from utils.utils import get_label_percentages

def test_get_label_percentages():
    label_col = 'label'
    test_df = pd.DataFrame(
        [[1, 10, 'A'], [5, 5, 'A'], [8, 0, 'B'], [4, 2, 'B'], [7, 1, 'A']],
        columns=['ex1', 'ex2', label_col]
    )

    expected = pd.Series([3/5, 2/5], index=['A', 'B'])
    
    actual = get_label_percentages(test_df, label_col)

    assert (expected.index == actual.index).all()
    assert (expected.values == actual.values).all()