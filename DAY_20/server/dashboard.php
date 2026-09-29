<?php

session_start();

/*
 * Authentication check
 *
 * Only users who successfully logged in through login.php
 * can access this dashboard.
 */

if (!isset($_SESSION["logged_in"]) || $_SESSION["logged_in"] !== true) {

    header("Location: login.php");
    exit;

}

$username = $_SESSION["username"] ?? "user";

?>

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>SecureVault | Dashboard</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family: Arial, Helvetica, sans-serif;

    background: #f5f7fa;

    color: #1f2937;

}

/* Navigation */

.navbar {

    height: 64px;

    background: #ffffff;

    border-bottom: 1px solid #e5e7eb;

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 0 40px;

}

.brand {

    display: flex;

    align-items: center;

    gap: 10px;

    font-size: 19px;

    font-weight: 600;

}

.brand-icon {

    width: 34px;

    height: 34px;

    background: #2563eb;

    color: white;

    border-radius: 7px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-weight: bold;

}

.user-area {

    display: flex;

    align-items: center;

    gap: 15px;

    font-size: 14px;

    color: #6b7280;

}

.logout {

    text-decoration: none;

    color: #2563eb;

    font-weight: 500;

}

/* Main */

.container {

    max-width: 1000px;

    margin: 50px auto;

    padding: 0 25px;

}

.header {

    margin-bottom: 30px;

}

.header h1 {

    margin: 0 0 8px;

    font-size: 28px;

}

.header p {

    margin: 0;

    color: #6b7280;

}

/* Cards */

.card {

    background: #ffffff;

    border: 1px solid #e5e7eb;

    border-radius: 10px;

    padding: 28px;

    margin-bottom: 25px;

}

.card h2 {

    margin: 0 0 8px;

    font-size: 20px;

}

.card-description {

    margin: 0 0 25px;

    color: #6b7280;

    font-size: 14px;

}

/* Upload */

.file-input {

    display: block;

    width: 100%;

    padding: 12px;

    border: 1px solid #d1d5db;

    border-radius: 6px;

    margin-bottom: 18px;

    background: #ffffff;

}

.upload-button {

    border: none;

    border-radius: 6px;

    background: #2563eb;

    color: white;

    padding: 11px 20px;

    font-size: 14px;

    cursor: pointer;

}

.upload-button:hover {

    background: #1d4ed8;

}

/* Information */

.info {

    background: #f9fafb;

    border: 1px solid #e5e7eb;

    border-radius: 7px;

    padding: 15px;

    font-size: 14px;

    color: #4b5563;

}

</style>

</head>

<body>

<nav class="navbar">

    <div class="brand">

        <div class="brand-icon">
            S
        </div>

        <span>
            SecureVault
        </span>

    </div>

    <div class="user-area">

        <span>
            Signed in as:
            <strong>
                <?php echo htmlspecialchars($username); ?>
            </strong>
        </span>

        <a
            class="logout"
            href="login.php"
        >
            Logout
        </a>

    </div>

</nav>


<main class="container">

    <div class="header">

        <h1>
            File Dashboard
        </h1>

        <p>
            Upload and manage your files.
        </p>

    </div>


    <div class="card">

        <h2>
            Upload File
        </h2>

        <p class="card-description">
            Upload your document securely.
        </p>


        <form
            action="upload.php"
            method="POST"
            enctype="multipart/form-data"
        >

            <input
                class="file-input"
                type="file"
                name="file"
                required
            >

            <button
                class="upload-button"
                type="submit"
            >
                Upload File
            </button>

        </form>

    </div>


    <div class="card">

        <h2>
            Account Information
        </h2>

        <p class="card-description">
            Current authenticated account.
        </p>

        <div class="info">

            Username:
            <strong>
                <?php echo htmlspecialchars($username); ?>
            </strong>

        </div>

    </div>

</main>

</body>

</html>
