"""
encoder_decoder.py

This module implements a deliberately obtuse data format dubbed “ObfUX” (Obfuscated
Unicorn Exchange) designed for hackathon hijinks.  The goal was to take a
simple JSON-like structure and encode it into something that’s both
humorous and intentionally confusing for anyone trying to make sense of it.

The encoder turns a Python dictionary (or value) into a single string
containing a series of emoji‑delimited fields.  The decoder performs the
reverse operation, reconstructing the original Python data structure.

High‑level overview of the format:

* Each top‑level object is wrapped with a “💫” at the beginning and end.
* Each key/value pair is separated by the tomb‑like “🧟” emoji.
* Within each pair, the encoded key, a one‑letter type tag, and the encoded
  value are separated by a “🐉” emoji.
* Keys are encoded by reversing the bits of each character’s ASCII code,
  converting the result to base‑36 and joining with “.”.
* Strings, numbers, booleans, lists, dictionaries and `None` all have
  distinct encodings described in the functions below.

This file exposes two functions: ``encode`` and ``decode``.  Each operates
recursively on Python data structures consisting of dictionaries, lists,
strings, numbers, booleans and ``None``.

Usage example (from the command line)::

    python3 encoder_decoder.py encode input.json output.ux
    python3 encoder_decoder.py decode output.ux restored.json

The above will take a JSON file as input, encode it into our cursed
format and write it out.  The second command reverses the process.
"""

from __future__ import annotations

import base64
import json
import string
import sys
from typing import Any, Dict, List, Tuple


# Character set for base32 encoding used in string values.  We implement
# our own base conversion functions to avoid relying on the ``base64``
# module’s behaviour for arbitrary bases.
BASE32_ALPHABET = "0123456789abcdefghijklmnopqrstuv"
BASE36_ALPHABET = string.digits + string.ascii_lowercase


def int_to_base(n: int, base: int, alphabet: str) -> str:
    """Convert a non‑negative integer to a string in the given base.

    :param n: The integer to convert (must be >= 0).
    :param base: The base to convert to (e.g., 32 or 36).
    :param alphabet: A string of characters representing the digits in the
        target base.  Its length must equal ``base``.
    :returns: A string representation of ``n`` in the given base.
    """
    if n == 0:
        return alphabet[0]
    digits: List[str] = []
    while n > 0:
        n, rem = divmod(n, base)
        digits.append(alphabet[rem])
    return ''.join(reversed(digits))


def base_to_int(s: str, base: int, alphabet: str) -> int:
    """Convert a string in a given base to an integer.

    :param s: The string to convert.
    :param base: The base of the string representation.
    :param alphabet: The digit characters for the base.
    :returns: The integer value.
    """
    n = 0
    for ch in s:
        n = n * base + alphabet.index(ch)
    return n


def reverse_bits_of_byte(n: int) -> int:
    """Reverse the order of the lowest 8 bits of ``n``.

    Only the lower 8 bits are used; higher bits are ignored.  This is
    intentionally arbitrary – it produces odd numbers when paired with
    ASCII codes and contributes to the confusion.
    """
    result = 0
    for i in range(8):
        if n & (1 << i):
            result |= 1 << (7 - i)
    return result


def encode_key(key: str) -> str:
    """Encode a dictionary key into a base36 dotted representation.

    Each character’s ASCII code has its bits reversed (on 8 bits),
    converted into base36 and joined with periods.  This routine is
    intentionally obscure but fully reversible.
    """
    encoded_parts = []
    for ch in key:
        ascii_code = ord(ch)
        reversed_bits = reverse_bits_of_byte(ascii_code)
        encoded_parts.append(int_to_base(reversed_bits, 36, BASE36_ALPHABET))
    return '.'.join(encoded_parts)


def decode_key(encoded: str) -> str:
    """Decode a key previously encoded with ``encode_key``.

    Splits on periods, converts each base36 number back to an integer,
    reverses its bits and then converts the resulting number to a
    character.
    """
    parts = encoded.split('.') if encoded else []
    chars: List[str] = []
    for part in parts:
        num = base_to_int(part, 36, BASE36_ALPHABET)
        orig_byte = reverse_bits_of_byte(num)
        chars.append(chr(orig_byte))
    return ''.join(chars)


def encode_value(value: Any) -> Tuple[str, str]:
    """Return a tuple of (type tag, encoded string) for a given Python value.

    Supported type tags:

    * ``S`` – string
    * ``N`` – number (int or float)
    * ``B`` – boolean
    * ``L`` – list
    * ``O`` – object/dict
    * ``U`` – null/None

    The encoding of the value itself varies by type.
    """
    # Strings
    if isinstance(value, str):
        # For strings, iterate over characters with their index.  Add the
        # index to the ASCII code, convert to base32 and reverse the order
        # of the resulting codes to obfuscate the direction.
        codes: List[str] = []
        for i, ch in enumerate(value):
            code = ord(ch) + i
            codes.append(int_to_base(code, 32, BASE32_ALPHABET))
        # Reverse order of codes and join with '-'.  Surround with sparkles
        encoded = '-'.join(reversed(codes))
        return 'S', encoded

    # Numbers (int or float)
    if isinstance(value, (int, float)):
        # Convert the number to its string representation, then encode
        # each character by subtracting the index (to vary the result),
        # converting to hex and joining with '&'.  This works for
        # negative numbers and decimals too.
        num_str = str(value)
        parts: List[str] = []
        for i, ch in enumerate(num_str):
            code = ord(ch) - i
            parts.append(format(code, 'x'))  # hex representation without 0x
        encoded = '&'.join(parts[::-1])  # reverse order
        return 'N', encoded

    # Booleans
    if isinstance(value, bool):
        # Represent True as 👍 and False as 👎
        return 'B', '👍' if value else '👎'

    # None (null)
    if value is None:
        return 'U', '💤'

    # Lists
    if isinstance(value, list):
        # Encode each element individually and join with '|'.  Surround
        # with brackets so the decoder can recognise lists.
        encoded_elems = []
        for elem in value:
            type_tag, encoded_elem = encode_value(elem)
            # We need to include the type tag along with the value encoding for lists
            encoded_elems.append(f"{type_tag}:{encoded_elem}")
        return 'L', '[' + '|'.join(encoded_elems) + ']'

    # Dictionaries/objects
    if isinstance(value, dict):
        # Recursively encode as a miniature ObfUX string (without the outer
        # wrappers).  We call ``encode`` which returns the full string with
        # wrappers; remove the first and last character (💫) to embed.
        inner = encode(value)
        # Remove the outer 💫 wrappers
        assert inner.startswith('💫') and inner.endswith('💫')
        return 'O', inner[1:-1]

    raise TypeError(f"Unsupported type: {type(value)}")


def decode_value(type_tag: str, encoded: str) -> Any:
    """Decode a value based on its type tag and encoded representation.

    The decoding logic mirrors ``encode_value``.
    """
    if type_tag == 'S':
        # Remove sparkles and split by '-' to get codes in reversed order,
        # then reverse back to original order.  Subtract the index to
        # restore the original ASCII code.
        codes = encoded.split('-') if encoded else []
        codes = list(reversed(codes))
        chars = []
        for i, code_str in enumerate(codes):
            code_int = base_to_int(code_str, 32, BASE32_ALPHABET)
            ascii_code = code_int - i
            chars.append(chr(ascii_code))
        return ''.join(chars)

    if type_tag == 'N':
        parts = encoded.split('&') if encoded else []
        parts = list(reversed(parts))
        chars: List[str] = []
        for i, hex_str in enumerate(parts):
            code_int = int(hex_str, 16)
            ascii_code = code_int + i
            chars.append(chr(ascii_code))
        num_str = ''.join(chars)
        # Convert string back to number (int if possible, else float)
        if '.' in num_str or 'e' in num_str or 'E' in num_str:
            return float(num_str)
        return int(num_str)

    if type_tag == 'B':
        return True if encoded == '👍' else False

    if type_tag == 'U':
        return None

    if type_tag == 'L':
        # Strip brackets and split by '|' to get elements.  Each element
        # includes its own type tag separated by ':' from the encoded value.
        assert encoded.startswith('[') and encoded.endswith(']'), "Invalid list encoding"
        inner = encoded[1:-1]
        if not inner:
            return []
        elems_str = inner.split('|')
        result_list = []
        for elem in elems_str:
            if ':' not in elem:
                raise ValueError(f"Invalid list element encoding: {elem}")
            sub_type, sub_encoded = elem.split(':', 1)
            result_list.append(decode_value(sub_type, sub_encoded))
        return result_list

    if type_tag == 'O':
        # Reconstruct the full string by wrapping with 💫 on both ends, then
        # call the top‑level decode.  ``decode`` expects the full wrapper.
        wrapped = '💫' + encoded + '💫'
        return decode(wrapped)

    raise ValueError(f"Unknown type tag: {type_tag}")


def encode(data: Dict[str, Any]) -> str:
    """Encode a Python dictionary into the ObfUX string format.

    :param data: Dictionary of values to encode.
    :returns: A string representing the encoded object.
    """
    if not isinstance(data, dict):
        raise TypeError("encode() expects a dictionary at the top level")

    parts = []
    for key, value in data.items():
        encoded_key = encode_key(key)
        type_tag, encoded_val = encode_value(value)
        parts.append(f"{encoded_key}🐉{type_tag}🐉{encoded_val}")
    # Join pairs with 🧟 and wrap with 💫
    return '💫' + '🧟'.join(parts) + '💫'


def decode(encoded_str: str) -> Dict[str, Any]:
    """Decode a string in the ObfUX format back into a Python dictionary.

    :param encoded_str: The encoded string, including the outer wrappers.
    :returns: A dictionary representing the original data.
    """
    if not (encoded_str.startswith('💫') and encoded_str.endswith('💫')):
        raise ValueError("Encoded string missing outer 💫 wrappers")

    inner = encoded_str[1:-1]
    if not inner:
        return {}
    result: Dict[str, Any] = {}
    pairs = inner.split('🧟')
    for pair in pairs:
        try:
            key_enc, type_tag, val_enc = pair.split('🐉', 2)
        except ValueError:
            raise ValueError(f"Invalid encoded pair: {pair}")
        key = decode_key(key_enc)
        result[key] = decode_value(type_tag, val_enc)
    return result


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _write_json(data: Dict[str, Any], path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _read_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def _write_text(text: str, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def main(argv: List[str] | None = None) -> int:
    """Entry point for command line usage.

    Usage::

        python encoder_decoder.py encode input.json output.ux
        python encoder_decoder.py decode input.ux output.json

    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 3 or argv[0] not in {'encode', 'decode'}:
        print("Usage: python encoder_decoder.py encode|decode input_file output_file")
        return 1
    command, input_path, output_path = argv
    if command == 'encode':
        data = _read_json(input_path)
        encoded = encode(data)
        _write_text(encoded, output_path)
    else:  # decode
        encoded = _read_text(input_path)
        data = decode(encoded.strip())
        _write_json(data, output_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())