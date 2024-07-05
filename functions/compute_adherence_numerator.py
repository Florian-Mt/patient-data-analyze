def compute_adherence_numerator(group):
    if len(group) > 1:
        return group["giorni di terapia reali (PDD)"][:-1].sum()
    else:
        return 0
