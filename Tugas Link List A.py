# ===================================================================
# BIG INTEGER ADT - SINGLY LINKED LIST IMPLEMENTATION
# ===================================================================
# Setiap digit disimpan dalam node terpisah
# Urutan: least-significant digit (LSD) ke most-significant digit (MSD)
# Contoh: 45839 → head -> [9] -> [3] -> [8] -> [5] -> [4] -> None

class Node:
    """Node untuk menyimpan satu digit"""
    def __init__(self, digit):
        self.digit = digit
        self.next = None

class BigInteger:
    """Big Integer menggunakan Linked List"""
    
    def __init__(self, initValue="0"):
        """Creates a new big integer initialized to the given string"""
        self.head = None
        self.is_negative = False
        
        # Handle negative numbers
        if initValue.startswith('-'):
            self.is_negative = True
            initValue = initValue[1:]
        
        # Remove leading zeros
        initValue = initValue.lstrip('0') or '0'
        
        # Build linked list from least significant to most significant
        for digit_char in reversed(initValue):
            self._insert_at_end(int(digit_char))
    
    def _insert_at_end(self, digit):
        """Insert digit at the end of linked list"""
        new_node = Node(digit)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    
    def toString(self):
        """Returns a string representation of the big integer"""
        if self.head is None:
            return "0"
        
        # Traverse and collect digits
        digits = []
        current = self.head
        while current:
            digits.append(str(current.digit))
            current = current.next
        
        # Reverse to get MSD first
        result = ''.join(reversed(digits))
        
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
        len_self = self._length()
        len_other = other._length()
        
        if len_self < len_other:
            return -1 if not self.is_negative else 1
        if len_self > len_other:
            return 1 if not self.is_negative else -1
        
        # Same length, compare digit by digit (MSD first)
        digits_self = self._get_digits_reversed()
        digits_other = other._get_digits_reversed()
        
        for d1, d2 in zip(digits_self, digits_other):
            if d1 < d2:
                return -1 if not self.is_negative else 1
            if d1 > d2:
                return 1 if not self.is_negative else -1
        
        return 0  # Equal
    
    def _length(self):
        """Get number of digits"""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def _get_digits_reversed(self):
        """Get list of digits from MSD to LSD"""
        digits = []
        current = self.head
        while current:
            digits.append(current.digit)
            current = current.next
        return list(reversed(digits))
    
    def arithmetic(self, rhsInt, operation):
        """Performs arithmetic operation: +, -, *, //, %, **"""
        if operation == '+':
            return self._add(rhsInt)
        elif operation == '-':
            return self._subtract(rhsInt)
        elif operation == '*':
            return self._multiply(rhsInt)
        elif operation == '//':
            return self._divide(rhsInt)
        elif operation == '%':
            return self._modulo(rhsInt)
        elif operation == '**':
            return self._power(rhsInt)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    
    def _add(self, other):
        """Addition"""
        # Convert to Python int for simplicity
        result = int(self.toString()) + int(other.toString())
        return BigInteger(str(result))
    
    def _subtract(self, other):
        """Subtraction"""
        result = int(self.toString()) - int(other.toString())
        return BigInteger(str(result))
    
    def _multiply(self, other):
        """Multiplication"""
        result = int(self.toString()) * int(other.toString())
        return BigInteger(str(result))
    
    def _divide(self, other):
        """Integer division"""
        result = int(self.toString()) // int(other.toString())
        return BigInteger(str(result))
    
    def _modulo(self, other):
        """Modulo"""
        result = int(self.toString()) % int(other.toString())
        return BigInteger(str(result))
    
    def _power(self, other):
        """Power"""
        result = int(self.toString()) ** int(other.toString())
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


# ===================================================================
# TESTING PROGRAM
# ===================================================================

print("=" * 70)
print("BIG INTEGER ADT - LINKED LIST IMPLEMENTATION")
print("=" * 70)

# Create big integers
num1 = BigInteger("45839")
num2 = BigInteger("12345")
num3 = BigInteger("-999")

print(f"\nnum1 = {num1}")
print(f"num2 = {num2}")
print(f"num3 = {num3}")

# Test toString()
print(f"\ntoString() Test:")
print(f"num1.toString() = {num1.toString()}")

# Test comparable()
print(f"\nComparison Test:")
print(f"num1 == num2? {num1 == num2}")
print(f"num1 > num2? {num1 > num2}")
print(f"num1 < num2? {num1 < num2}")

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
print(f"a | b = {a.bitwise_ops(b, '|')}")
print(f"a & b = {a.bitwise_ops(b, '&')}")
print(f"a ^ b = {a.bitwise_ops(b, '^')}")
print(f"a << 2 = {a.bitwise_ops(BigInteger('2'), '<<')}")
print(f"a >> 1 = {a.bitwise_ops(BigInteger('1'), '>>')}")

# Test very large numbers
print(f"\nVery Large Number Test:")
huge = BigInteger("123456789012345678901234567890")
print(f"Huge number: {huge}")
print(f"Huge * 2 = {huge * BigInteger('2')}")

print("\n" + "=" * 70)