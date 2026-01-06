import subprocess

# Чтение IP из файла (по одному на строку)
with open("ip_list.txt", "r") as f:
    ip_list = [line.strip() for line in f if line.strip()]

# Проверяем и сохраняем результаты
with open("ping_results.txt", "w") as out:
    out.write("Результаты проверки IP-адресов:\n")
    out.write("=" * 40 + "\n")
    
    for ip in ip_list:
        # Выполняем ping
        result = subprocess.run(["ping", "-c", "2", "-W", "1", ip], 
                              capture_output=True)
        
        status = "ДОСТУПЕН" if result.returncode == 0 else "НЕДОСТУПЕН"
        line = f"{ip} — {status}\n"
        
        out.write(line)
        print(line.strip())

print("\nГотово! Проверено", len(ip_list), "IP-адресов.")