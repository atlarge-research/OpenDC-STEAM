echo "Generating topologies..."

echo "Surf..."
python topologies/generate_topologies_surf.py

echo "Marconi..."
python topologies/generate_topologies_marconi.py

echo "Borg..."
python topologies/generate_topologies_borg.py