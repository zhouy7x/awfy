<?php
session_start();

require_once("internals.php");

init_database();

function fault() {
	exit();
}

if (!isset($_GET["machine"]) || !isset($_GET["type"]) || !isset($_GET["suite_id"]) || !isset($_GET["cset"]))
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
