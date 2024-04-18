def int_range(min=1, max=10):
    def validate(value):
        try:
            value_int = int(value)
        except Exception as ex:
            raise ValueError(f"Invalid literal for int={value}: {str(ex)}")

        if not (min <= value_int <= max):
            raise ValueError(f"Value must be in range [{min}, {max}]")

        return value

    return validate
