# Informationen zur Verwendung der Daten und Programme

## Rohdaten

Die Rohdaten befinden sich im Ordner `/Rohdaten`. Für jeden Körper und die Kalibrierung gibt es einen Ordner, in dem sich mehrere CSV-Dateien befinden. Diese Dateien enthalten jeweils in der ersten Spalte die vergangene Zeit seit Messbeginn in µs (nur zum Teil bei 0 beginnend) und in den darauffolgenden Spalten die Beschleunigung als Vielfaches der Erdbeschleunigung g = 9,80665 in x-, y- und z-Richtung.

Bei allen Messungen ist die z-Achse parallel zur Fallrichtung.

## Programm zum Messen der Daten

Die Messung der Daten wird mit zwei Python-Skripten durchgeführt. Das Skript `server.py` wird auf dem Raspberry Pi ausgeführt. Es stellt eine REST-API auf Port 80 zur Verfügung, die vom Programm `client.py` genutzt wird, um rudimentäre Diagramme zu erstellen. Letzteres Skript läuft i.d.R. auf einem anderen Computer, der sich in demselben Netzwerk wie der Raspberry Pi befindet (z.B., indem die beiden mit einem Ethernet-Kabel verbunden und entsprechend konfiguriert werden).

## Programm zum Finden des c_w-Wertes mit den geringsten quadratischen Abweichungen

`best-fit.py` findet für gegebenen Messwerte und Eigenschaften eines Körpers den c_w-Wert mit den geringsten quadratischen Abweichungen.

## Programm zum Konvertieren von CSV-Dateien

`convert-csv.py` konvertiert eine CSV-Datei, in der als Dezimaltrennzeichen ein Komma verwendet wird und daher alle Zahlen in Anführungszeichen stehen, zu einer CSV-Datei mit englischem Zahlenformat.

## 3D-Modell der Messapparatur

Die Datei `Messapparatur.stl` enthält ein 3D-Modell der Messapparatur. STL-Dateien können z.B. mit Blender geöffnet werden.
