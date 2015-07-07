LOCK TABLES `awfy_suite` WRITE;
/*!40000 ALTER TABLE `awfy_suite` DISABLE KEYS */;
INSERT INTO `awfy_suite` VALUES (13, 'VellamoKruptein', 'Vellamo 3.0', -1, 120, 1);
/*!40000 ALTER TABLE `awfy_suite` ENABLE KEYS */;
UNLOCK TABLES;

/*
LOCK TABLES `awfy_suite_version` WRITE;
INSERT INTO `awfy_suite_version` VALUES (11, 13, 'VellamoKruptein 3.0');
UNLOCK TABLES;

LOCK TABLES `awfy_suite_test` WRITE;
INSERT INTO `awfy_suite_test` VALUES (126, 9, 'array_blur', 1), (127, 9, 'array_weighted',1), (128, 9, 'string_chart',1), (129, 9, 'string_filter',1);
UNLOCK TABLES;
*/
