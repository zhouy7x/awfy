LOCK TABLES `awfy_suite` WRITE;
/*!40000 ALTER TABLE `awfy_suite` DISABLE KEYS */;
INSERT INTO `awfy_suite` VALUES (9, 'embenchen', 'the Emscripten benchmark suite', -1, 80, 1);
/*!40000 ALTER TABLE `awfy_suite` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `awfy_suite_version` WRITE;
INSERT INTO `awfy_suite_version` VALUES (7, 9, 'embenchen 0.0.2');
UNLOCK TABLES;

LOCK TABLES `awfy_suite_test` WRITE;
/*!40000 ALTER TABLE `awfy_suite_test` DISABLE KEYS */;
INSERT INTO `awfy_suite_test` VALUES (107, 7, 'bench_box2d',1), (108, 7, 'bench_bullet',1), (109, 7, 'bench_copy',1), (110, 7, 'bench_corrections',1), (111, 7, 'bench_fannkuch',1), (112, 7, 'bench_fasta',1), (113, 7, 'bench_lua_binarytrees',1), (114, 7, 'bench_memops',1), (115, 7, 'bench_primes',1), (116, 7, 'bench_skinning',1), (117, 7, 'bench_zlib',1);
/*!40000 ALTER TABLE `awfy_suite_test` ENABLE KEYS */;
UNLOCK TABLES;
