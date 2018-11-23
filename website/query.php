<?php
session_start();

require_once("internals.php");

init_database();

function fault() {
	exit();
}

if (isset($_GET["git_rev"]) && isset($_GET["vendor"])) {
  $rev = $_GET["git_rev"];
  $vendor = $_GET["vendor"];
  $dir = "";

  if ($vendor == "V8") {
    $dir = "/home/user/work/repos/v8";
  }
  else if ($vendor == "JerryScript") {
    $dir = "/home/user/work/repos/jerryscript";
  }
  else if ($vendor == "Chromium") {
    $dir = "/home/user/work/chromium_repos/chromium/src";
  }
  $cmd = "cd $dir && git log -1 $rev";

  $pipe = popen($cmd , 'r');
  if (!$pipe) {
    die();
  }
  $output = '';
  while(!feof($pipe)) {
    $output .= fread($pipe, 1024);
  }
  pclose($pipe);

  echo $output;
  die();
}

if (!isset($_GET["machine"]) || !isset($_GET["type"]) ||/* !isset($_GET["suite_id"]) || */!isset($_GET["cset"]))
	fault();

$machine = $_GET["machine"];
$type = $_GET["type"];
$suite_id = $_GET["suite_id"];
$cset = $_GET["cset"];

if ($type == "breakdown") {
  $query = mysql_query("SELECT STRAIGHT_JOIN r.id, r.stamp, t.name, s.score, b.mode_id, v.id
    FROM awfy_run r
    JOIN awfy_build b ON r.id = b.run_id
    JOIN awfy_breakdown s ON s.build_id = b.id
    JOIN awfy_suite_test t ON s.suite_test_id = t.id
    JOIN awfy_suite_version v ON v.id = t.suite_version_id
    WHERE r.status > 0
    AND r.machine = $machine
    AND v.suite_id = $suite_id
    AND b.cset LIKE '$cset%'");
  $data = Array();
  while ($output = mysql_fetch_assoc($query)) {
      $data[] = $output;
  }
  echo json_encode($data);
  die();
}
else if ($type == "overview") {
  $query = mysql_query("SELECT STRAIGHT_JOIN r.id, r.stamp, v.name, s.score, b.mode_id, v.id
    FROM awfy_run r
    JOIN awfy_build b ON r.id = b.run_id
    JOIN awfy_score s ON s.build_id = b.id
    JOIN awfy_suite_version v ON v.id = s.suite_version_id
    WHERE r.status > 0
    AND r.machine = $machine
    AND b.cset LIKE '$cset%'");
  $data = Array();
  while ($output = mysql_fetch_assoc($query)) {
      $data[] = $output;
  }
  echo json_encode($data);
  die();
}


if ($type == "single") {
  if (!isset($_GET["test"]))
    fault();

  $test = urldecode($_GET["test"]);

  $query = mysql_query("SELECT STRAIGHT_JOIN r.id, r.stamp, s.score, b.mode_id, v.id
    FROM awfy_run r
    JOIN awfy_build b ON r.id = b.run_id
    JOIN awfy_breakdown s ON s.build_id = b.id
    JOIN awfy_suite_test t ON s.suite_test_id = t.id
    JOIN awfy_suite_version v ON v.id = t.suite_version_id
    WHERE r.status > 0
    AND r.machine = $machine
    AND v.suite_id = $suite_id
    AND b.cset LIKE '$cset%'
    AND t.name = '$test'");
  $data = Array();
  while ($output = mysql_fetch_assoc($query)) {
      $data[] = $output;
  }
  echo json_encode($data);
  die();
}
