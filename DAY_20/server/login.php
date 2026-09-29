<?php

session_start();

$message = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $username = $_POST["username"] ?? "";
    $password = $_POST["password"] ?? "";

    if ($username === "user" && $password === "password123") {

        $_SESSION["logged_in"] = true;
        $_SESSION["username"] = $username;

        header("Location: dashboard.php");
        exit;
    }

    $message = "Invalid username or password.";
}

?>

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>SecureVault | Login</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f5f7fa;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #1f2937;
}

.login-container {
    width: 380px;
    max-width: 92%;
}

.logo {
    text-align: center;
    margin-bottom: 25px;
}

.logo-icon {
    width: 42px;
    height: 42px;
    margin: 0 auto 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #2563eb;
    color: white;
    border-radius: 8px;
    font-size: 20px;
    font-weight: bold;
}

.logo h1 {
    margin: 0;
    font-size: 22px;
    font-weight: 600;
}

.login-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.04);
}

.login-card h2 {
    margin: 0 0 6px;
    font-size: 20px;
}

.login-card p {
    margin: 0 0 25px;
    color: #6b7280;
    font-size: 14px;
}

.error {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
    border-radius: 6px;
    padding: 9px;
    margin-bottom: 18px;
    font-size: 13px;
}

label {
    display: block;
    margin-bottom: 7px;
    font-size: 13px;
    font-weight: 500;
}

input {
    width: 100%;
    padding: 11px;
    margin-bottom: 18px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
}

input:focus {
    outline: none;
    border-color: #2563eb;
}

button {
    width: 100%;
    padding: 11px;
    border: none;
    border-radius: 6px;
    background: #2563eb;
    color: white;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}

</style>

</head>

<body>

<div class="login-container">

    <div class="logo">

        <div class="logo-icon">
            S
        </div>

        <h1>
            SecureVault
        </h1>

    </div>

    <div class="login-card">

        <h2>
            Sign in
        </h2>

        <p>
            Enter your credentials to continue.
        </p>

        <?php if ($message !== ""): ?>

            <div class="error">
                <?php echo htmlspecialchars($message); ?>
            </div>

        <?php endif; ?>

        <form method="POST">

            <label for="username">
                Username
            </label>

            <input
                id="username"
                type="text"
                name="username"
                placeholder="Enter username"
                required
            >

            <label for="password">
                Password
            </label>

            <input
                id="password"
                type="password"
                name="password"
                placeholder="Enter password"
                required
            >

            <button type="submit">
                Sign In
            </button>

        </form>

    </div>

</div>

</body>

</html>
