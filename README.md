"""
Puzzle Solver Projekt
=====================

## Überblick

Das Puzzle Solver Projekt ist eine innovative Softwarelösung, die darauf abzielt, das klassische 15-Puzzle-Spiel (und seine Variationen) automatisch zu lösen. Es unterstützt verschiedene Puzzle-Größen und ermöglicht Puzzles mit Zahlen, Buchstaben oder einer Mischung aus beidem. Durch die Implementierung eines effizienten Algorithmus bietet diese Anwendung eine schnelle Lösung und wertvolle Einblicke in die Lösungsstrategie.

## Funktionen

- Unterstützung verschiedener Puzzle-Größen: Wählen Sie zwischen verschiedenen Puzzle-Größen, einschließlich der Standardgröße 4x4.
- Tile-Modi: Die Puzzles können aus Zahlen, Buchstaben oder einer Mischung von beiden bestehen.
- Duplikationsmodus: Erzeugen Sie Puzzles mit einzigartigen oder duplizierten Elementen.
- Visualisierung: Betrachten Sie die Puzzle-Lösung Schritt für Schritt in einer benutzerfreundlichen grafischen Schnittstelle.
- Effiziente Algorithmen: Nutzt Breadth-First Search (BFS) und weitere Optimierungen für eine schnelle Lösungsfindung.

## Installation

Vor der Installation stellen Sie sicher, dass Python 3.8 oder höher auf Ihrem System installiert ist.

1. Klonen Sie das Repository:

```bash
git clone https://github.com/IhrBenutzername/puzzle-solver.git
```

## Anwendung starten

Um das Programm zu starten, führen Sie main.py mit Python aus:

```bash
python main.py
```

Folgen Sie anschließend den Anweisungen im Programm, um Ihr Puzzle zu konfigurieren und die Lösung zu starten.

## Nutzung

1. Programmstart: Öffnen Sie main.py, um das Programm zu starten.
2. Puzzle-Parameter festlegen: Im Startfenster wählen Sie zuerst die Puzzle-Größe aus. Aufgrund der langen Berechnungszeit sind 3x4 und 4x4 Puzzles momentan deaktiviert.
3. Modus wählen: Bestimmen Sie den Puzzle-Modus. Sie haben die Wahl zwischen Zahlen, Buchstaben oder einer Mischung aus beiden.
4. Anzahl der Lösungen: Geben Sie ein, wie viele Puzzles gelöst werden sollen. Die maximale Anzahl ist 181440.
5. Duplikate: Entscheiden Sie sich für den Duplizierungsmodus. Puzzles können entweder ausschließlich einzigartige Elemente oder eine Kombination mit Duplikaten enthalten. Bei Auswahl von „DUPLICATED“, geben Sie die Anzahl der Duplikate an. Diese werden zufällig im Puzzle verteilt.
6. Start: Mit einem Klick auf „Submit“ beginnen Sie mit der Lösung. Korrekte Eingaben werden bestätigt und der Lösungsprozess startet.
7. Nach der Lösung: Ein Hinweisfenster informiert Sie über die Fertigstellung. Lösungen und detaillierte Daten dazu finden sich im Verzeichnis assets/solved_states, sortiert nach Datum und Uhrzeit des Lösungsstarts.
