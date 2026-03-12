if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Python is not installed."
    exit 1
fi

echo "Plotting figures for the paper..."

echo "Plotting battery capacity..."
$PYTHON plotting_functions/battery_capacity.py

echo "Plotting battery charging..."
$PYTHON plotting_functions/battery_charging.py

echo "Plotting battery embodied..."
$PYTHON plotting_functions/battery_embodied.py

echo "Plotting battery impact..."
$PYTHON plotting_functions/battery_impact.py

echo "Plotting combined techniques..."
$PYTHON plotting_functions/combined_techniques.py

echo "Plotting horizontal scaling..."
python plotting_functions/horizontal_scaling.py

echo "Plotting optimal battery..."
python plotting_functions/optimal_battery.py

echo "Plotting technique impact..."
python plotting_functions/technique_impact.py

echo "Finished plotting all figures!"