import pandas_profiling


def create_summary_report(df):
    # Data profiling/EDA
    profile = pandas_profiling.ProfileReport(
        df, title="Data Audit Report \nAuthor: Ved"
    )
    profile.to_file(output_file="../reports/data_audit_report.html")
