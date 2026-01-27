#!/usr/bin/env python3
"""DSL отчет для Homework #30"""

import json
import os
from datetime import datetime

# Собираем данные
data = {
    "homework": 30,
    "title": "Jenkins Pipeline with Docker",
    "build": os.getenv('BUILD_NUMBER', 'unknown'),
    "job": os.getenv('JOB_NAME', 'unknown'),
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "environment": os.getenv('ENVIRONMENT', 'dev'),
    "docker_operations": os.getenv('SKIP_DOCKER', 'false') == 'false',
    "pipeline_status": "completed",
    "requirements_met": 12
}

# Сохраняем в файл
os.makedirs('reports', exist_ok=True)
with open('reports/dsl_report.json', 'w') as f:
    json.dump(data, f, indent=2)

# Выводим результат
print(json.dumps({"status": "success", "report": "dsl_report.json"}, indent=2))