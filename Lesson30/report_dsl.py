#!/usr/bin/env python3
"""
DSL для генерации отчётов из Jenkins Pipeline
"""

import json
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, Any, List

class ReportGenerator:
    """DSL класс для генерации отчётов"""
    
    def __init__(self):
        self.config = {
            'report_type': 'default',
            'period': datetime.now().strftime('%Y-%m'),
            'filters': {},
            'output_dir': './generated_reports',
            'format': 'json'
        }
    
    def configure(self, **kwargs) -> 'ReportGenerator':
        """Конфигурация отчёта через DSL"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
            elif key == 'filter':
                # Обработка фильтров в формате key=value
                if isinstance(value, list):
                    for filter_item in value:
                        if '=' in filter_item:
                            k, v = filter_item.split('=', 1)
                            self.config['filters'][k] = v
                elif '=' in value:
                    k, v = value.split('=', 1)
                    self.config['filters'][k] = v
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
                    'environment': os.getenv('ENVIRONMENT', 'dev'),
                    'job_name': os.getenv('JOB_NAME', 'unknown')
                },
                'config': self.config,
                'data': self._fetch_data(),
                'summary': self._generate_summary(),
                'pipeline_status': 'success',
                'docker_info': self._get_docker_info()
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
        # Всегда возвращаем тестовые данные
        return [
            {"id": 1, "name": "Jenkins Pipeline Lesson 30", "value": 100, "status": "completed", "environment": "dev", "tags": ["jenkins", "pipeline", "lesson30"]},
            {"id": 2, "name": "Docker Deployment", "value": 200, "status": "active", "environment": "dev", "tags": ["docker", "deployment"]},
            {"id": 3, "name": "Groovy Script", "value": 150, "status": "active", "environment": "dev", "tags": ["groovy", "automation"]},
            {"id": 4, "name": "DSL Report Generator", "value": 180, "status": "completed", "environment": "dev", "tags": ["dsl", "report", "python"]},
            {"id": 5, "name": "TMS Application", "value": 250, "status": "active", "environment": "dev", "tags": ["web", "application"]},
            {"id": 6, "name": "Build Automation", "value": 120, "status": "pending", "environment": "test", "tags": ["automation", "ci/cd"]},
            {"id": 7, "name": "Production Deployment", "value": 300, "status": "completed", "environment": "prod", "tags": ["production", "deployment"]}
        ]
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Генерация сводки"""
        data = self._fetch_data()
        total = sum(item['value'] for item in data)
        
        return {
            'total_items': len(data),
            'total_value': total,
            'average_value': total / len(data) if data else 0,
            'status_distribution': {
                'active': len([d for d in data if d['status'] == 'active']),
                'completed': len([d for d in data if d['status'] == 'completed']),
                'pending': len([d for d in data if d['status'] == 'pending'])
            },
            'environment_distribution': {
                'dev': len([d for d in data if d.get('environment') == 'dev']),
                'test': len([d for d in data if d.get('environment') == 'test']),
                'prod': len([d for d in data if d.get('environment') == 'prod'])
            }
        }
    
    def _get_docker_info(self) -> Dict[str, Any]:
        """Получение информации о Docker"""
        try:
            import subprocess
            result = subprocess.run(
                ['docker', 'info', '--format', '{{json .}}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass
        return {'available': False, 'message': 'Docker info not available'}
    
    def _save_report(self, report_data: Dict[str, Any]) -> str:
        """Сохранение отчёта в файл"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_type = self.config['report_type'].replace(' ', '_')
        filename = f"{report_type}_report_{timestamp}"
        
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
                f.write(json.dumps(report_data, indent=2, ensure_ascii=False))
        
        return filepath
    
    def _generate_html(self, report_data: Dict[str, Any]) -> str:
        """Генерация HTML отчёта"""
        config = self.config
        
        # Генерация таблицы данных
        data_rows = ""
        for item in report_data['data']:
            data_rows += f"""
                <tr>
                    <td>{item['id']}</td>
                    <td>{item['name']}</td>
                    <td>{item['value']}</td>
                    <td><span class="badge badge-{item['status']}">{item['status']}</span></td>
                    <td>{item.get('environment', 'N/A')}</td>
                </tr>
            """
        
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Отчёт {config['report_type']} - Jenkins Pipeline</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header p {{ margin: 5px 0 0; opacity: 0.9; }}
        .section {{ margin: 25px 0; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background: #fafafa; }}
        .section h2 {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-top: 0; }}
        .success {{ color: #28a745; font-weight: bold; }}
        .warning {{ color: #ffc107; font-weight: bold; }}
        .error {{ color: #dc3545; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; font-weight: 600; color: #495057; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .badge {{ padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
        .badge-active {{ background: #d4edda; color: #155724; }}
        .badge-completed {{ background: #d1ecf1; color: #0c5460; }}
        .badge-pending {{ background: #fff3cd; color: #856404; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        .filters {{ background: #e8f4fd; padding: 15px; border-radius: 6px; margin: 15px 0; }}
        pre {{ background: #f8f9fa; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 14px; }}
        .footer {{ margin-top: 30px; text-align: center; color: #666; font-size: 14px; padding-top: 20px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Отчёт Jenkins Pipeline</h1>
            <p>Тип: {config['report_type'].upper()} | Период: {config['period']} | Формат: {config['format'].upper()}</p>
            <p>Сгенерирован: {report_data['metadata']['generated_at']} | Сборка: #{report_data['metadata']['pipeline_build']}</p>
        </div>
        
        <div class="section">
            <h2>Конфигурация отчёта</h2>
            <div class="filters">
                <strong>Применённые фильтры:</strong>
                {', '.join([f'{k}={v}' for k, v in config['filters'].items()]) if config['filters'] else 'Нет фильтров'}
            </div>
            <pre>{json.dumps(config, indent=2, ensure_ascii=False)}</pre>
        </div>
        
        <div class="section">
            <h2>Статистика</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{report_data['summary']['total_items']}</div>
                    <div class="stat-label">Всего записей</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{report_data['summary']['total_value']}</div>
                    <div class="stat-label">Общая сумма</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{report_data['summary']['average_value']:.1f}</div>
                    <div class="stat-label">Среднее значение</div>
                </div>
            </div>
            
            <h3>Распределение по статусам</h3>
            <pre>{json.dumps(report_data['summary']['status_distribution'], indent=2, ensure_ascii=False)}</pre>
            
            <h3>Распределение по окружениям</h3>
            <pre>{json.dumps(report_data['summary']['environment_distribution'], indent=2, ensure_ascii=False)}</pre>
        </div>
        
        <div class="section">
            <h2>Данные отчёта</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Название</th>
                        <th>Значение</th>
                        <th>Статус</th>
                        <th>Окружение</th>
                    </tr>
                </thead>
                <tbody>
                    {data_rows}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>Метаданные</h2>
            <pre>{json.dumps(report_data['metadata'], indent=2, ensure_ascii=False)}</pre>
        </div>
        
        <div class="section">
            <p class="success">✅ Отчёт успешно сгенерирован</p>
            <p>Файл сохранён в директории: {config['output_dir']}/</p>
            <p>Время генерации: {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
        
        <div class="footer">
            <p>Отчёт сгенерирован автоматически Jenkins Pipeline | Задание №30 | TMS Project</p>
        </div>
    </div>
</body>
</html>"""

# CLI интерфейс
def main():
    parser = argparse.ArgumentParser(description='DSL генератор отчётов для Jenkins Pipeline')
    parser.add_argument('--type', default='jenkins_pipeline', help='Тип отчёта (default: jenkins_pipeline)')
    parser.add_argument('--period', help='Период отчёта (default: текущий месяц)')
    parser.add_argument('--format', choices=['json', 'html', 'txt'], default='json', help='Формат вывода')
    parser.add_argument('--output-dir', default='./generated_reports', help='Директория для отчётов')
    parser.add_argument('--filter', action='append', help='Фильтры в формате key=value')
    
    args = parser.parse_args()
    
    try:
        # Создание генератора
        generator = ReportGenerator()
        
        # Настройка из аргументов
        config_kwargs = {
            'report_type': args.type,
            'format': args.format,
            'output_dir': args.output_dir
        }
        
        if args.period:
            config_kwargs['period'] = args.period
        
        if args.filter:
            config_kwargs['filter'] = args.filter
        
        generator.configure(**config_kwargs)
        
        # Генерация отчёта
        result = generator.generate()
        
        # Вывод результата
        if result['success']:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(0)
        else:
            print(f"❌ Ошибка: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()