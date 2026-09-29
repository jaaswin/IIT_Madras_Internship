<?php

$secretFile = "/var/www/html/lab-secret.txt";

if (file_exists($secretFile)) {

    $secret = file_get_contents($secretFile);

    echo $secret;

} else {

    echo "LAB_SECRET_NOT_FOUND";

}

?>
