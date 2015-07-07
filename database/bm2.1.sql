LOCK TABLES `awfy_suite` WRITE;
/*!40000 ALTER TABLE `awfy_suite` DISABLE KEYS */;
INSERT INTO `awfy_suite` VALUES (11, 'browsermark', 'browsermark2.1', -1, 100, 1);
/*!40000 ALTER TABLE `awfy_suite` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `awfy_suite_version` WRITE;
INSERT INTO `awfy_suite_version` VALUES (9, 11, 'browsermark 2.1');
UNLOCK TABLES;

LOCK TABLES `awfy_suite_test` WRITE;
/*!40000 ALTER TABLE `awfy_suite_test` DISABLE KEYS */;
INSERT INTO `awfy_suite_test` VALUES (126, 9, 'array_blur', 1), (127, 9, 'array_weighted',1), (128, 9, 'string_chart',1), (129, 9, 'string_filter',1);
/*!40000 ALTER TABLE `awfy_suite_test` ENABLE KEYS */;
UNLOCK TABLES;

