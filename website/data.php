<?php
session_start();

$datafolder = "/home/user/work/awfy/website/data/";

include "internals.php";

function fault() {
	exit();
}

if (!isset($_GET["file"]))
	fault();

$name = $_GET["file"];
if (substr($name, 0, 4) == "auth")
	fault();
if (!preg_match("/^[a-zA-Z0-9-. _]*$/i", $name))
	fault();

$file = $datafolder.$name;
if (!file_exists($file)) {
	$file = $datafolder."auth-".$name;
	if (!file_exists($file))
		fault();
}

if (isset($_SERVER['HTTP_IF_MODIFIED_SINCE']) &&
    strtotime($_SERVER['HTTP_IF_MODIFIED_SINCE']) == filemtime($file))
{
    header('Last-Modified: '.gmdate('D, d M Y H:i:s', filemtime($file)).' GMT', true, 304);
} else {
    header('Last-Modified: '.gmdate('D, d M Y H:i:s', filemtime($file)).' GMT', true, 200);
    header('Content-Length: '.filesize($file));
	echo file_get_contents($file); 
}
