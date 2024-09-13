def summarize_adherence_columns(df):
    if df["BASSA ADERENZA"] == 1:
        return 0
    elif df["INTERMEDIA ADERENZA"] == 1:
        return 1
    elif df["ALTA ADERENZA"] == 1:
        return 2
    else:
        return -1
