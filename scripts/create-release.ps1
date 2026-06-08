$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path "release")) { New-Item -ItemType Directory -Path "release" | Out-Null }

$zipPath = Join-Path $root "release\project_release.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

$items = @(
    "apps", "magazin", "templates", "static", "scripts",
    "manage.py", "requirements.txt", "requirements-dev.txt",
    "Dockerfile", "docker-compose.yml", "docker-compose.prod.yml",
    ".env.example", ".env.production.example", ".env.demo.example",
    "README.md", "INSTALL.md", "DEPLOYMENT.md", "DEMO_GUIDE.md",
    "CHANGELOG.md", "RELEASE_NOTES.md", "SECURITY.md"
)

$existing = $items | Where-Object { Test-Path $_ }
Compress-Archive -Path $existing -DestinationPath $zipPath -Force

@"
Интернет-магазин канцтоваров — release v0.1.1
============================================

1. Установите Python 3.12
2. Запустите scripts\setup.bat
3. Запустите scripts\run.bat
4. Откройте http://127.0.0.1:8000/

Демо-аккаунты: см. release\demo_accounts.txt
"@ | Set-Content -Path "release\demo_readme.txt" -Encoding UTF8

@"
admin@shop.ru / demo1234 (Администратор)
manager@shop.ru / demo1234 (Менеджер)
warehouse@shop.ru / demo1234 (Кладовщик)
customer@shop.ru / demo1234 (Покупатель)
"@ | Set-Content -Path "release\demo_accounts.txt" -Encoding UTF8

Write-Host "Release archive created: $zipPath"
