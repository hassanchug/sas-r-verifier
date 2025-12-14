from python.comparators.dataset_compare import compare_datasets


def test_exact_match():
    sas_path = "sas/sample_data/test.csv"
    r_path = "r/sample_data/test.csv"
    result = compare_datasets(sas_path, r_path)
    assert result["status"] == "match"

def test_numeric_mismatch():
    sas_path = "sas/sample_data/test.csv"
    r_path = "r/sample_data/test_numeric_diff.csv"
    result = compare_datasets(sas_path, r_path)
    assert result["status"] == "mismatch"

def test_row_order_difference():
    sas_path = "sas/sample_data/test.csv"
    r_path = "r/sample_data/test_reordered.csv"
    result = compare_datasets(sas_path, r_path, ignore_row_order=True)
    assert result["status"] == "match"
