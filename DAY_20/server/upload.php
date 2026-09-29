<?php

session_start();

/*
 * SecureVault - intentionally vulnerable upload handler
 * -----------------------------------------------------
 * LAB PURPOSE:
 * Demonstrates unrestricted file upload where PHP files
 * can be stored inside the web-accessible uploads directory.
 */

if (!isset($_SESSION["logged_in"]) || $_SESSION["logged_in"] !== true) {

    header("Location: login.php");
    exit;

}

$uploadDir = __DIR__ . "/uploads/";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {

    http_response_code(405);
    exit("Method not allowed.");

}

if (!isset($_FILES["file"])) {

    exit("No file was selected.");

}

$file = $_FILES["file"];

if ($file["error"] !== UPLOAD_ERR_OK) {

    exit("File upload failed.");

}

$originalName = basename($file["name"]);

/*
 * INTENTIONAL LAB VULNERABILITY:
 *
 * There is no extension allowlist here.
 *
 * PHP files can therefore be stored in the web-accessible
 * uploads directory.
 */

$extension = pathinfo(
    $originalName,
    PATHINFO_EXTENSION
);

if ($extension === "") {

    $extension = "bin";

}

$newName = uniqid(
    "upload_",
    true
) . "." . strtolower($extension);

$destination = $uploadDir . $newName;

if (!move_uploaded_file(
    $file["tmp_name"],
    $destination
)) {

    exit("Unable to save the uploaded file.");

}

echo "<!DOCTYPE html>";

echo "<html>";

echo "<head>";

echo "<meta charset='UTF-8'>";

echo "<title>SecureVault | Upload Result</title>";

echo "<style>";

echo "body{font-family:Arial,Helvetica,sans-serif;background:#f5f7fa;margin:0;padding:60px;color:#1f2937;}";

echo ".card{max-width:650px;margin:auto;background:white;border:1px solid #e5e7eb;border-radius:10px;padding:30px;}";

echo "h2{margin-top:0;color:#166534;}";

echo ".info{background:#f9fafb;border:1px solid #e5e7eb;padding:15px;border-radius:6px;margin-top:20px;}";

echo "a{color:#2563eb;text-decoration:none;}";

echo "</style>";

echo "</head>";

echo "<body>";

echo "<div class='card'>";

echo "<h2>File uploaded successfully.</h2>";

echo "<div class='info'>";

echo "<p><strong>Original filename:</strong> "
    . htmlspecialchars($originalName)
    . "</p>";

echo "<p><strong>Stored filename:</strong> "
    . htmlspecialchars($newName)
    . "</p>";

echo "</div>";

echo "<p style='margin-top:25px;'>";

echo "<a href='dashboard.php'>Back to Dashboard</a>";

echo "</p>";

echo "</div>";

echo "</body>";

echo "</html>";

?>
