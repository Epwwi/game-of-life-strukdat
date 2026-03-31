# ===================================================================
# BIG INTEGER ADT - PYTHON LIST IMPLEMENTATION
# ===================================================================
# Setiap digit disimpan dalam list
# Urutan: least-significant digit (LSD) ke most-significant digit (MSD)
# Contoh: 45839 → [9, 3, 8, 5, 4]

class BigInteger:
    """Big Integer menggunakan Python List"""
    
    def __init__(self, initValue="0"):
        """Creates a new big integer initialized to the given string"""
        self.is_negative = False
        
        # Handle negative numbers
        if initValue.startswith('-'):
            self.is_negative = True
            initValue = initValue[1:]
        
        # Remove leading zeros
        initValue = initValue.lstrip('0') or '0'
        
        # Store digits in reverse (LSD first)
        self.digits = [int(d) for d in reversed(initValue)]
    
    def toString(self):
        """Returns a string representation of the big integer"""
        if not self.digits:
            return "0"
        
        # Reverse to get MSD first
        result = ''.join(str(d) for d in reversed(self.digits))
        
        if self.is_negative and result != "0":
            result = '-' + result
        
        return result
    
    def comparable(self, other):
        """Compares this big integer to other big integer"""
        if not isinstance(other, BigInteger):
            raise TypeError("Can only compare with another BigInteger")
        
        # Handle signs
        if self.is_negative and not other.is_negative:
            return -1
        if not self.is_negative and other.is_negative:
            return 1
        
        # Both same sign, compare absolute values
        len_self = len(self.digits)
        len_other = len(other.digits)
        
        if len_self < len_other:
            return -1 if not self.is_negative else 1
        if len_self > len_other:
            return 1 if not self.is_negative else -1
        
        # Same length, compare digit by digit (MSD first)
        for i in range(len_self - 1, -1, -1):
            if self.digits[i] < other.digits[i]:
                return -1 if not self.is_negative else 1
            if self.digits[i] > other.digits[i]:
                return 1 if not self.is_negative else -1
        
        return 0  # Equal
    
    def arithmetic(self, rhsInt, operation):
        """Performs arithmetic operation: +, -, *, //, %, **"""
        val1 = int(self.toString())
        val2 = int(rhsInt.toString())
        
        if operation == '+':
            result = val1 + val2
        elif operation == '-':
            result = val1 - val2
        elif operation == '*':
            result = val1 * val2
        elif operation == '//':
            result = val1 // val2
        elif operation == '%':
            result = val1 % val2
        elif operation == '**':
            result = val1 ** val2
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        return BigInteger(str(result))
    
    def bitwise_ops(self, rhsInt, operation):
        """Performs bitwise operation: |, &, ^, <<, >>"""
        val1 = int(self.toString())
        val2 = int(rhsInt.toString())
        
        if operation == '|':
            result = val1 | val2
        elif operation == '&':
            result = val1 & val2
        elif operation == '^':
            result = val1 ^ val2
        elif operation == '<<':
            result = val1 << val2
        elif operation == '>>':
            result = val1 >> val2
        else:
            raise ValueError(f"Unsupported bitwise operation: {operation}")
        
        return BigInteger(str(result))
    
    # Operator overloading
    def __str__(self):
        return self.toString()
    
    def __eq__(self, other):
        return self.comparable(other) == 0
    
    def __ne__(self, other):
        return self.comparable(other) != 0
    
    def __lt__(self, other):
        return self.comparable(other) < 0
    
    def __le__(self, other):
        return self.comparable(other) <= 0
    
    def __gt__(self, other):
        return self.comparable(other) > 0
    
    def __ge__(self, other):
        return self.comparable(other) >= 0
    
    def __add__(self, other):
        return self.arithmetic(other, '+')
    
    def __sub__(self, other):
        return self.arithmetic(other, '-')
    
    def __mul__(self, other):
        return self.arithmetic(other, '*')
    
    def __floordiv__(self, other):
        return self.arithmetic(other, '//')
    
    def __mod__(self, other):
        return self.arithmetic(other, '%')
    
    def __pow__(self, other):
        return self.arithmetic(other, '**')
    
    def __or__(self, other):
        return self.bitwise_ops(other, '|')
    
    def __and__(self, other):
        return self.bitwise_ops(other, '&')
    
    def __xor__(self, other):
        return self.bitwise_ops(other, '^')
    
    def __lshift__(self, other):
        return self.bitwise_ops(other, '<<')
    
    def __rshift__(self, other):
        return self.bitwise_ops(other, '>>')


# ===================================================================
# TESTING PROGRAM
# ===================================================================

print("=" * 70)
print("BIG INTEGER ADT - PYTHON LIST IMPLEMENTATION")
print("=" * 70)

# Create big integers
num1 = BigInteger("45839")
num2 = BigInteger("12345")
num3 = BigInteger("-999")

print(f"\nnum1 = {num1} (digits: {num1.digits})")
print(f"num2 = {num2} (digits: {num2.digits})")
print(f"num3 = {num3} (digits: {num3.digits})")

# Test toString()
print(f"\ntoString() Test:")
print(f"num1.toString() = {num1.toString()}")

# Test comparable()
print(f"\nComparison Test:")
print(f"num1 == num2? {num1 == num2}")
print(f"num1 > num2? {num1 > num2}")
print(f"num1 < num2? {num1 < num2}")
print(f"num1 >= num2? {num1 >= num2}")

# Test arithmetic operations
print(f"\nArithmetic Operations:")
print(f"num1 + num2 = {num1 + num2}")
print(f"num1 - num2 = {num1 - num2}")
print(f"num1 * num2 = {num1 * num2}")
print(f"num1 // num2 = {num1 // num2}")
print(f"num1 % num2 = {num1 % num2}")
print(f"BigInteger('2') ** BigInteger('10') = {BigInteger('2') ** BigInteger('10')}")

# Test bitwise operations
print(f"\nBitwise Operations:")
a = BigInteger("12")
b = BigInteger("5")
print(f"a = {a}, b = {b}")
print(f"a | b = {a | b}  (12 | 5 = {12 | 5})")
print(f"a & b = {a & b}  (12 & 5 = {12 & 5})")
print(f"a ^ b = {a ^ b}  (12 ^ 5 = {12 ^ 5})")
print(f"a << 2 = {a << BigInteger('2')}  (12 << 2 = {12 << 2})")
print(f"a >> 1 = {a >> BigInteger('1')}  (12 >> 1 = {12 >> 1})")

# Test very large numbers
print(f"\nVery Large Number Test:")
huge1 = BigInteger("999999999999999999999999999999")
huge2 = BigInteger("123456789012345678901234567890")
print(f"Huge1: {huge1}")
print(f"Huge2: {huge2}")
print(f"Huge1 + Huge2 = {huge1 + huge2}")
print(f"Huge1 * BigInteger('2') = {huge1 * BigInteger('2')}")

# Test edge cases
print(f"\nEdge Cases:")
zero = BigInteger("0")
one = BigInteger("1")
neg = BigInteger("-100")
print(f"Zero: {zero}")
print(f"One: {one}")
print(f"Negative: {neg}")
print(f"Negative + Positive: {neg + BigInteger('150')} = {-100 + 150}")

print("\n" + "=" * 70)