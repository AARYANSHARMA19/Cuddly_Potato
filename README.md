ObfUX: The Cursed Data Format

Welcome to the most unhinged data format you never asked for. This
project was created for a winter‑themed hackathon that challenged
participants to invent a catastrophically complex encoding scheme with
both an encoder and a decoder. The goal? To leave fellow engineers in
a perpetual state of confusion, wondering “but why?” as they comb
through emoji‑laden strings.

📜 Problem Statement

The hackathon brief asked us to accept a simple input.json with
arbitrary structured data and transform it into a new format. The
format should resemble JSON or XML only in spirit. In practice it
should be deliberately inscrutable and humorous—think
hieroglyphics meets Lovecraftian apocrypha. On top of encoding, we
also needed to provide a decoder capable of reconstructing the original
data (because the walk of shame only works if there’s proof it ever
worked).

From the event slides:

“Right now it’s boring JSON, but your job? Make it absolutely unhinged.”

“Don’t write any documentation!!! (You know nothing, Jon Snow, and
neither should your teammates.)”

Yet here we are, defiantly writing documentation anyway because your
future self will thank you. 😉

🦄 Meet ObfUX (Obfuscated Unicorn Exchange)

ObfUX is a text‑based format that uses emoji as structural markers and
obscure number bases to confound readers. At its core, it simply
serialises Python dictionaries (or JSON objects) into a single string.
Here’s what makes it special:

Feature	Description
Outer wrapper	Every encoded string begins and ends with the 💫 emoji.
Pair separator	Individual key/value pairs are separated by the zombie emoji 🧟. Because your coworkers will feel like zombies trying to decode it.
Field separator	Within a pair, the encoded key, a one‑letter type tag and the encoded value are separated by the dragon emoji 🐉.
Key encoding	Each character’s ASCII byte has its bits reversed, then converted to base 36 and joined with periods (e.g., 'name' → '3a.3q.52.4m').
Type tags	S for strings, N for numbers, B for booleans, L for lists, O for objects/dicts and U for null/None.
Value encoding	Depends on the type: strings shift character codes and use base 32, numbers alter codes and use hexadecimal, lists recursively annotate types, booleans become 👍/👎 and null becomes 💤.

Altogether, a simple object like {"age": 24} becomes:

💫3q.6e.4m🐉N🐉33&32💫


Beautifully cursed, isn’t it?

🧠 How Encoding Works

Here’s a breakdown of the encoding process:

Key encoding: Each character of a key has its 8‑bit pattern reversed (for no good reason other than to confuse). The resulting integer is converted to base 36 using the digits 0–9a–z. The codes are joined with periods. For example, 'age' becomes 3q.6e.4m.

Type tag: We prepend a single character denoting the type of the value: S, N, B, L, O or U.

Value encoding: The value itself is then encoded according to its type:

Strings: For each character, we add the character’s index to its ASCII code, convert to base 32 (using digits 0–9a–v), reverse the list of codes and join with -. This order reversal ensures reading left‑to‑right yields a seemingly random string.

Numbers: Convert the number to a string. Each character has its code reduced by its index, is written in hex and the sequence is reversed and joined with &.

Booleans: True becomes 👍, False becomes 👎.

Lists: Each element is encoded separately, prefixed with its own type tag, joined with | and wrapped in brackets ([ ]).

Objects/Dictionaries: We recursively encode them as ObfUX strings (without the outer 💫), store them as the value of type O.

Null/None: Represented by 💤.

Finally, pairs are concatenated with 🧟 and wrapped with 💫…💫.

🔁 Decoding

The decoder performs the inverse operations:

It strips the outer 💫, splits pairs on 🧟, splits fields on 🐉, decodes keys back to their original form and then dispatches based on the type tag.

Base conversions are reversed and indices are added or subtracted appropriately.

Lists and objects decode their contents recursively.

By following these steps, every encoding is fully reversible, no matter how bizarre it may look.

💻 Usage

To run the encoder or decoder directly from the command line:

python3 encoder_decoder.py encode input.json output.ux
python3 encoder_decoder.py decode output.ux roundtrip.json


The script reads the input file, encodes or decodes it depending on the
command and writes the result to the output file. You can also import
the encode and decode functions directly in your own Python code.

📂 Repository Contents
File	Purpose
encoder_decoder.py	Implementation of the ObfUX encoder and decoder.
README.md	You’re reading it! Explains the format and usage.
slides/	Contains a presentation summarising the project and the hackathon context.
IMG_3669.PNG, Screenshot 2025‑11‑27 at…	Reference images from the hackathon briefing. They inspired the meta‑humour and wintery theme.
🎞️ Presentation

We’ve prepared a short slide deck (see the slides directory) that
introduces the hackathon, outlines the problem statement, explains the
encoding scheme with visuals and concludes with examples. Feel free to
open it in your favourite slide viewer.

🤔 Final Thoughts

ObfUX isn’t meant for production use. It’s a playful exploration of
what happens when you prioritise obfuscation over clarity. However,
working through its design will strengthen your understanding of
serialisation, recursion and base conversions. At the very least it
will give your colleagues a good laugh (or a headache). Enjoy!
