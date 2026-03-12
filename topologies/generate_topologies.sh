if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Python is not installed."
    exit 1
fi

echo "Generating topologies..."

echo "Surf..."
$PYTHON topologies/generate_topologies_surf.py

echo "Marconi..."
$PYTHON topologies/generate_topologies_marconi.py

echo "Borg..."
$PYTHON topologies/generate_topologies_borg.py