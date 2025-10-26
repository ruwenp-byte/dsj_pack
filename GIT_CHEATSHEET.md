# 🧭 Git – Cheat Sheet für das MLOps-Projekt

Dieses Projekt nutzt Git, um alle Änderungen an Code, Docker-Dateien, Skripten und Konfigurationen nachzuvollziehen.  
Die folgenden Befehle helfen dir, dein Repository sauber zu verwalten.

---

## 🚀 Grundbefehle

| Aktion | Befehl | Erklärung |
|--------|---------|-----------|
| Repository initialisieren | `git init` | Erstellt ein neues lokales Git-Repo |
| Aktuellen Status prüfen | `git status` | Zeigt neue, geänderte, gelöschte Dateien |
| Änderungen anzeigen | `git diff` | Zeigt Unterschiede zu letzter Commit-Version |
| Dateien hinzufügen | `git add <datei>` | Eine Datei zur Staging-Area hinzufügen |
| **Alle Änderungen hinzufügen** | `git add .` | Alle neuen/geänderten Dateien (empfohlen) |
| **Alles im gesamten Repo hinzufügen** | `git add -A` | Fängt auch gelöschte Dateien ab |
| Änderungen committen | `git commit -m "Nachricht"` | Erstellt einen neuen Versions-Snapshot |
| Änderungen pushen | `git push` | Überträgt Commits an das Remote-Repo |
| Branch wechseln | `git switch <branch>` | Auf einen anderen Branch umschalten |
| Branch erstellen | `git switch -c <branch>` | Neuen Branch anlegen und wechseln |

---

## 🌍 Remote-Repository verbinden

```bash
git remote add origin https://github.com/<BENUTZER>/<REPO>.git
git branch -M main
git push -u origin main
```

> `origin` ist der Name des Remote-Repos, `main` der Standard-Branch.

---

## 🔄 Änderungen holen / mergen

| Aktion | Befehl | Beschreibung |
|---------|--------|--------------|
| Neueste Version holen | `git fetch` | Lädt Änderungen ohne Merge |
| Updaten (Merge) | `git pull` | Holt und integriert Änderungen |
| Branch zusammenführen | `git merge <branch>` | Merged Branch in aktuellen |
| Branch löschen | `git branch -d <branch>` | Lokalen Branch löschen |

---

## 🧹 Aufräumen & Rückgängig machen

| Situation | Befehl | Wirkung |
|------------|---------|---------|
| Datei aus Staging entfernen | `git restore --staged <datei>` | Entfernt aus Staging-Area |
| Datei auf letzte Version zurücksetzen | `git restore <datei>` | Überschreibt lokale Änderungen |
| Letzten Commit rückgängig (ohne Verlust) | `git reset --soft HEAD~1` | Commit bleibt lokal, nicht gepusht |
| Änderungen komplett verwerfen | `git reset --hard HEAD` | Alles zurück auf letzten Commit ⚠️ |

---

## 🧩 Nützliche Befehle für dieses Projekt

```bash
# Status prüfen
git status

# Alle Änderungen auf einmal committen
git add .
git commit -m "Update Compose, API und Trainer"

# Änderungen hochladen
git push

# Neue Version taggen (z. B. für Release)
git tag -a v1.0.0 -m "Stable MLOps Setup"
git push origin v1.0.0
```

---

## 💡 Tipps

- **Kleine Commits** sind besser als riesige Blöcke: z. B. „Add Trainer script“, „Fix Docker healthcheck“.  
- Nutze `.gitignore`, um Artefakte (`mlruns/`, `work/`, `n8n_data/`) draußen zu halten.  
- Bevor du Änderungen an `docker-compose.yml` pushst:  
  ```bash
  docker compose config
  ```  
  prüft, ob sie syntaktisch korrekt ist.  
- Für Teamarbeit: `git pull --rebase` verhindert unnötige Merge-Commits.

---
