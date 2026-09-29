<?php

$result = "";
$statusClass = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $host = trim($_POST["host"] ?? "");

    if ($host === "") {

        $result = "Please enter a hostname.";
        $statusClass = "error";

    } else {

        /*
         * Normal server-status functionality.
         *
         * The application checks whether the supplied
         * hostname accepts a TCP connection on port 80.
         */

        $connection = @fsockopen(
            $host,
            80,
            $errno,
            $errstr,
            3
        );

        if ($connection) {

            fclose($connection);

            $safeHost = htmlspecialchars(
                $host,
                ENT_QUOTES,
                "UTF-8"
            );

            $result = "Server '$safeHost' is reachable.";
            $statusClass = "success";

        } else {

            $safeHost = htmlspecialchars(
                $host,
                ENT_QUOTES,
                "UTF-8"
            );

            $result = "Server '$safeHost' is not reachable.";
            $statusClass = "error";

        }

    }
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

<title>SecureVault | Server Status</title>


<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #f5f7fa;

    color: #1f2937;

}


.container {

    width: 500px;

    max-width: 92%;

    margin: 100px auto;

}


.card {

    background: #ffffff;

    border: 1px solid #e5e7eb;

    border-radius: 10px;

    padding: 30px;

    box-shadow:
        0 5px 20px
        rgba(0, 0, 0, 0.04);

}


.logo {

    width: 40px;

    height: 40px;

    display: flex;

    align-items: center;

    justify-content: center;

    margin-bottom: 18px;

    background: #2563eb;

    color: white;

    border-radius: 8px;

    font-weight: bold;

}


h1 {

    margin: 0 0 8px;

    font-size: 24px;

    font-weight: 600;

}


.description {

    margin: 0 0 25px;

    color: #6b7280;

    font-size: 14px;

    line-height: 1.5;

}


label {

    display: block;

    margin-bottom: 7px;

    font-size: 14px;

    font-weight: 500;

}


input {

    width: 100%;

    padding: 11px 12px;

    border: 1px solid #d1d5db;

    border-radius: 6px;

    font-size: 14px;

    outline: none;

}


input:focus {

    border-color: #2563eb;

}


button {

    width: 100%;

    margin-top: 18px;

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


.result {

    margin-top: 22px;

    padding: 13px;

    border-radius: 6px;

    font-size: 14px;

}


.success {

    background: #ecfdf5;

    color: #166534;

    border: 1px solid #bbf7d0;

}


.error {

    background: #fef2f2;

    color: #991b1b;

    border: 1px solid #fecaca;

}

</style>

</head>


<body>


<div class="container">


    <div class="card">


        <div class="logo">
            S
        </div>


        <h1>
            Server Status
        </h1>


        <p class="description">
            Check whether a server is reachable.
        </p>


        <form method="POST">


            <label for="host">
                Server hostname
            </label>


            <input
                id="host"
                type="text"
                name="host"
                placeholder="Enter hostname"
                required
            >


            <button type="submit">
                Check Status
            </button>


        </form>


        <?php if ($result !== ""): ?>


            <div class="result <?php echo $statusClass; ?>">

                <?php echo $result; ?>

            </div>


        <?php endif; ?>


    </div>


</div>


</body>

</html>