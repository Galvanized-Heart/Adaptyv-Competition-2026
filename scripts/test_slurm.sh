#!/bin/bash
#SBATCH --account=rrg-mahadeva_gpu
#SBATCH --job-name=bc2_gpu_test
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --gpus=h100_1g.10gb:1
#SBATCH --output=logs/gpu_test_%j.out

set -euo pipefail

cd /project/6007171/maxkirby/adaptyv/BindCraft2

export XDG_CACHE_HOME=/project/6007171/maxkirby/adaptyv/.cache

source .venv/bin/activate

nvidia-smi

python - <<'PY'
import jax
print("JAX:", jax.__version__)
print("devices:", jax.devices())
print("backend:", jax.default_backend())
PY