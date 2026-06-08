# Build git-stages/stage-NN folders from the current project (run once after code changes).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$StagesRoot = Join-Path $Root "git-stages"
$ScreenshotGuide = Get-ChildItem -Path (Join-Path $Root "screenshots") -Filter "*.md" |
    Where-Object { $_.Name -ne "README_SCREENSHOTS.md" } |
    Select-Object -First 1

$StageFiles = @{
    "stage-01" = @(
        "README.md", "INSTALL.md", ".env.example", ".gitignore",
        "manage.py", "requirements.txt",
        "magazin/wsgi.py", "magazin/settings.py", "magazin/urls.py", "magazin/health.py", "magazin/asgi.py",
        "apps/users/backends.py", "apps/users/admin.py", "apps/users/forms.py", "apps/users/views.py",
        "apps/catalog/admin.py", "apps/cart/admin.py", "apps/orders/admin.py", "apps/orders/views.py",
        "apps/processing/views.py", "apps/admin_panel/views.py", "apps/admin_panel/urls.py",
        "magazin/reports/views.py", "magazin/reports/urls.py", "magazin/reports/apps.py",
        "apps/catalog/management/commands/load_demo_data.py",
        "logs/.gitkeep"
    )
    "stage-02" = @(
        "Makefile", "Dockerfile", "docker-compose.yml", ".dockerignore", ".editorconfig",
        "pyproject.toml", "requirements-dev.txt",
        "scripts/setup.bat", "scripts/run.bat", "scripts/check.bat", "scripts/format.bat",
        "scripts/docker-up.bat", "scripts/docker-down.bat", "scripts/logs.bat"
    )
    "stage-03" = @(
        "DEPLOYMENT.md", "DEMO_GUIDE.md", "public_url.txt",
        "docker-compose.prod.yml", ".env.production.example", ".env.demo.example",
        "scripts/deploy.bat", "scripts/restart.bat", "scripts/check_deploy.bat",
        "scripts/build_release.bat", "scripts/create-release.ps1"
    )
    "stage-04" = @(
        "docs/TEST_PLAN.md", "docs/DEFECT_LOG.md", "docs/RISK_REGISTER.md", "docs/API_TEST_REPORT.md",
        "scripts/test.bat", "scripts/api-test.bat", "scripts/quality-check.bat",
        "scripts/performance.bat", "scripts/logs-check.bat",
        "screenshots/README_SCREENSHOTS.md"
    )
    "stage-05" = @(
        "SECURITY.md",
        "docs/SECURITY_CHECKLIST.md", "docs/BACKUP_RESTORE_REPORT.md", "docs/RECOMMENDATIONS.md",
        "scripts/security-check.bat", "scripts/deps-check.bat", "scripts/backup.bat",
        "scripts/restore.bat", "scripts/ports-check.bat"
    )
    "stage-06" = @(
        ".github/workflows/ci.yml", "CHANGELOG.md", "RELEASE_NOTES.md",
        "docs/INCIDENT_REPORT.md", "docs/github_issue_template.md", "docs/RELEASE_CHECKLIST.md",
        "scripts/release-check.bat"
    )
}

function Copy-ProjectPath($RelativePath, $DestRoot) {
    $Src = Join-Path $Root $RelativePath
    $Dst = Join-Path $DestRoot $RelativePath
    if (-not (Test-Path $Src)) {
        if ($RelativePath -match "migrations|templates|tests|apps/") {
            return
        }
        Write-Warning "Skip (missing): $RelativePath"
        return
    }
    $DstDir = Split-Path $Dst -Parent
    if (-not (Test-Path $DstDir)) { New-Item -ItemType Directory -Path $DstDir -Force | Out-Null }
    if (Test-Path $Src -PathType Container) {
        Copy-Item $Src $DstDir -Recurse -Force
    } else {
        Copy-Item $Src $Dst -Force
    }
}

foreach ($stage in $StageFiles.Keys | Sort-Object) {
    $Dest = Join-Path $StagesRoot $stage
    $CommitBackup = $null
    $CommitPath = Join-Path $Dest "COMMIT.txt"
    if (Test-Path $CommitPath) {
        $CommitBackup = Get-Content $CommitPath -Raw
    }

    if (Test-Path $Dest) { Remove-Item $Dest -Recurse -Force }
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null

    if ($CommitBackup) {
        Set-Content -Path $CommitPath -Value $CommitBackup -NoNewline
    }

    foreach ($item in $StageFiles[$stage]) {
        Copy-ProjectPath $item $Dest
    }

    if ($stage -eq "stage-01") {
        foreach ($dir in @("templates", "apps/users/migrations", "apps/catalog/migrations",
            "apps/cart/migrations", "apps/orders/migrations",
            "apps/catalog/management", "static/css")) {
            $s = Join-Path $Root $dir
            if (Test-Path $s) {
                $d = Join-Path $Dest $dir
                $parent = Split-Path $d -Parent
                if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
                Copy-Item $s (Split-Path $d -Parent) -Recurse -Force
            }
        }
        Get-ChildItem $Root/apps -Recurse -Include *.py | Where-Object {
            $_.FullName -notmatch "migrations|management|admin_panel|__pycache__"
        } | ForEach-Object {
            $rel = $_.FullName.Substring($Root.Length + 1)
            Copy-ProjectPath $rel $Dest
        }
        Get-ChildItem $Root/magazin -Recurse -Include *.py | Where-Object {
            $_.FullName -notmatch "reports|__pycache__"
        } | ForEach-Object {
            $rel = $_.FullName.Substring($Root.Length + 1)
            if ($rel -notin @("magazin/settings.py","magazin/urls.py","magazin/wsgi.py","magazin/health.py","magazin/asgi.py")) {
                Copy-ProjectPath $rel $Dest
            }
        }
    }

    if ($stage -eq "stage-04") {
        if (Test-Path "$Root/tests") {
            Copy-Item "$Root/tests" $Dest -Recurse -Force
        }
        New-Item -ItemType Directory -Path (Join-Path $Dest "reports") -Force | Out-Null
        ".gitkeep" | Set-Content (Join-Path $Dest "reports/.gitkeep")
        if ($ScreenshotGuide) {
            $relShot = $ScreenshotGuide.FullName.Substring($Root.Length + 1)
            Copy-ProjectPath $relShot $Dest
        }
    }

    Write-Host "OK: $stage"
}

Write-Host ""
Write-Host "Done: $StagesRoot"
