LOCK TABLES `awfy_suite` WRITE;
/*!40000 ALTER TABLE `awfy_suite` DISABLE KEYS */;
INSERT INTO `awfy_suite` VALUES (12, 'VellamoSurfWaxBinder', 'Vellamo 3.0 Surf Wax Binder', -1, 110, 1);
/*!40000 ALTER TABLE `awfy_suite` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `awfy_suite_version` WRITE;
INSERT INTO `awfy_suite_version` VALUES (10, 12, 'Vellamo-SurfWaxBinder 3.0');
UNLOCK TABLES;
/*
LOCK TABLES `awfy_suite_test` WRITE;
INSERT INTO `awfy_suite_test` VALUES (130, 10, 'jsarray_sweep_mrps', 1), (131, 10, 'jsarray_single_mrps',1), (132, 10, 'jsarray_sweep_mwps',1), (133, 10, 'jsarray_single_mwps',1), (134, 10, 'jsarray_seep_mcps', 1), (135, 10, 'imagedata_seq_mrps',1), (136, 10, 'imagedata_seq_mwps',1);
UNLOCK TABLES;
*/
