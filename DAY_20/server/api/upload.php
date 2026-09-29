<?php

$uploadDir = "/var/www/html/uploads/";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    exit("Method not allowed.");
}

if (!isset($_FILES["file"])) {
    http_response_code(400);
    exit("No file was uploaded.");
}

$file = $_FILES["file"];

if ($file["error"] !== UPLOAD_ERR_OK) {
    http_response_code(400);
    exit("Upload failed.");
}

/*
 * INTENTIONAL LAB VULNERABILITY:
 * - No authentication/authorization check
 * - No file-extension allowlist
 * - Uploaded files are stored inside the web root
 */

$originalName = basename($file["name"]);
$extension = pathinfo($originalName, PATHINFO_EXTENSION);

if ($extension === "") {
    $extension = "bin";
}

$newName = uniqid("api_upload_", true) . "." . strtolower($extension);
$destination = $uploadDir . $newName;

if (!move_uploaded_file($file["tmp_name"], $destination)) {
    http_response_code(500);
    exit("Unable to save uploaded file.");
}

header("Content-Type: application/json");

echo json_encode([
    "status" => "success",
    "original_name" => $originalName,
    "stored_name" => $newName
]);
?>
