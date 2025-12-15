import pandas as pd
import pyreadstat
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import conversion
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri


def load_sas(path):
    # Reads SAS dataset
    df, meta = pyreadstat.read_sas7bdat(path)
    return df

def load_r_rda(path, dataset_name):
    """
    Load an R .rda file and return a pandas DataFrame
    """
    ro.r['load'](path)

    if dataset_name not in ro.globalenv:
        raise ValueError(f"Dataset '{dataset_name}' not found in {path}")

    r_obj = ro.globalenv[dataset_name]

    with localconverter(conversion.default_converter + pandas2ri.converter):
        df = ro.conversion.rpy2py(r_obj)

    return df



def compare_datasets(
    sas_path,
    r_path,
    r_dataset_name,
    tol=1e-8,
    ignore_row_order=False
):
    df_sas = load_sas(sas_path)
    df_r = load_r_rda(r_path, r_dataset_name)

    # Column name check
    if set(df_sas.columns) != set(df_r.columns):
        return {"status": "mismatch", "message": "Column names differ"}

    # Align column order
    df_r = df_r[df_sas.columns]

    # Optional row reordering
    if ignore_row_order:
        sort_cols = list(df_sas.columns)
        df_sas = df_sas.sort_values(by=sort_cols).reset_index(drop=True)
        df_r = df_r.sort_values(by=sort_cols).reset_index(drop=True)

    # Numeric comparison
    numeric_cols = df_sas.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        left = df_sas[col].astype(float)
        right = df_r[col].astype(float)

        diff = np.abs(left - right)
        if not np.all(diff <= tol):
            return {
                "status": "mismatch",
                "message": f"Numeric mismatch in column {col}"
            }

    # Character comparison
    char_cols = df_sas.select_dtypes(include=['object']).columns
    for col in char_cols:
        left = df_sas[col].fillna("").astype(str)
        right = df_r[col].fillna("").astype(str)

        if not left.equals(right):
            return {
                "status": "mismatch",
                "message": f"Character mismatch in column {col}"
            }

    return {"status": "match", "message": "Datasets match"}

