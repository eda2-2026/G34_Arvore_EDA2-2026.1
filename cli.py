# cli.py
"""
Interactive command-line interface for the TTLCache system.

Commands:
  SET <key> <value> <ttl_ms>  Insert/update a key-value pair with TTL
  GET <key>                   Retrieve a value by key
  DELETE <key>                Remove a key
  PURGE                       Remove all expired entries
  STATS                       Display usage statistics
  EXIT                        Quit the program
"""
import sys
from cache import TTLCache


def main():
    cache = TTLCache()

    while True:
        try:
            line = input().strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not line:
            continue

        parts = line.split()
        command = parts[0].upper() if parts else ""

        if command == "EXIT":
            break
        elif command == "SET":
            if len(parts) < 4:
                print("Usage: SET <key> <value> <ttl_ms>")
                continue
            key = parts[1]
            value = parts[2]
            raw_ttl = parts[3].lower()
            if raw_ttl in ("none", "-", "inf"):
                ttl_ms = None
            else:
                try:
                    ttl_ms = int(raw_ttl)
                except ValueError:
                    print("Usage: SET <key> <value> <ttl_ms>")
                    continue
            cache.set(key, value, ttl_ms)
            print("OK")
        elif command == "GET":
            if len(parts) < 2:
                print("Usage: GET <key>")
                continue
            key = parts[1]
            result = cache.get(key)
            if result is None:
                print("MISS")
            else:
                print(result)
        elif command == "DELETE":
            if len(parts) < 2:
                print("Usage: DELETE <key>")
                continue
            key = parts[1]
            success = cache.delete(key)
            if success:
                print("OK")
            else:
                print("MISS")
        elif command == "PURGE":
            removed = cache.purge()
            print(f"Removed {removed} expired entries")
        elif command == "STATS":
            stats = cache.get_stats()
            print(f"Live entries: {stats['live_entries']}")
            print(f"TTL misses: {stats['ttl_misses']}")
            print(f"Total ops: {stats['total_ops']}")
        else:
            print(f"Unknown command: {parts[0]}")


if __name__ == "__main__":
    main()
