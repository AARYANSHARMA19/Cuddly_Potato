#!/usr/bin/env python3
import json
import sys
import string

# ---------------------------------------------------------
#  ALL Original ObfUX Encoder/Decoder Code (unchanged)
# ---------------------------------------------------------

BASE32_ALPHABET = "0123456789abcdefghijklmnopqrstuv"
BASE36_ALPHABET = string.digits + string.ascii_lowercase

def int_to_base(n: int, base: int, alphabet: str) -> str:
    if n == 0:
        return alphabet[0]
    digits = []
    while n > 0:
        n, rem = divmod(n, base)
        digits.append(alphabet[rem])
    return ''.join(reversed(digits))

def base_to_int(s: str, base: int, alphabet: str) -> int:
    n = 0
    for ch in s:
        n = n * base + alphabet.index(ch)
    return n

def reverse_bits_of_byte(n: int) -> int:
    result = 0
    for i in range(8):
        if n & (1 << i):
            result |= 1 << (7 - i)
    return result

def encode_key(key: str) -> str:
    parts = []
    for ch in key:
        reversed_bits = reverse_bits_of_byte(ord(ch))
        parts.append(int_to_base(reversed_bits, 36, BASE36_ALPHABET))
    return '.'.join(parts)

def decode_key(encoded: str) -> str:
    parts = encoded.split('.') if encoded else []
    out = []
    for p in parts:
        num = base_to_int(p, 36, BASE36_ALPHABET)
        orig = reverse_bits_of_byte(num)
        out.append(chr(orig))
    return ''.join(out)

def encode_value(value):
    if isinstance(value, str):
        codes = []
        for i, ch in enumerate(value):
            codes.append(int_to_base(ord(ch) + i, 32, BASE32_ALPHABET))
        return 'S', '-'.join(reversed(codes))

    # FIX: check bool before int
    if isinstance(value, bool):
        return 'B', '👍' if value else '👎'

    if isinstance(value, (int, float)):
        parts = []
        for i, ch in enumerate(str(value)):
            parts.append(format(ord(ch) - i, 'x'))
        return 'N', '&'.join(parts[::-1])

    if value is None:
        return 'U', '💤'

    if isinstance(value, list):
        elems = []
        for elem in value:
            tag, enc = encode_value(elem)
            elems.append(f"{tag}:{enc}")
        return 'L', '[' + '|'.join(elems) + ']'

    if isinstance(value, dict):
        inner = encode(value)
        return 'O', inner[1:-1]

    raise TypeError("Unsupported type")

def decode_value(tag: str, encoded: str):
    if tag == 'S':
        parts = list(reversed(encoded.split('-')))
        chars = []
        for i, code in enumerate(parts):
            ascii_code = base_to_int(code, 32, BASE32_ALPHABET) - i
            chars.append(chr(ascii_code))
        return ''.join(chars)

    if tag == 'N':
        parts = list(reversed(encoded.split('&')))
        chars = []
        for i, hx in enumerate(parts):
            code = int(hx, 16) + i
            chars.append(chr(code))
        s = ''.join(chars)
        return float(s) if '.' in s or 'e' in s or 'E' in s else int(s)

    if tag == 'B':
        return encoded == '👍'

    if tag == 'U':
        return None

    if tag == 'L':
        inner = encoded[1:-1]
        if not inner:
            return []
        out = []
        for elem in inner.split('|'):
            t, v = elem.split(':', 1)
            out.append(decode_value(t, v))
        return out

    if tag == 'O':
        return decode('💫' + encoded + '💫')

    raise ValueError("Unknown tag")

def encode(data: dict) -> str:
    parts = []
    for key, value in data.items():
        k = encode_key(key)
        t, v = encode_value(value)
        parts.append(f"{k}🐉{t}🐉{v}")
    return '💫' + '🧟'.join(parts) + '💫'

def decode(s: str) -> dict:
    if not (s.startswith('💫') and s.endswith('💫')):
        raise ValueError("Missing 💫 wrappers")
    inner = s[1:-1]
    if not inner:
        return {}
    out = {}
    for pair in inner.split('🧟'):
        kenc, tag, venc = pair.split('🐉', 2)
        out[decode_key(kenc)] = decode_value(tag, venc)
    return out

# -------------------------------------------------------------------
#                       Terminal-only Program
# -------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python terminal_encoder.py <input.json>")
        return

    input_path = sys.argv[1]

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n🔐 ENCRYPTING JSON...\n")
    encrypted = encode(data)
    print("📦 Encrypted Output:")
    print(encrypted)

    choice = input("\n🔄 Decrypt it? (y/n): ").strip().lower()
    if choice == "y":
        print("\n🗝️ DECRYPTING...\n")
        decrypted = decode(encrypted)
        print(json.dumps(decrypted, indent=2, ensure_ascii=False))
    else:
        print("\nExiting without decryption.")

if __name__ == "__main__":
    main()
