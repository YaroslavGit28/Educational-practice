"""Entrypoint для Docker: migrate, demo-данные, затем запуск сервера."""
import os
import subprocess
import sys


def main():
    subprocess.check_call([sys.executable, "manage.py", "migrate", "--noinput"])
    subprocess.check_call([sys.executable, "manage.py", "load_demo_data"])
    os.execvp(sys.executable, [sys.executable, *sys.argv[1:]])


if __name__ == "__main__":
    main()
