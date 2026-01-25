#!/usr/bin/env python3
"""
DSL для генерации отчётов из Jenkins Pipeline
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

class ReportGenerator:
    """DSL класс для генерации отчётов"""
    
    def __init__(self):
        self.config = {
            'report_type': 'default',
            'period': datetime.now().strftime('%Y-%m'),
            'filters': {},
            'output_dir': './reports',
            'format': 'json'
        }
    
    def configure(self, **kwargs) -> 'ReportGenerator':
        """Конфигурация отчёта через DSL"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
            else:
                print(f"⚠ Предупреждение: неизвестный параметр '{key}'")
        return self
    
    def add_filter(self, key: str, value: Any) -> 'ReportGenerator':
        """Добавление фильтра"""
        self.config['filters'][key] = value
        return self
    
    def generate(self) -> Dict[str, Any]:
        """Генерация отчёта"""
        try:
            # Создаём директорию для отчётов
            os.makedirs(self.config['output_dir'], exist_ok=True)
            
            # Имитация данных из БД
            report_data = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'pipeline_build': os.getenv('BUILD_NUMBER', 'unknown'),
                    'pipeline_id': os.getenv('BUILD_ID', 'unknown'),
                    'environment': os.getenv('ENVIRONMENT', 'dev')
                },
                'config': self.config,
                'data': self._fetch_data(),
                'summary': self._generate_summary()
            }
            
            # Сохранение отчёта
            filename = self._save_report(report_data)
            
            return {
                'success': True,
                'report_file': filename,
                'data': report_data,
                'message': f"Отчёт успешно сгенерирован: {filename}"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка генерации отчёта: {e}"
            }
    
    def _fetch_data(self) -> list:
        """Имитация получения данных из БД"""
        # В реальном проекте здесь будет запрос к БД
        return [
            {"id": 1, "name": "Проект А", "value": 150, "status": "active"},
            {"id": 2, "name": "Проект Б", "value": 230, "status": "completed"},
            {"id": 3, "name": "Проект В", "value": 75, "status": "pending"}
        ]
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Генерация сводки"""
        data = self._fetch_data()
        total = sum(item['value'] for item in data)
        
        return {
            'total_projects': len(data),
            'total_value': total,
            'average_value': total / len(data) if data else 0,
            'status_distribution': {
                'active': len([d for d in data if d['status'] == 'active']),
                'completed': len([d for d in data if d['status'] == 'completed']),
                'pending': len([d for d in data if d['status'] == 'pending'])
            }
        }
    
    def _save_report(self, report_data: Dict[str, Any]) -> str:
        """Сохранение отчёта в файл"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.config['report_type']}_report_{timestamp}"
        
        if self.config['format'] == 'json':
            filepath = os.path.join(self.config['output_dir'], f"{filename}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        elif self.config['format'] == 'html':
            filepath = os.path.join(self.config['output_dir'], f"{filename}.html")
            html = self._generate_html(report_data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
        
        else:
            filepath = os.path.join(self.config['output_dir'], f"{filename}.txt")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(report_data))
        
        return filepath
    
    def _generate_html(self, report_data: Dict[str, Any]) -> str:
        """Генерация HTML отчёта"""
        return f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Отчёт {self.config['report_type']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .success {{ color: green; font-weight: bold; }}
        .error {{ color: red; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Отчёт: {self.config['report_type'].upper()}</h1>
        <p>Сгенерирован: {report_data['metadata']['generated_at']}</p>
        <p>Сборка Jenkins: #{report_data['metadata']['pipeline_build']}</p>
        <p>Окружение: {report_data['metadata']['environment']}</p>
    </div>
    
    <div class="section">
        <h2>Конфигурация</h2>
        <pre>{json.dumps(self.config, indent=2, ensure_ascii=False)}</pre>
    </div>
    
    <div class="section">
        <h2>Данные</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Название</th>
                    <th>Значение</th>
                    <th>Статус</th>
                </tr>
            </thead>
            <tbody>
                {"".join([
                    f"<tr><td>{item['id']}</td><td>{item['name']}</td><td>{item['value']}</td><td>{item['status']}</td></tr>"
                    for item in report_data['data']
                ])}
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>Сводка</h2>
        <pre>{json.dumps(report_data['summary'], indent=2, ensure_ascii=False)}</pre>
    </div>
    
    <div class="section">
        <p class="success">✅ Отчёт успешно сгенерирован</p>
        <p>Файл сохранён в: {self._save_report.__name__}</p>
    </div>
</body>
</html>
"""

# Функция для использования в качестве модуля
def generate_report(**kwargs) -> Dict[str, Any]:
    """Фабричная функция для создания отчёта"""
    generator = ReportGenerator()
    generator.configure(**kwargs)
    return generator.generate()

# CLI интерфейс
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='DSL генератор отчётов')
    parser.add_argument('--type', default='default', help='Тип отчёта')
    parser.add_argument('--period', help='Период отчёта')
    parser.add_argument('--format', choices=['json', 'html', 'txt'], default='json', help='Формат вывода')
    parser.add_argument('--output-dir', default='./reports', help='Директория для отчётов')
    
    args = parser.parse_args()
    
    # Создание генератора
    generator = ReportGenerator()
    generator.configure(
        report_type=args.type,
        period=args.period,
        format=args.format,
        output_dir=args.output_dir
    )
    
    # Генерация отчёта
    result = generator.generate()
    
    # Вывод результата
    if result['success']:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)
    else:
        print(f"❌ Ошибка: {result['error']}")
        sys.exit(1)