def error_progres(errors):
    error_messages = []    
    for error in errors:
        error_messages.append(errors[error][0])
    return error_messages