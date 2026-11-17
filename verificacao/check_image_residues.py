from pathlib import Path
import json

MAX_BITS = 16
modulus = 1 << MAX_BITS
values = set()
for n in range(modulus):
    choose = 1
    total = 1
    for k in range(1, min(n, MAX_BITS - 1) + 1):
        choose = choose * (n - k + 1) // k
        total = (total + (1 << k) * choose * choose) % modulus
    values.add(total)

rows = []
for bits in range(4, MAX_BITS + 1):
    mod = 1 << bits
    actual = {v % mod for v in values}
    predicted = {1, mod - 1}
    predicted.update(range(3, mod, 16))
    predicted.update(range(13, mod, 16))
    for a in range(2, (bits - 1) // 3 + 1):
        step = 1 << (3 * a + 1)
        predicted.update(range(1 + (1 << (3*a)), mod, step))
        predicted.update(range(-1 + (1 << (3*a)), mod, step))
    assert actual == predicted, (bits, actual ^ predicted)
    rows.append({'bits': bits, 'number_of_image_residues': len(actual),
                 'residue_proportion': len(actual) / mod,
                 'matches_image_formula': True})
result = {'integer_indices_checked': modulus, 'max_bits': MAX_BITS,
          'failures': 0, 'limiting_haar_measure_from_proof': '1/7', 'levels': rows,
          'caution': 'Finite check is corroboration, not proof of image surjectivity or novelty.'}
dest = Path(__file__).with_suffix('.json')
dest.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
