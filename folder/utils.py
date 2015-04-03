
def dehydrate_validation_errors(errors_data):
    """Convert ValidationError objects to their string representation
    it is safe for JsonResponse
    """

    dehydrated_output = {}

    for key, value in errors_data.items():
        errors = ", ".join([str(x).lstrip("[u'").rstrip("']") for x in value])
        dehydrated_output[key] = errors

    return dehydrated_output
