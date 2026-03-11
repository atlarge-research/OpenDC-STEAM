echo "Plotting figures for the paper..."

echo "Plotting battery capacity..."
python plotting_functions/battery_capacity.py

echo "Plotting battery charging..."
python plotting_functions/battery_charging.py

echo "Plotting battery embodied..."
python plotting_functions/battery_embodied.py

echo "Plotting battery impact..."
python plotting_functions/battery_impact.py

echo "Plotting combined techniques..."
python plotting_functions/combined_techniques.py

echo "Plotting horizontal scaling..."
python plotting_functions/horizontal_scaling.py

echo "Plotting optimal battery..."
python plotting_functions/optimal_battery.py

echo "Plotting technique impact..."
python plotting_functions/technique_impact.py

echo "Finished plotting all figures!"