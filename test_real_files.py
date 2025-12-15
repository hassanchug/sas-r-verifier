from python.comparators.dataset_compare import compare_datasets

# ---- CHANGE THESE TO YOUR REAL FILES ----

sas_file = r"C:\FULL\PATH\TO\your_sas_file.sas7bdat"
r_file   = r"C:\FULL\PATH\TO\your_r_file.rda"

# This must match the object name INSIDE the .rda file
r_dataset_name = "my_dataframe_name"

# ----------------------------------------

result = compare_datasets(
    sas_path=sas_file,
    r_path=r_file,
    r_dataset_name=r_dataset_name,
    tol=1e-8,
    ignore_row_order=True
)

print(result)
