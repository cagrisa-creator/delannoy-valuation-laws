"""Check internal consistency of the supplied NEG archive using stdlib only.

This does not recompute T_k, layer sums, valuations, or a tail bound. Those
definitions and the generating source are not part of the supplied archive.
The scope of each check is stated explicitly in the generated JSON report.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
import re
import zipfile


DEFAULT_ARCHIVE = Path(__file__).resolve().parent.parent / 'suplemento' / 'NEG_original.zip'


def parse_assignment(text: str, name: str):
    match = re.search(r'^' + re.escape(name) + r'=(.+)$', text, re.M)
    if not match:
        raise ValueError(f'Missing metadata {name}')
    return ast.literal_eval(match.group(1))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive', nargs='?', type=Path, default=DEFAULT_ARCHIVE)
    ap.add_argument('--output', type=Path, default=Path(__file__).with_name('archive_integrity_report.json'))
    args = ap.parse_args()
    payload = args.archive.read_bytes()
    errors = []
    checks = Counter()

    def require(condition, check, context=None):
        checks[check] += 1
        if not condition:
            errors.append({'check': check, 'context': context})

    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        require(archive.testzip() is None, 'zip_crc')
        info = [{'name': entry.filename, 'bytes': entry.file_size,
                 'sha256': hashlib.sha256(archive.read(entry)).hexdigest()}
                for entry in archive.infolist()]
        metadata = archive.read('resultado_delannoy_negative_finite_certificate.txt').decode('utf-8-sig')
        records = json.loads(archive.read('delannoy_negative_ladder_certificate.json').decode('utf-8-sig'))
        rows = list(csv.DictReader(io.StringIO(archive.read('delannoy_negative_ladder_certificate.csv').decode('utf-8-sig'))))

    a_values = parse_assignment(metadata, 'A_VALUES')
    q_values = parse_assignment(metadata, 'Q_VALUES')
    u_values = parse_assignment(metadata, 'U_VALUES')
    s_max = parse_assignment(metadata, 'S_MAX')
    declared_total = s_max * len(a_values) * len(q_values) * len(u_values)
    require(declared_total == 104448, 'declared_grid_product')
    require(len(rows) == len(records) == 11858, 'state_count')
    keys_seen = set()
    sum_count = 0
    ladder_lengths = Counter()
    active_counts = Counter()
    counts_multiplicity = Counter()
    a_present, s_present, pmod_present = set(), set(), set()
    prior_cumulative_nonnegative = 0
    nonconsecutive_ladders = 0
    q_frequency = Counter(q % 256 for q in q_values)
    u_frequency = Counter(u % 128 for u in u_values)

    for line, row in enumerate(rows, start=2):
        state = [int(row[x]) for x in ['pmod', 's', 'a', 'q_mod_256', 'u_mod_128']]
        key = json.dumps(state, separators=(',', ':'))
        require(key not in keys_seen, 'csv_unique_key', key)
        keys_seen.add(key)
        require(key in records, 'csv_key_in_json', key)
        if key not in records:
            continue
        record = records[key]
        require(json.loads(key) == record['state'] == state, 'json_key_state', key)
        integer_fields = ['count', 'H', 'active_count', 'ladder_len', 'vnonneg_example']
        for field in integer_fields:
            require(int(row[field]) == record[field], 'csv_json_' + field, key)
        tuple_fields = ['active_ks', 'ladder', 'Umods_example']
        for field in tuple_fields:
            csv_value = ast.literal_eval(row[field])
            require(json.loads(json.dumps(csv_value)) == record[field], 'csv_json_' + field, key)
        ladder = record['ladder']
        require(record['count'] >= 1, 'positive_state_multiplicity', key)
        require(len(ladder) == record['ladder_len'], 'ladder_length', key)
        require(bool(ladder) and ladder[-1] == [-1, 0], 'ladder_last_minus1_zero', key)
        require(all(len(item) == 2 and all(isinstance(x, int) for x in item) for item in ladder), 'ladder_integer_pairs', key)
        require(all(item[0] < 0 for item in ladder), 'negative_layer_margins', key)
        require(all(b[0] > a[0] for a,b in zip(ladder, ladder[1:])), 'strictly_increasing_layer_margins', key)
        nonconsecutive_ladders += not all(b[0] == a[0]+1 for a,b in zip(ladder, ladder[1:]))
        require(len(record['active_ks']) == record['active_count'], 'active_indices_count', key)
        require(record['active_count'] % 2 == 0, 'even_active_count', key)
        require(record['vnonneg_example'] > 0, 'example_nonnegative_block_strict_gain', key)
        require(len(record['Umods_example']) == 4, 'four_unit_modulus_examples', key)
        prior_cumulative_nonnegative += sum(item[1] >= 0 for item in ladder[:-1])

        example = record['example']
        pmod, s, a, qmod, umod = state
        require(1 <= s <= s_max and a in a_values and qmod in q_frequency and umod in u_frequency, 'key_in_declared_grid', key)
        require(example['a'] == a and example['s'] == s and example['pmod'] == pmod, 'example_exact_parameters', key)
        require(example['q'] in q_values and example['u'] in u_values, 'example_in_declared_lists', key)
        require(example['q'] % 256 == example['q256'] == qmod, 'example_q_residue', key)
        require(example['u'] % 128 == example['u128'] == umod, 'example_u_residue', key)
        require(example['q'] % 2 == 1 and example['u'] % 2 == 1, 'example_odd_units', key)
        require(example['p'] == 1 + (1 << s) * example['q'], 'example_multiplier_definition', key)
        require(example['p'] % 8 == pmod, 'example_multiplier_mod8', key)
        expected_multiplicity = q_frequency[qmod] * u_frequency[umod]
        require(record['count'] == expected_multiplicity, 'state_multiplicity_matches_grid_aliases', key)
        sum_count += record['count']
        ladder_lengths[record['ladder_len']] += 1
        active_counts[record['active_count']] += 1
        counts_multiplicity[record['count']] += 1
        a_present.add(a); s_present.add(s); pmod_present.add(pmod)

    require(keys_seen == set(records), 'csv_json_identical_key_sets')
    require(sum_count == 13552, 'negative_case_count')
    require(dict(active_counts) == {0: 9044, 2: 2814}, 'reported_active_count_distribution')
    report = {
        'audit_kind': 'Internal archive consistency only; no recomputation of the mathematical certificate',
        'archive_sha256': hashlib.sha256(payload).hexdigest(),
        'archive_bytes': len(payload),
        'archive_files': info,
        'declared_grid': {'s': list(range(1,s_max+1)), 'a': a_values, 'q': q_values, 'u': u_values,
                          'raw_parameter_combinations': declared_total},
        'actual_retained_data': {'csv_rows': len(rows), 'json_states': len(records), 'sum_recorded_state_multiplicities': sum_count,
                                 'a_values': sorted(a_present), 's_values': sorted(s_present), 'p_mod8_values': sorted(pmod_present),
                                 'state_multiplicity_distribution': dict(sorted(counts_multiplicity.items())),
                                 'ladder_length_distribution': dict(sorted(ladder_lengths.items())),
                                 'active_count_distribution': dict(sorted(active_counts.items())),
                                 'prior_cumulative_ladder_entries_with_nonnegative_normalized_value': prior_cumulative_nonnegative,
                                 'ladders_with_gaps_between_layer_margins': nonconsecutive_ladders},
        'checks_by_name': dict(checks), 'checks_total': sum(checks.values()),
        'errors_count': len(errors), 'errors_by_check':dict(Counter(e['check'] for e in errors)), 'errors': errors[:100],
        'status': 'INTERNAL_CONSISTENCY_PASS' if not errors else 'INTERNAL_CONSISTENCY_FAIL',
        'what_was_not_verified': [
            'The 104448 original executions: only the declared Cartesian grid size is reconstructible.',
            'The non-NEG cases: the archive retains the NEG states, not all original case records.',
            'The numerical values of T_k, H, negative layer sums, and their 2-adic valuations.',
            'The claimed tail bound or the equality of the full Delannoy difference with the decomposed sums.',
            'Absence of conflicting omitted raw states; matching retained CSV and JSON is not an independent experiment.',
            'A universal reduction to residues of q mod 256 and u mod 128.',
            'Coverage of arbitrary a,s: the state key itself retains exact, unbounded a,s.'
        ],
        'missing_material': ['Generating/verifying source for the mathematical NEG certificate',
                             'Definitions of T_k and the cutoff H(a-1)',
                             'Written proof of the tail bound and global finite-state reduction'],
        'terminology': 'NEG means v2(T_k)-w<0 in a term decomposition, not a negative Delannoy index or a negative shift.',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'status': report['status'], 'checks': report['checks_total'], 'errors': report['errors_count'],
                      'csv_rows': len(rows), 'recorded_NEG_cases': sum_count, 'archive_sha256': report['archive_sha256']}, indent=2))
    if errors:
        print(json.dumps(errors[:20],indent=2))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
