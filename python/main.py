from runners.sas_runner import run_sas
from runners.r_runner import run_r
from comparators.dataset_compare import compare_datasets

def main():
    sas_out = run_sas("sas/sample_sas_code/example.sas")
    r_out = run_r("r/sample_r_code/example.R")

    result = compare_datasets(sas_out, r_out)
    print(result)

if __name__ == "__main__":
    main()
