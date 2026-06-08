"""
Script para popular o TTLCache com vários registros para testes manuais.
Roda a CLI com comandos pre-carregados via stdin.
"""
import sys
import subprocess
import random
import string

TOTAL = 20  # quantos registros criar

def random_key():
    return "key_" + "".join(random.choices(string.ascii_lowercase, k=4))

def main():
    random.seed(2026)

    # Gera comandos: mix de TTL longo, curto e sem TTL
    commands = []
    keys = []

    for i in range(TOTAL):
        key = random_key()
        value = f"val_{i}"
        ttl = random.choice([100, 300, 500, 2000, None])
        ttl_str = str(ttl) if ttl is not None else "none"
        commands.append(f"SET {key} {value} {ttl_str}")
        keys.append((key, ttl))

    commands.append("STATS")
    commands.append("GET " + keys[0][0])
    commands.append("GET " + keys[-1][0])
    commands.append("DELETE " + keys[2][0])
    commands.append("GET " + keys[2][0])
    commands.append("STATS")
    commands.append("PURGE")
    commands.append("STATS")
    commands.append("EXIT")

    print("=== COMANDOS GERADOS ===")
    for c in commands:
        print(f"  {c}")

    print(f"\n=== RODANDO CLI COM {TOTAL} REGISTROS ===")
    script = "\n".join(commands)
    proc = subprocess.run(
        [sys.executable, "cli.py"],
        input=script,
        capture_output=True,
        text=True,
        timeout=10,
    )
    print(proc.stdout)
    if proc.stderr:
        print("STDERR:", proc.stderr)


if __name__ == "__main__":
    main()
