<?php
/*
 * Serve CSV - Yahoo Financial Market Dashboard
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
 * PHP page serving .csv file (protects against "path traversal")
 */
$baseDir = "/cytrus/256/tomaszlebioda.com/scraper-yahoo-finance/";
$file = basename($_GET["file"]);
$fullPath = $baseDir . $file;

if (!file_exists($fullPath)) {
    die("file not found");
}
header("Content-Type: text/csv");
header("Content-Length: " . filesize($fullPath));
ob_clean();
flush();
readfile($fullPath);
