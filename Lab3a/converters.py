# converters.py
class FourDigitYearConverter:
    regex = "[0-9]{4}"  # Khớp với chuỗi có 4 chữ số (năm)

    def to_python(self, value):
        return int(value)  # Chuyển đổi chuỗi thành kiểu số nguyên

    def to_url(self, value):
        return "%04d" % value  # Chuyển đổi số nguyên thành chuỗi có 4 chữ số
