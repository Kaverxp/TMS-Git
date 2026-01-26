#!/usr/bin/env python3
import json
import sys
import os

def main():
    # Простой скрипт для демонстрации
    report = {
        "status": "success",
        "message": "Report generated for educational purposes",
        "build_info": {
            "number": os.getenv('BUILD_NUMBER', 'unknown'),
            "parameters": {
                "image_name": os.getenv('IMAGE_NAME', 'tms-app'),
                "port": os.getenv('HOST_PORT', '9090')
            }
        }
    }
    
    print(json.dumps(report, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()