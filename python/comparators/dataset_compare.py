import pandas as pd
import pyreadstat
import numpy as np

def load_sas(path):
    # For testing without SAS, treat CSV as SAS
    df = pd.read_csv(path)

    # Convert numeric columns properly
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')  # numbers stay numbers
        if df[col].dtype == object:
            df[col] = df[col].str.strip()  # remove extra spaces

    return df


def load_r_csv(path):
    df = pd.read_csv(path)

    # Convert numeric columns properly
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')  # numbers stay numbers
        if df[col].dtype == object:
            df[col] = df[col].str.strip()  # remove extra spaces

    return df


def compare_datasets(sas_path, r_path, tol=1e-8, ignore_row_order=False):
    # Load datasets
    df_sas = load_sas(sas_path)
    df_r = load_r_csv(r_path)

    # Check columns
    if set(df_sas.columns) != set(df_r.columns):
        return {"status": "mismatch", "message": "Column names differ"}

    # Reorder rows if needed
    if ignore_row_order:
        df_sas = df_sas.sort_values(by=list(df_sas.columns)).reset_index(drop=True)
        df_r = df_r.sort_values(by=list(df_r.columns)).reset_index(drop=True)

    # Compare numeric columns
    numeric_cols = df_sas.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
    # Ensure both sides are numeric
        left = pd.to_numeric(df_sas[col], errors='coerce')
        right = pd.to_numeric(df_r[col], errors='coerce')

        diff = np.abs(left - right)
        if not np.all(diff <= tol):
            return {"status": "mismatch", "message": f"Numeric mismatch in column {col}"}


    # Compare object/character columns
    object_cols = df_sas.select_dtypes(include=['object']).columns
    for col in object_cols:
        if not (df_sas[col].fillna("").astype(str).equals(df_r[col].fillna("").astype(str))):
            return {"status": "mismatch", "message": f"Character mismatch in column {col}"}

    return {"status": "match", "message": "Datasets match"}
import pandas as pd
import pyreadstat
import numpy as np

def load_sas(path):
    ## df, meta = pyreadstat.read_sas7bdat(path)
    ## return df

    # For testing without SAS, treat CSV as SAS
    return pd.read_csv(path)

def load_r_csv(path):
    df = pd.read_csv(path)
    return df

def compare_datasets(sas_path, r_path, tol=1e-8, ignore_row_order=False):
    # Load datasets
    df_sas = load_sas(sas_path)
    df_r = load_r_csv(r_path)

    # Check columns
    if set(df_sas.columns) != set(df_r.columns):
        return {"status": "mismatch", "message": "Column names differ"}

    # Reorder rows if needed
    if ignore_row_order:
        df_sas = df_sas.sort_values(by=list(df_sas.columns)).reset_index(drop=True)
        df_r = df_r.sort_values(by=list(df_r.columns)).reset_index(drop=True)

    # Compare numeric columns
    numeric_cols = df_sas.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        diff = np.abs(df_sas[col] - df_r[col])
        if not np.all(diff <= tol):
            return {"status": "mismatch", "message": f"Numeric mismatch in column {col}"}

    # Compare object/character columns
    object_cols = df_sas.select_dtypes(include=['object']).columns
    for col in object_cols:
        if not (df_sas[col].fillna("").astype(str).equals(df_r[col].fillna("").astype(str))):
            return {"status": "mismatch", "message": f"Character mismatch in column {col}"}

    return {"status": "match", "message": "Datasets match"}
