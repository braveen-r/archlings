# 🐧 Archlings

> A "Rustlings-inspired" Arch Linux troubleshooting trainer that provides sandboxed, Docker-based labs for practicing system repairs, complete with automated verification and telemetry.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED.svg?style=flat-square&logo=docker&logoColor=white)
![Arch Linux](https://img.shields.io/badge/OS-Arch_Linux-1793D1.svg?style=flat-square&logo=arch-linux&logoColor=white)
![DuckDB](https://img.shields.io/badge/Database-DuckDB-FDED01.svg?style=flat-square&logo=duckduckgo&logoColor=black)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF.svg?style=flat-square&logo=github-actions&logoColor=white)

---

## 🎯 Overview

**Archlings** acts as a flight simulator for Linux system administration. When Arch Linux breaks, beginners often panic and copy-paste dangerous commands from forums. Archlings solves this by spinning up disposable, intentionally broken Linux containers. You diagnose the fault, repair the system, and run an automated verifier to confirm your fix—all without risking your actual operating system. 

---

## 💻 Development Environment

This project was natively developed and tested in the following environment:
- **Operating System:** Arch Linux (Wayland / Hyprland)
- **Terminal Environment:** `sunraku` (ZSH)
- **Containerization:** Docker Engine
- **Core Languages/Tools:** Python 3.14 (Typer, Rich), DuckDB, Bash Shell Scripting
- **CI/CD:** GitHub Actions

---

## 🚀 Installation

### Prerequisites
- **Python 3.10+**
- **Docker** (Ensure the Docker daemon is running: `sudo systemctl start docker`)
- **Git**

### Step-by-Step Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Braveen811/archlings.git](https://github.com/Braveen811/archlings.git)
   cd archlings

```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate

```


3. **Install the CLI tool in editable mode:**
```bash
pip install -e .

```



---

## 🎮 How to Run (Usage)

Archlings uses a **Two-Terminal Workflow**. Your host machine acts as the control engine, while the Docker container acts as your broken sandbox.

### 1. Start a Scenario

Open **Terminal 1** (your host machine, inside the `archlings` folder with the virtual environment activated) and run:

```bash
archlings start 01-keyring-broken

```

*Docker will build the sandbox, inject the fault, and drop you directly into a broken `root` shell.*

### 2. Get a Hint (Optional)

If you get stuck, open **Terminal 2** (on your host machine) and request a clue:

```bash
archlings hint 01-keyring-broken

```

### 3. Fix the System

Go back to **Terminal 1** (the root shell inside the container) and type the Linux commands needed to fix the problem (e.g., reinitializing the keyring or deleting a lock file).

### 4. Verify Your Fix

Once you think it's fixed, go to **Terminal 2** (host machine) and run:

```bash
archlings verify 01-keyring-broken

```

*If you fixed it correctly, you will get a success message. You can now type `exit` in Terminal 1 to close the sandbox.*

### 5. Check Your Leaderboard

Track your completion times and hint penalties:

```bash
archlings progress

```

---

## 🏗️ System Architecture

```text
[ Archlings CLI ] (Typer & Rich TUI)
        │
        ▼
[ Docker Runner ] (Spins up ephemeral Arch Linux sandbox)
        │
        ├──▶ [ setup.sh ] (Injects deliberate fault: e.g., stale lock, broken keyring)
        │
        ├──▶ [ User Sandbox ] (Learner repairs the system safely in root shell)
        │
        └──▶ [ verify.sh ] (Executes strict bash checks to confirm the fix)
        │
        ▼
[ Telemetry Engine ] (Logs completion time & hint usage to local DuckDB)

```

---

## 📂 Project Structure

```text
archlings/
├── archlings/
│   ├── cli/main.py          # Start, hint, verify, and progress commands
│   ├── runner/docker.py     # Docker container orchestrator
│   └── progress/db.py       # DuckDB schema and tracking logic
├── scenarios/
│   ├── 01-keyring-broken/   # Fault: Wiped GPG keyring
│   └── 02-stale-lock/       # Fault: Interrupted pacman db.lck
├── tests/
│   └── test_runner.sh       # Automated CI suite testing all scenarios
├── .github/workflows/       # GitHub Actions pipeline
└── README.md

```

---

## 🚀 Key Features

* **Safe Sandboxing:** All faults are injected into isolated Docker containers. Your host system is never touched, and you never run `--privileged`.
* **Automated Fix Verification:** Verifier scripts don't just check if the error disappeared; they actively test system capabilities (e.g., verifying `pacman` can fetch *new* un-cached packages) to prevent false positives.
* **Progress Telemetry:** An embedded **DuckDB** database tracks how long it takes you to solve a scenario and penalizes you for using hints.
* **Progressive Hints:** A YAML-driven hint system provides gradual clues to unblock learners without giving away the exact solution.
* **CI/CD Validated:** A custom bash test-runner executes automatically via GitHub Actions on every push, ensuring every scenario remains solvable against rolling Arch updates.

---

## 🛠️ System Tweaks & Troubleshooting

* **ModuleNotFoundError:** Ensure the CLI is installed in editable mode within a virtual environment using `pip install -e .` from the project root.
* **Command Not Found (Verify):** You cannot run `archlings verify` *inside* the broken Docker container. The container is a dumb sandbox. You must run the verify command on your host machine in a separate terminal tab.
* **Strict Verifier Constraints:** During testing, `pacman -Sy` would falsely pass signature verification checks. The verification engine was deliberately hardened to install uncached packages (`nano`), forcing a strict GPG signature evaluation.
* **Automated Markdown Extraction:** The CI pipeline automatically parses ````bash`blocks directly from`solution.md` files to test scenario validity, ensuring documentation and actual fixes never drift out of sync.

---

**Author:** [Braveen R](https://braveenr.linklee.in/)

---

## ✌️ Wrapping Up

You now have a fully functional, CI/CD-backed Linux training lab. Dive into the scenarios, break the system, and learn how to fix it the right way. 🚀 

See you in the terminal!