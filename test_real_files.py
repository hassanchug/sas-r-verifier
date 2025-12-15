from python.comparators.dataset_compare import compare_datasets

result = compare_datasets(
    sas_path = r"C:\Users\hachu\Documents\sas-r-verifier\sas\sample_data\sales.sas7bdat",
    r_path = r"C:\Users\hachu\Documents\sas-r-verifier\r\sample_data\sales.rds",
    r_dataset_name="sales",
    tol=1e-8,
    ignore_row_order=True
)

print(result)

