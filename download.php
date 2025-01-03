<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $link = $_POST['link'];
    $format = $_POST['format'];

    if (filter_var($link, FILTER_VALIDATE_URL)) {
        $output = shell_exec("youtube-dl -f $format -o 'downloads/%(title)s.%(ext)s' $link 2>&1");
        echo "<pre>$output</pre>";
    } else {
        echo "URL inválida.";
    }
} else {
    echo "Método de requisição inválido.";
}
?>