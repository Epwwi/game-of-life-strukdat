# ===================================================================
# BIG INTEGER ADT - WITH ASSIGNMENT COMBO OPERATORS
# ===================================================================
# Menambahkan: +=, -=, *=, //=, %=, **=, <<=, >>=, |=, &=, ^=

class BigInteger:
    """Big Integer dengan Assignment Combo Operators"""
    
    def __init__(self, initValue="0"):
        """Creates a new big integer initialized to the given string"""
        self.is_negative = False
        
        if initValue.startswith('-'):
            self.is_negative = True
            initValue = initValue[1:]
        
        initValue = initValue.lstrip('0') or '0'
        self.digits = [int(d) for d in reversed(initValue)]
    
    def toString(self):
        """Returns a string representation of the big integer"""
        if not self.digits:
            return "0"
        
        result = ''.join(str(d) for d in reversed(self.digits))
        
        if self.is_negative and result != "0":
            result = '-' + result
        
        return result
    
    def comparable(self, other):
        """Compares this big integer to other"""
        if not isinstance(other, BigInteger):
            raise TypeError("Can only compare with another BigInteger")
        
        if self.is_negative and not other.is_negative:
            return -1
        if not self.is_negative and other.is_negative:
            return 1
        
        len_self = len(self.digits)
        len_other = len(other.digits)
        
        if len_self < len_other:
            return -1 if not self.is_negative else 1
        if len_self > len_other:
            return 1 if not self.is_negative else -1
        
        for i in range(len_self - 1, -1, -1):
            if self.digits[i] < other.digits[i]:
                return -1 if not self.is_negative else 1
            if self.digits[i] > other.digits[i]:
                return 1 if not self.is_negative else -1
        
        return 0
    
    def _to_int(self):
        """Convert to Python int"""
        return int(self.toString())
    
    def _from_int(self, value):
        """Update from Python int"""
        result = BigInteger(str(value))
        self.digits = result.digits
        self.is_negative = result.is_negative
        return self
    
    # ===== BASIC OPERATORS =====
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
    
    # ===== ARITHMETIC OPERATORS =====
    def __add__(self, other):
        result = self._to_int() + other._to_int()
        return BigInteger(str(result))
    
    def __sub__(self, other):
        result = self._to_int() - other._to_int()
        return BigInteger(str(result))
    
    def __mul__(self, other):
        result = self._to_int() * other._to_int()
        return BigInteger(str(result))
    
    def __floordiv__(self, other):
        result = self._to_int() // other._to_int()
        return BigInteger(str(result))
    
    def __mod__(self, other):
        result = self._to_int() % other._to_int()
        return BigInteger(str(result))
    
    def __pow__(self, other):
        result = self._to_int() ** other._to_int()
        return BigInteger(str(result))
    
    # ===== BITWISE OPERATORS =====
    def __or__(self, other):
        result = self._to_int() | other._to_int()
        return BigInteger(str(result))
    
    def __and__(self, other):
        result = self._to_int() & other._to_int()
        return BigInteger(str(result))
    
    def __xor__(self, other):
        result = self._to_int() ^ other._to_int()
        return BigInteger(str(result))
    
    def __lshift__(self, other):
        result = self._to_int() << other._to_int()
        return BigInteger(str(result))
    
    def __rshift__(self, other):
        result = self._to_int() >> other._to_int()
        return BigInteger(str(result))
    
    # ===== ASSIGNMENT COMBO OPERATORS =====
    
    def __iadd__(self, other):
        """+="""
        result = self._to_int() + other._to_int()
        return self._from_int(result)
    
    def __isub__(self, other):
        """-="""
        result = self._to_int() - other._to_int()
        return self._from_int(result)
    
    def __imul__(self, other):
        """*="""
        result = self._to_int() * other._to_int()
        return self._from_int(result)
    
    def __ifloordiv__(self, other):
        """//="""
        result = self._to_int() // other._to_int()
        return self._from_int(result)
    
    def __imod__(self, other):
        """%="""
        result = self._to_int() % other._to_int()
        return self._from_int(result)
    
    def __ipow__(self, other):
        """**="""
        result = self._to_int() ** other._to_int()
        return self._from_int(result)
    
    def __ilshift__(self, other):
        """<<="""
        result = self._to_int() << other._to_int()
        return self._from_int(result)
    
    def __irshift__(self, other):
        """>>="""
        result = self._to_int() >> other._to_int()
        return self._from_int(result)
    
    def __ior__(self, other):
        """|="""
        result = self._to_int() | other._to_int()
        return self._from_int(result)
    
    def __iand__(self, other):
        """&="""
        result = self._to_int() & other._to_int()
        return self._from_int(result)
    
    def __ixor__(self, other):
        """^="""
        result = self._to_int() ^ other._to_int()
        return self._from_int(result)


# ===================================================================
# TESTING PROGRAM
# ===================================================================

print("=" * 70)
print("BIG INTEGER ADT - WITH ASSIGNMENT COMBO OPERATORS")
print("=" * 70)

# Test Assignment Combo Operators
print("\n" + "="*70)
print("TESTING ASSIGNMENT COMBO OPERATORS")
print("="*70)

# Test +=
print("\n1. += (Addition Assignment)")
x = BigInteger("100")
print(f"   x = {x}")
x += BigInteger("50")
print(f"   x += 50  →  x = {x}")

# Test -=
print("\n2. -= (Subtraction Assignment)")
x = BigInteger("100")
print(f"   x = {x}")
x -= BigInteger("30")
print(f"   x -= 30  →  x = {x}")

# Test *=
print("\n3. *= (Multiplication Assignment)")
x = BigInteger("10")
print(f"   x = {x}")
x *= BigInteger("5")
print(f"   x *= 5  →  x = {x}")

# Test //=
print("\n4. //= (Floor Division Assignment)")
x = BigInteger("100")
print(f"   x = {x}")
x //= BigInteger("7")
print(f"   x //= 7  →  x = {x}")

# Test %=
print("\n5. %= (Modulo Assignment)")
x = BigInteger("100")
print(f"   x = {x}")
x %= BigInteger("7")
print(f"   x %= 7  →  x = {x}")

# Test **=
print("\n6. **= (Power Assignment)")
x = BigInteger("2")
print(f"   x = {x}")
x **= BigInteger("8")
print(f"   x **= 8  →  x = {x}")

# Test <<=
print("\n7. <<= (Left Shift Assignment)")
x = BigInteger("5")
print(f"   x = {x}")
x <<= BigInteger("2")
print(f"   x <<= 2  →  x = {x}  (5 << 2 = {5 << 2})")

# Test >>=
print("\n8. >>= (Right Shift Assignment)")
x = BigInteger("20")
print(f"   x = {x}")
x >>= BigInteger("2")
print(f"   x >>= 2  →  x = {x}  (20 >> 2 = {20 >> 2})")

# Test |=
print("\n9. |= (Bitwise OR Assignment)")
x = BigInteger("12")
print(f"   x = {x}")
x |= BigInteger("5")
print(f"   x |= 5  →  x = {x}  (12 | 5 = {12 | 5})")

# Test &=
print("\n10. &= (Bitwise AND Assignment)")
x = BigInteger("12")
print(f"    x = {x}")
x &= BigInteger("5")
print(f"    x &= 5  →  x = {x}  (12 & 5 = {12 & 5})")

# Test ^=
print("\n11. ^= (Bitwise XOR Assignment)")
x = BigInteger("12")
print(f"    x = {x}")
x ^= BigInteger("5")
print(f"    x ^= 5  →  x = {x}  (12 ^ 5 = {12 ^ 5})")

# Complex Example
print("\n" + "="*70)
print("COMPLEX EXAMPLE")
print("="*70)

total = BigInteger("100")
print(f"Starting value: {total}")

total += BigInteger("50")
print(f"After += 50: {total}")

total *= BigInteger("2")
print(f"After *= 2: {total}")

total //= BigInteger("10")
print(f"After //= 10: {total}")

total **= BigInteger("2")
print(f"After **= 2: {total}")

print("\n" + "=" * 70)
print("✓ ALL ASSIGNMENT COMBO OPERATORS WORKING!")
print("=" * 70)