# Stranded Capacity Calculator

### Modelo de Estimación de Capacidad Atrapada en Data Centers de IA

**Stranded Capacity Calculator** es una herramienta desarrollada para una startup de infraestructura de IA que necesita medir un problema crítico de los data centers modernos: la capacidad pagada y encendida que no produce nada porque las capas físicas y operativas del facility no se coordinan entre sí.

La plataforma traduce 3 datos operativos del usuario en 5 métricas financieras y técnicas de alto valor, construidas sobre un dataset de referencia de fuentes públicas de la industria — dándole a un operador de data center un orden de magnitud confiable sobre su capacidad atrapada, sin necesidad de revelar información confidencial de su facility.

---

# 🚀 Problema y Solución

## 📉 El Problema

Los data centers de IA enfrentan un desperdicio financiero y energético masivo por:

- desacople entre la capa física (cooling, distribución de energía) y la capa operativa (orquestación de cargas de IA)
- capacidad pagada y encendida que no produce trabajo útil ("stranded capacity")
- falta de una forma estandarizada y auditable de estimar ese desperdicio
- ausencia de benchmarks de industria accesibles para comparar el propio facility

Esto provoca:

- pérdidas financieras anuales no cuantificadas
- decisiones de inversión en infraestructura sin datos de respaldo
- imposibilidad de priorizar qué optimizar primero

---

## 💡 Nuestra Solución

**Stranded Capacity Calculator** ofrece un modelo de rangos —no de precisión exacta— que le permite a un operador entender el orden de magnitud de su problema de forma honesta y auditable.

### 📦 Modelo de Estimación basado en Datos Públicos

El modelo recibe 3 inputs del operador (tamaño del facility en MW, utilización aproximada, tipo de cooling) y los combina con un dataset de referencia construido a partir de fuentes públicas verificables: Uptime Institute, Lawrence Berkeley National Lab, EIA (Annual Energy Outlook), y papers académicos.

### 🎯 Outputs Financieros y Técnicos

El sistema calcula:

- Stranded Capacity, en % y MW
- pérdida financiera anual estimada (rango en USD)
- valor recuperable potencial
- tiempo estimado de recuperación
- KPIs de industria: $/MW perdido, utilización vs. benchmark, capacidad efectiva vs. pagada

### 📊 Dashboard Interactivo

La plataforma incorpora un dashboard visual (Vista Ejecutiva y Análisis Avanzado) con comparativas por país, proyección de escenarios, análisis de sensibilidad y una matriz de oportunidades con ROI estimado por mejora.

### 🔍 Trazabilidad y Auditabilidad

Cada dato del dataset de referencia está documentado con su fuente, nivel de confianza, y —cuando corresponde— marcado explícitamente como supuesto del equipo.

---

# 🛠️ Stack Tecnológico

## Frontend / Dashboard

- **Streamlit** — Framework de Python para el dashboard interactivo
- **Plotly** — Visualización de gráficos interactivos

## Backend & Datos

- **Python (Pandas)** — Procesamiento y limpieza (ETL) del dataset de referencia
- **Jupyter Notebook** — Documentación reproducible del proceso de EDA/ETL
- **JSON** — Formato de almacenamiento del dataset de referencia

## Fuentes de Datos

- Uptime Institute Global Data Center Survey
- Lawrence Berkeley National Lab — Data Center Energy Reports
- EIA — Annual Energy Outlook (AEO2026)
- Datasets complementarios: Google Cluster Data, Azure Public Dataset, IEEE DataPort

---

# 📈 Logros del MVP

- ✅ Dataset de referencia consolidado a partir de fuentes públicas verificables
- ✅ Modelo de estimación funcional con lógica de rangos
- ✅ Dashboard interactivo desplegado (Vista Ejecutiva + Análisis Avanzado)
- ✅ Análisis de sensibilidad identificando las variables de mayor impacto
- ✅ Comparativa de benchmarks por país y tipo de facility

---

# 🌐 Enlaces del Proyecto

- [Repositorio del proyecto](https://github.com/No-Country-simulation/S07-26-Team-33)
- [Dashboard en vivo](https://s07-26-team-33-8dnryneg52zimeygftuqin.streamlit.app/)

---

# 👥 Equipo — S07-26-Team-33

| Integrante | Especialidad |
| --- | --- |
| Florencia Hidalgo | Data Analytics |
| Marvin Orozco | Data Science / Data Engineering |
| Luis Perez Ortiz | Data Science |
| Carolhay Carhuas | Ingeniería en Sistemas |
| Claudia Rivero | Data Science |

---

# 🎯 Visión

> *"Que ningún operador de data center tenga que adivinar cuánta capacidad está desperdiciando — solo medirla, con datos honestos y auditables."*