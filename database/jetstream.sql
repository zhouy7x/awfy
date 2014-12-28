LOCK TABLES `awfy_suite` WRITE;
/*!40000 ALTER TABLE `awfy_suite` DISABLE KEYS */;
INSERT INTO `awfy_suite` VALUES (10, 'jetstream', 'JetStream-asmjs', -1, 90, 1);
/*!40000 ALTER TABLE `awfy_suite` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `awfy_suite_version` WRITE;
INSERT INTO `awfy_suite_version` VALUES (8, 10, 'jetstream 1.0.1');
UNLOCK TABLES;

LOCK TABLES `awfy_suite_test` WRITE;
/*!40000 ALTER TABLE `awfy_suite_test` DISABLE KEYS */;
INSERT INTO `awfy_suite_test` VALUES (118, 8, 'bigfib.cpp', 1), (119, 8, 'container.cpp',1), (120, 8, 'dry.c',1), (121, 8, 'float-mm.c',1), (122, 8, 'gcc-loops.cpp',1), (123, 8, 'n-body.c',1), (124, 8, 'quicksort.c',1), (125, 8, 'towers.c',1);
/*!40000 ALTER TABLE `awfy_suite_test` ENABLE KEYS */;
UNLOCK TABLES;
