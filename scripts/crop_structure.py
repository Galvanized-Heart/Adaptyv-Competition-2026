import argparse
from pathlib import Path

from biotite.structure import get_residues
from biotite.structure.io import load_structure, save_structure


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("--chain", required=True)
parser.add_argument("--start", required=True, type=int)
parser.add_argument("--end", required=True, type=int)

args = parser.parse_args()

structure = load_structure(args.input, model=1)

selection = (
    (structure.chain_id == args.chain)
    & (~structure.hetero)
    & (structure.res_id >= args.start)
    & (structure.res_id <= args.end)
)

cropped = structure[selection]

if len(cropped) == 0:
    raise RuntimeError("Selection contained no atoms")

res_ids, res_names = get_residues(cropped)

print(
    f"Selected chain {args.chain}: "
    f"{res_ids.min()}-{res_ids.max()} "
    f"({len(res_ids)} residues)"
)

histidines = [
    int(rid)
    for rid, name in zip(res_ids, res_names)
    if name == "HIS"
]

print("Histidines:", histidines)

Path(args.output).parent.mkdir(parents=True, exist_ok=True)
save_structure(args.output, cropped)

print("Wrote:", args.output)
