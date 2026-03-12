if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Python is not installed."
    exit 1
fi

echo "Generating experiments..."

echo "Surf..."
$PYTHON experiments/generate_experiments_surf.py

echo "Marconi..."
$PYTHON experiments/generate_experiments_marconi.py

echo "Borg..."
$PYTHON experiments/generate_experiments_borg.py