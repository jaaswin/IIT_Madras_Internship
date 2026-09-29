<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>SecureVault</title>

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

.container {
    width: 380px;
    max-width: 92%;

    text-align: center;
}

.logo-icon {
    width: 48px;
    height: 48px;

    margin: 0 auto 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #2563eb;
    color: white;

    border-radius: 9px;

    font-size: 22px;
    font-weight: bold;
}

h1 {
    margin: 0 0 10px;

    font-size: 28px;
    font-weight: 600;
}

.description {
    margin: 0 auto 28px;

    color: #6b7280;

    font-size: 14px;

    line-height: 1.6;
}

.login-button {
    display: inline-block;

    padding: 11px 28px;

    background: #2563eb;

    color: white;

    text-decoration: none;

    border-radius: 6px;

    font-size: 14px;

    font-weight: 500;
}

.login-button:hover {
    background: #1d4ed8;
}

</style>

</head>

<body>


<div class="container">


    <div class="logo-icon">
        S
    </div>


    <h1>
        SecureVault
    </h1>


    <p class="description">
        Secure document management and file upload.
    </p>


    <a
        class="login-button"
        href="login.php"
    >
        Sign In
    </a>


</div>


</body>

</html>