class NumberUtils:
    def int_or_0(value):
        try:
            return int(value)
        except:
            return 0
