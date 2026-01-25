#!/usr/bin/env python3

import json
import sys
import os
import argparse
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.config = {
            'report_type': 'default',
            'period': datetime.now().strftime('%Y-%m'),
            'output_dir': './reports'
        }
    
    def configure(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        return self
    
    def generate(self):
        try:
            os.makedirs(self.config['output_dir'], exist_ok=True)
            
            data = self._get_data()
            summary = self._get_summary(data)
            
            report = {
                'config': self.config,
                'data': data,
                'summary': summary,
                'timestamp': datetime.now().isoformat()
            }
            
            filename = self._save(report)
            
            return {
                'success': True,
                'file': filename,
                'data': report
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_data(self):
        return [
            {"id": 1, "name": "Pipeline", "value": 100, "status": "done"},
            {"id": 2, "name": "Docker", "value": 200, "status": "done"},
            {"id": 3, "name": "Groovy", "value": 150, "status": "done"}
        ]
    
    def _get_summary(self, data):
        total = sum(item['value'] for item in data)
        return {
            'count': len(data),
            'total': total,
            'average': total / len(data) if data else 0
        }
    
    def _save(self, report):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{timestamp}.json"
        filepath = os.path.join(self.config['output_dir'], filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath

def main():
    parser = argparse.ArgumentParser(description='Генератор отчетов')
    parser.add_argument('--type', default='pipeline', help='Тип отчета')
    parser.add_argument('--period', help='Период')
    parser.add_argument('--output-dir', default='./reports', help='Папка для отчетов')
    
    args = parser.parse_args()
    
    generator = ReportGenerator()
    generator.configure(
        report_type=args.type,
        period=args.period or datetime.now().strftime('%Y-%m'),
        output_dir=args.output_dir
    )
    
    result = generator.generate()
    
    if result['success']:
        print(json.dumps(result, indent=2))
        sys.exit(0)
    else:
        print(f"Ошибка: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()