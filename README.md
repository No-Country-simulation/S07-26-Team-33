# Data Center Analytics - Stranded Capacity Intelligence

# S07-26-Team-33

## Índice

1. [Introducción](#introducción)
2. [Qué es Stranded Capacity](#qué-es-stranded-capacity)
3. [Modelo de Estimación](#modelo-de-estimación)
4. [Datasets y Fuentes](#datasets-y-fuentes)
5. [Instalación y Uso](#instalación-y-uso)
6. [Estructura del Proyecto](#estructura-del-proyecto)
7. [Supuestos del Modelo](#supuestos-del-modelo)
8. [Referencias](#referencias)

---

## Introducción

**Data Center Analytics** es una herramienta de inteligencia de capacidad diseñada para medir y cuantificar el problema de **"Stranded Capacity"** en data centers modernos.

### El Problema

En la industria de data centers, existe un desperdicio silencioso pero costoso: capacidad pagada y energizada que no produce valor. Esto ocurre cuando las capas físicas, eléctricas y operativas del facility no se coordinan entre sí, generando:

- Megavatios inactivos que consumen energía sin generar ingresos
- Capital inmovilizado en infraestructura no utilizada
- Costos de oportunidad por inversiones que podrían generar retorno

### La Solución

Este dashboard permite a operadores y dueños de data centers:

1. Estimar su capacidad stranded en porcentaje y megavatios
2. Cuantificar el impacto financiero (capital inmovilizado + costo de oportunidad)
3. Comparar su desempeño contra benchmarks de la industria
4. Proyectar escenarios de recuperación
5. Identificar oportunidades de mejora

---

## Qué es Stranded Capacity

**Stranded Capacity** es la porción de capacidad instalada que:

- Está pagada (inversión ya realizada)
- Está encendida (energizada y operativa)
- No produce valor (no genera ingresos ni retorno)

### Fórmula Conceptual

```
Stranded Capacity = Idle Capacity - Headroom Legítimo
```

Donde:

| Concepto | Definición |
|----------|------------|
| **Idle Capacity** | Capacidad total no utilizada (100% - Utilización Actual) |
| **Headroom Legítimo** | Margen operativo necesario para picos de demanda y seguridad |
| **Stranded Capacity** | Capacidad ociosa que podría ser aprovechada |

### Ejemplo Práctico

```
Facility: 100 MW
Utilización Actual: 55%
Idle Capacity: 45 MW (45%)

Peak Delta (Tier III): 14% → Peak = 69%
Safety Margin (Tier III): 20% → Headroom = 89%

Stranded = 100% - 89% = 11% = 11 MW
```

**Interpretación:** De los 45 MW ociosos, solo 11 MW son realmente "stranded". Los otros 34 MW son necesarios para picos de demanda y seguridad operativa.

---

## Modelo de Estimación

### Inputs del Modelo

| Input | Descripción | Rango |
|-------|-------------|-------|
| **Facility MW** | Capacidad total del data center | 1 - 1000 MW |
| **Average Utilization** | Utilización promedio actual | 0 - 100% |
| **Cooling Type** | Tipo de refrigeración | Air / Liquid / Hybrid |
| **País** | Ubicación geográfica | 25+ países |
| **Tier** | Nivel de disponibilidad | Tier I - IV |
| **Market Demand** | Demanda del mercado | Baja / Media / Alta / Muy Alta |

### Outputs del Modelo

| Output | Descripción | Unidad |
|--------|-------------|--------|
| **Stranded Capacity** | Capacidad inmovilizada | % y MW |
| **Capital Inmovilizado** | Capital asociado a capacidad stranded | USD |
| **Costo de Oportunidad** | Costo anual del capital inmovilizado | USD/año |
| **Recovery Time** | Tiempo estimado de recuperación | años |
| **Utilization Gap** | Brecha vs benchmark de industria | puntos porcentuales |

---

### Fórmulas del Modelo

#### Fórmula 1: Peak Utilization

```
Peak = Average Utilization + Peak Delta
```

**Peak Delta por Tier:**

| Tier | Peak Delta |
|------|------------|
| Tier I | 18% |
| Tier II | 16% |
| Tier III | 14% |
| Tier IV | 12% |

---

#### Fórmula 2: Headroom Legítimo

```
Headroom = Peak Utilization - Safety Margin
```

**Safety Margin por Tier:**

| Tier | Safety Margin |
|------|---------------|
| Tier I | 15% |
| Tier II | 18% |
| Tier III | 20% |
| Tier IV | 25% |

---

#### Fórmula 3: Stranded Capacity

```
Idle Capacity = 100% - Average Utilization
Stranded % = max(0, Idle Capacity - Headroom)
Stranded MW = Facility MW × Stranded %
```

---

#### Fórmula 4: PUE Inferido

```
PUE = f(Cooling Type, Climate)
```

| Cooling | Frío | Templado | Cálido |
|---------|------|----------|--------|
| Air-cooled | 1.15 | 1.25 | 1.35 |
| Liquid-cooled | 1.05 | 1.08 | 1.12 |
| Hybrid | 1.09 | 1.15 | 1.22 |

---

#### Fórmula 5: Costo Energético Anual

```
Energy Loss = Stranded MW × 8,760 × PUE × Tarifa
```

Donde:
- 8,760 = horas anuales
- Tarifa = precio de electricidad por kWh

---

#### Fórmula 6: Capital Inmovilizado

```
Stranded CapEx = Stranded MW × CapEx/MW
```

---

#### Fórmula 7: Costo de Oportunidad

```
Costo Oportunidad = Stranded CapEx × WACC (10%)
```

Donde WACC = Weighted Average Cost of Capital

---

#### Fórmula 8: Pérdida Total Anual

```
Pérdida Total Anual = Energy Loss + Costo Oportunidad
```

---

#### Fórmula 9: Recovery Time

```
Recovery Time = ln(Target Utilization / Current Utilization) / ln(1 + Growth Rate)
```

---

#### Fórmula 10: Utilization Gap

```
Gap = Benchmark - Average Utilization
```

**Benchmark por Tier:**

| Tier | Benchmark |
|------|-----------|
| Tier I | 45% |
| Tier II | 55% |
| Tier III | 62% |
| Tier IV | 85% |

---

### Rangos de Confianza

El modelo expresa resultados en **rangos de confianza** para ser honesto sobre la incertidumbre:

| Variable | Incertidumbre | Justificación |
|----------|---------------|---------------|
| Stranded MW | ±12% | Variabilidad en datasets de utilización |
| Energy Loss | ±15% | Variabilidad en tarifas eléctricas |
| Stranded CapEx | ±10% | Datos de CapEx más estables |
| Costo Oportunidad | ±15% | Variabilidad en WACC |
| Recovery Time | ±20% | Mayor incertidumbre en proyecciones |

---

## Datasets y Fuentes

### Estructura de Datasets

| Dataset | Nombre | Registros | Propósito |
|---------|--------|-----------|-----------|
| **Dataset 1** | Average Utilization | 100,000 | Utilización por país, tier y workload |
| **Dataset 2** | Utilization Range Summary | 95,000 | Rangos de utilización y desviaciones |
| **Dataset 3** | Precio Construcción / CapEx | 25,000 | Costos de construcción por MW |
| **Dataset 4** | Cooling Efficiency / PUE | 88,000 | PUE por clima y tipo de cooling |
| **Dataset 5** | PUE Actual / Argentina | 95,000 | Datos de referencia para Argentina |
| **Dataset 6** | Utilization Range | 95,000 | Distribución de utilización |

### Metodología de Construcción

Los datasets son **sintéticos** y fueron generados a partir de distribuciones estadísticas coherentes con las fuentes citadas. No contienen datos reales de facilidades específicas.

**Principios de construcción:**

1. Distribuciones normales alrededor de benchmarks por tier
2. Factores de corrección por país (mercados maduros vs emergentes)
3. Workloads asignados según patrones de la industria
4. Rangos construidos usando percentiles 10-90 de la distribución global

---

## Instalación y Uso

### Requisitos

- Python 3.9 o superior
- pip (gestor de paquetes)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/No-Country-simulation/S07-26-Team-33.git
cd data_center_dashboard

# Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
streamlit run app.py
```

La aplicación estará disponible en: `http://localhost:8501`

### Requirements.txt

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
```

---

## Estructura del Proyecto

```
data_center_dashboard/
│
├── app.py                          # Punto de entrada principal
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Documentación del proyecto
├── .gitignore                      # Archivos ignorados por git
│
├── models/                         # Lógica del modelo
│   ├── __init__.py                 # Inicializador del paquete
│   ├── calculator.py               # Motor de cálculo principal
│   ├── datasets.py                 # Carga y gestión de datasets
│   └── lookup_tables.py            # Tablas de referencia
│
├── components/                     # Componentes de interfaz
│   ├── __init__.py                 # Inicializador del paquete
│   ├── banner.py                   # Banner dinámico
│   └── charts.py                   # Generación de gráficos
│
└── data/                           # Datos en formato JSON
    ├── data_1.json                 # Average Utilization
    ├── data_2.json                 # Utilization Range Summary
    ├── data_3.json                 # Precio Construcción / CapEx
    ├── data_4.json                 # Cooling Efficiency / PUE
    ├── data_5.json                 # PUE Actual / Argentina
    └── data_6.json                 # Utilization Range
```

### Descripción de Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| **app.py** | Aplicación principal Streamlit con UI y routing |
| **calculator.py** | Motor de cálculo con todas las fórmulas del modelo |
| **datasets.py** | Funciones para cargar y consultar los datasets |
| **lookup_tables.py** | Tablas de referencia (PUE, benchmarks, etc.) |
| **charts.py** | Generación de 11 gráficos interactivos con Plotly |
| **banner.py** | Banner dinámico con estado de severidad |

---

## Supuestos del Modelo

### Supuestos Clave

| Supuesto | Valor | Fuente | Justificación |
|----------|-------|--------|---------------|
| Factor de Energización | 70% | Uptime Institute 2024 | 70% de la capacidad stranded está energizada |
| Costo de Oportunidad (WACC) | 10% | Deloitte 2024 | WACC típico para inversiones en data centers |
| Factor de Recuperación | 60% | AFCOM 2024 | 60% de la capacidad stranded es recuperable |
| Incertidumbre Base | 15% | Variabilidad de datasets | Incertidumbre estándar en estimaciones |

### Limitaciones

1. **Datos sintéticos:** Los datasets son representaciones sintéticas, no datos reales
2. **Rangos estimados:** Todos los valores son estimaciones basadas en fuentes públicas
3. **Actualización anual:** Los datos deben actualizarse con nuevos reportes
4. **Orden de magnitud:** El modelo estima órdenes de magnitud, no valores exactos

---

## Referencias

### Consultoras Inmobiliarias

1. **CBRE Research** - Global Data Center Trends
   https://www.cbre.com/insights/reports/global-data-center-trends

2. **JLL** - Data Center Outlook
   https://www.us.jll.com/en/trends-and-insights/research/data-center-report

3. **Cushman & Wakefield** - Global Data Center Market Comparison
   https://www.cushmanwakefield.com/en/insights/reports/data-center-report

### Think Tanks y Laboratorios Nacionales

4. **Epoch AI** - AI Datacenter Cost Breakdown
   https://epoch.ai/data-insights/ai-datacenter-cost-breakdown

5. **Thunder Said Energy** - Data Centers: The Economics
   https://thundersaidenergy.com/downloads/data-centers-the-economics/

6. **LBNL + Uptime Institute** - True TCO Model
   https://datacenters.lbl.gov/resources/total-cost-ownership-tco-model-data

7. **PNNL (DOE)** - IM3 Data Center Atlas
   https://im3.pnnl.gov/datacenter-atlas

8. **DCGen - Argonne National Lab**
   https://github.com/WedanEmmanuel/DCGen

9. **NREL** - Annual Technology Baseline
   https://atb.nrel.gov/

10. **Sandia National Labs** - QuESt Planning
    https://github.com/sandialabs/quest_planning

### Fuentes Gubernamentales

11. **EIA Open Data API**
    https://www.eia.gov/opendata/

12. **PJM Interconnection** - Data Miner API
    https://dataminer2.pjm.com/

13. **U.S. Census Bureau** (via Our World in Data)
    https://ourworldindata.org/grapher/monthly-spending-data-center-us

14. **EIA** - Construction Cost Data
    https://www.eia.gov/electricity/generatorcosts/

### Papers Académicos

15. **Harvard / NSAPH** - Data Center Energy and Emissions
    https://arxiv.org/html/2411.09786v1

16. **WECC/NPCC** - Electricity Market Data
    https://figshare.com/articles/dataset/Economic_data_for_the_WECC_and_NPCC_electricity_markets/24116484

17. **IRENA** - Renewable Energy Statistics 2025
    https://www.irena.org/Publications/2025/Jul/Renewable-energy-statistics-2025

### Kaggle Datasets

18. **Global Data Centre Energy Footprints**
    https://www.kaggle.com/datasets/thedevastator/global-data-centre-energy-footprints

19. **Global AI Compute & Data Center Growth**
    https://www.kaggle.com/datasets/abdulmaliklodhra/global-ai-compute-and-data-center-growth-20002036

20. **Data Centre Warm Channel Temperature Prediction**
    https://www.kaggle.com/datasets/mbjunior/data-centre-hot-corridor-temperature-prediction

21. **Global Data Center Dataset**
    https://www.kaggle.com/datasets/rockyt07/data-center-dataset

### Vendors y Estándares de Industria

22. **Nlyte** - Data Center Rack Power Costs
    https://www.nlyte.com/blog/data-center-rack-power-costs-a-condensed-analysis/

23. **Uptime Institute** - Annual Data Center Survey
    https://uptimeinstitute.com/resources/research-and-reports

24. **ASHRAE** - Data Center Power Equipment Thermal Guidelines
    https://www.ashrae.org/technical-resources/bookstore/datacom-series

25. **TIA-942-B** - Telecommunications Infrastructure Standard
    https://tiaonline.org/

### Directorios y Bases de Datos

26. **Global Data Center Map**
    https://www.datacentermap.com/

27. **Baxtel** - Global Data Center Database
    https://baxtel.com/services/datasets

28. **Aterio** - US Data Center Locations
    https://www.aterio.io/datasets/lst_us_data_centers

### Open Source

29. **Data Center TCO Calculation Model**
    https://github.com/sfireworks/Data-center-TCO-calculation-model

30. **Apify** - EIA Energy Data Actor
    https://apify.com/ryanclinton/eia-energy-data

---

## Nota sobre los Datasets Generados

Los datasets de este proyecto son **sintéticos** generados a partir de los benchmarks y rangos reportados en las fuentes anteriores. No contienen datos reales de facilidades específicas, sino distribuciones estadísticas coherentes con la literatura de la industria.

| Dataset | Registros | Fuente Principal |
|---------|-----------|------------------|
| average_utilization_datacenter_100k.csv | 100,000 | Uptime Institute 2024 |
| utilization_range_datacenter_95k.csv | 95,000 | Uptime + AFCOM 2024 |
| benchmark_costo_por_mw_datacenter_25k.csv | 25,000 | CBRE, JLL, C&W 2024 |
| cooling_efficiency_datacenter_88k.csv | 88,000 | ASHRAE + Schneider 2023 |
| pue_datacenter_95k.csv | 95,000 | Uptime + NREL 2024 |
| costo_construccion_datacenter_100k.csv | 100,000 | Epoch AI, Thunder Said 2024 |

---

## Licencia

Este proyecto es de uso interno y demostración. Todos los derechos reservados.

---

## Contacto

Para preguntas o sugerencias, contactar al equipo de desarrollo.

---

*Versión 2.0 - S07-26-Team-33*
*Actualizado: 2026*
