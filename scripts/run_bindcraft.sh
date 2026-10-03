#!/bin/bash
#SBATCH --account=rrg-mahadeva_gpu
#SBATCH --job-name=bindcraft
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --gpus=h100_3g.40gb:1
#SBATCH --output=logs/bindcraft_%j.out

set -euo pipefail

cd /project/6007171/maxkirby/adaptyv/BindCraft2

export XDG_CACHE_HOME=/project/6007171/maxkirby/adaptyv/.cache
export BINDCRAFT_WORKERS_PER_GPU=1

source .venv/bin/activate

echo "=== GPU ==="
nvidia-smi

echo "=== JAX ==="
python - <<'PY'
import jax
print("JAX:", jax.__version__)
print("devices:", jax.devices())
print("backend:", jax.default_backend())
assert jax.default_backend() == "gpu"
PY

echo "=== BindCraft ==="
bindcraft design "$@"