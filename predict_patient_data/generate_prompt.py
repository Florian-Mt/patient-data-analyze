def generate_prompt(patient):
    full_prompt = f"""<s>[INST]Considering the sex, birth date, birth city, residence city and first drug to take of a
    patient, all information given line by line and formatted as 'label: value', the whole block of lines being enclosed
    by triple single quotes, predict the values for adherence and follow-up persistence.
    Do not consider any information than those provided enclosed by triple single quotes. Your task is to predict one
    value for adherence and one for follow-up persistence based on the patient's information and to output the predicted
    values in the same format.
    Do not absolutely include for any reason any other content, especially input information, in the output.
    '''
    sex: {patient['SESSO']}
    birth date: {patient['DT_NAS']}
    birth city: {patient['COMUNE NASCITA']}
    residence city: {patient['COMUNE_RESIDENZA']}
    first drug to take: {patient['PRIMO_PROD']}
    '''[/INST]
    adherence: {patient['ADERENZA']}
    persistence follow-up: {patient['Persistenza di Follow-up']}
    </s>
    """
    return full_prompt
