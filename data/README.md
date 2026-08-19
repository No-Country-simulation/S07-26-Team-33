# Mapeo de archivos de datos

| Archivo | Metrica | Campos clave | Registros |
|---|---|---|---|
| data_1.json | Average utilization | average_utilization_pct, peak_utilization_pct, valley_utilization_pct | 100,000 |
| data_6.json | Utilization range (%) | pct_utilizacion_promedio, pct_inactivo, utilizacion_peak, utilizacion_valle | 95,000 |
| data_3.json | PUE | pue, cop, wue, eficiencia_kw_cooling_por_kw_it, tipos_cooling | 88,000 |
| data_5.json | Cooling efficiency | pue, wue, power_it_mw, power_cooling_mw, power_total_mw, tipos_cooling | 95,000 |
| data_4.json | Precio (costo de construir un data center) | costo_total_usd, costo_por_mw_usd, costo_por_sqft_usd, tiers | 100,000 |
| data_2.json | Costo por MW de capacidad | costo_usd_por_mw (+min/max), capacidad_mw | 82,555 |

Pendiente de confirmar con el equipo: data_3/data_5 comparten variables (pue, wue) y data_2/data_4 comparten variables de costo por MW - verificar si miden cosas distintas o hay solapamiento de esfuerzo entre quienes las armaron.
