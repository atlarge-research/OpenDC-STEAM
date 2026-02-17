echo "Generating experiments..."

echo "Surf..."
python experiments/generate_experiments_surf.py

echo "Marconi..."
python experiments/generate_experiments_marconi.py

echo "Borg..."
python experiments/generate_experiments_borg.py