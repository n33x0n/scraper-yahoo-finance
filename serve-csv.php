/* Strona .php podająca plik .csv (zabezpiecza przed “path traversal”) */
<?php
$baseDir = "/path/to/yahoo-finance-indexes";
$file = basename($_GET["file"]);
$fullPath = $baseDir . $file;

if (!file_exists($fullPath)) {
    die("nie ma");
}
header("content-type: text/csv");
header("content-length:" . filesize($fullPath));
ob_clean();
flush();
readfile($fullPath);

