from pathlib import Path

import numpy as np
from biotite.structure import get_residues
from biotite.structure.io import load_structure


FILES = [
    Path("targets/egfr/raw/6ARU.cif"),
    Path("targets/egfr/raw/AF-Q01279-F1-model_v6.cif"),
]


def inspect(path):
    structure = load_structure(path, model=1)

    print()
    print("=" * 80)
    print(path)
    print("=" * 80)

    for chain in np.unique(structure.chain_id):
        atoms = structure[
            (structure.chain_id == chain)
            & (~structure.hetero)
        ]

        if len(atoms) == 0:
            continue

        ids, names = get_residues(atoms)

        print(
            f"chain={chain!r:5} "
            f"residues={len(ids):4} "
            f"range={ids.min()}-{ids.max()}"
        )

        # Print histidines in the extracellular/domain-III-ish region
        histidines = [
            int(rid)
            for rid, name in zip(ids, names)
            if name == "HIS" and 250 <= rid <= 600
        ]

        if histidines:
            print("  HIS residues 250-600:", histidines)

        # Useful positions for our expected numbering schemes
        residue_map = {
            int(rid): name
            for rid, name in zip(ids, names)
        }

        probes = [
            311, 335,
            346, 370,
            409, 433,
            514, 538,
        ]

        print("  probe residues:")
        for residue in probes:
            if residue in residue_map:
                print(
                    f"    {residue:4}: {residue_map[residue]}"
                )


for path in FILES:
    inspect(path)
