<?php
/*
 * Serve Reports - Yahoo Finance Scraper
 * Copyright (C) 2025 Tomasz Lebioda <tlebioda@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * Skrypt PHP do serwowania raportów (zabezpiecza przed "path traversal")
 */

$baseDir = "/path/to/scraper-yahoo-finance/reports/";
$allowedTypes = ['html', 'txt', 'json'];

// Pobierz nazwę pliku z parametru GET
$file = isset($_GET['file']) ? $_GET['file'] : '';

if (empty($file)) {
    // Wyświetl listę dostępnych raportów
    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Raporty Yahoo Finance Scraper</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        a { color: #007bff; text-decoration: none; margin-right: 15px; }
        a:hover { text-decoration: underline; }
        .date { font-weight: bold; margin-bottom: 5px; }
        .formats { font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Raporty Yahoo Finance Scraper</h1>';
    
    $reports = [];
    $files = scandir($baseDir);
    
    foreach ($files as $filename) {
        if (preg_match('/report_(\d{4}-\d{2}-\d{2})\.html$/', $filename, $matches)) {
            $date = $matches[1];
            $reports[$date] = true;
        }
    }
    
    if (empty($reports)) {
        echo '<p>Brak dostępnych raportów.</p>';
    } else {
        echo '<ul>';
        krsort($reports); // Sortuj malejąco po dacie
        
        foreach ($reports as $date => $value) {
            echo '<li>';
            echo '<div class="date">📅 ' . $date . '</div>';
            echo '<div class="formats">';
            echo '<a href="?file=report_' . $date . '.html">📄 HTML</a>';
            echo '<a href="?file=report_' . $date . '.txt">📝 TXT</a>';
            echo '<a href="?file=report_' . $date . '.json">🔧 JSON</a>';
            echo '</div>';
            echo '</li>';
        }
        echo '</ul>';
    }
    
    echo '
        <p style="margin-top: 30px; text-align: center; color: #666; font-size: 0.9em;">
            Yahoo Finance Scraper v.1.5.0 | GNU GPL v3.0<br>
            © 2025 Tomasz Lebioda
        </p>
    </div>
</body>
</html>';
    exit;
}

// Zabezpieczenie przed path traversal
$file = basename($file);

// Sprawdź rozszerzenie pliku
$extension = strtolower(pathinfo($file, PATHINFO_EXTENSION));
if (!in_array($extension, $allowedTypes)) {
    http_response_code(403);
    die("Niedozwolony typ pliku");
}

// Sprawdź czy plik istnieje
$fullPath = $baseDir . $file;
if (!file_exists($fullPath)) {
    http_response_code(404);
    die("Plik nie istnieje");
}

// Ustaw odpowiedni Content-Type
switch ($extension) {
    case 'html':
        header('Content-Type: text/html; charset=utf-8');
        break;
    case 'txt':
        header('Content-Type: text/plain; charset=utf-8');
        break;
    case 'json':
        header('Content-Type: application/json; charset=utf-8');
        break;
}

// Wyślij plik
header('Content-Length: ' . filesize($fullPath));
ob_clean();
flush();
readfile($fullPath);
?>