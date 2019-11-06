-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: dvander
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.16.04.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `awfy_breakdown`
--

DROP TABLE IF EXISTS `awfy_breakdown`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_breakdown` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `build_id` int(11) DEFAULT NULL,
  `suite_test_id` int(10) DEFAULT NULL,
  `score` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `build_id` (`build_id`),
  KEY `suite_test_id` (`suite_test_id`)
) ENGINE=MyISAM AUTO_INCREMENT=23589644 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_breakdown`
--

LOCK TABLES `awfy_breakdown` WRITE;
/*!40000 ALTER TABLE `awfy_breakdown` DISABLE KEYS */;
/*!40000 ALTER TABLE `awfy_breakdown` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_build`
--

DROP TABLE IF EXISTS `awfy_build`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_build` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `run_id` int(10) unsigned NOT NULL,
  `mode_id` int(10) unsigned NOT NULL,
  `cset` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index2` (`run_id`,`mode_id`)
) ENGINE=MyISAM AUTO_INCREMENT=348819 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_build`
--

LOCK TABLES `awfy_build` WRITE;
/*!40000 ALTER TABLE `awfy_build` DISABLE KEYS */;
/*!40000 ALTER TABLE `awfy_build` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_config`
--

DROP TABLE IF EXISTS `awfy_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_config` (
  `key` varchar(64) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_config`
--

LOCK TABLES `awfy_config` WRITE;
/*!40000 ALTER TABLE `awfy_config` DISABLE KEYS */;
INSERT INTO `awfy_config` VALUES ('version','3');
/*!40000 ALTER TABLE `awfy_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_machine`
--

DROP TABLE IF EXISTS `awfy_machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_machine` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `os` varchar(30) NOT NULL,
  `cpu` varchar(30) NOT NULL,
  `description` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `frontpage` tinyint(1) NOT NULL DEFAULT '1',
  `pushed_separate` tinyint(1) NOT NULL,
  `last_checked` int(10) unsigned NOT NULL,
  `timeout` int(11) unsigned NOT NULL,
  `contact` mediumtext NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_machine`
--

LOCK TABLES `awfy_machine` WRITE;
/*!40000 ALTER TABLE `awfy_machine` DISABLE KEYS */;
INSERT INTO `awfy_machine` VALUES (1,'ubuntu','x64','BigCore - hsw i5 (V8)',1,1,1,1461546973,1,'1','1'),(2,'ubuntu','x64','Atom - slm N2830 (V8)',1,2,2,1461546973,2,'2','2'),(3,'ubuntu','arm-v7','ARM - Chromebook (V8)',1,4,3,3,3,'3','3'),(4,'ubuntu','x86','Atom -  N2820 (Jerry)',1,5,4,4,3,'4','4'),(5,'ubuntu','x64','BigCore - i7 (V8: Interpreter, FC)',1,6,5,5,5,'5','5'),(6,'ChromeOS','arm-v7','ARM-ChromeOS(V8: octane2)',1,7,6,6,6,'6','6'),(7,'ubuntu','x64','Atom - N3700 (V8)',1,3,7,0,0,'7','7'),(8,'ubuntu','x64','Atom - APL (V8)',1,8,8,0,0,'8','8'),(9,'ChromeOS','arm','chromebook-arm (Chromebook plus Rockchip3399)',1,9,9,0,0,'9','9'),(10,'ChromeOS','x64','chromebook (Electro N3350)',1,10,10,0,0,'10','10'),(11,'ChromeOS','x64','GalliumOS chromebook (Electro N3450)',1,11,11,0,0,'11','11'),(12,'ubuntu','amd64','AMD 2500U',1,12,12,0,0,'12','12'),(13,'ChromeOS','x64','chromebook (Cyan N3150 for compressed pointer)',1,13,13,0,0,'13','13'),(14,'ubuntu','x64','BigCore - i5-6260U (V8: for compressed pointer)',1,14,14,0,0,'14','14'),(15,'ubuntu','amd64','AMD 1800X',1,15,15,0,0,'15','15');
/*!40000 ALTER TABLE `awfy_machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_mode`
--

DROP TABLE IF EXISTS `awfy_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_mode` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `vendor_id` int(10) unsigned NOT NULL,
  `mode` varchar(24) NOT NULL,
  `name` varchar(255) NOT NULL,
  `color` varchar(45) DEFAULT NULL,
  `level` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mode` (`mode`),
  UNIQUE KEY `index3` (`vendor_id`,`mode`)
) ENGINE=MyISAM AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_mode`
--

LOCK TABLES `awfy_mode` WRITE;
/*!40000 ALTER TABLE `awfy_mode` DISABLE KEYS */;
INSERT INTO `awfy_mode` VALUES (31,10,'IoTjs-x86','IoTjs-x86','#33FFFF',99),(28,1,'v8-temp-test','v8-temp-test','#000000',99),(26,1,'v8-turbofan-arm','v8-turbofan-arm','#DB1FA9',1),(17,0,'native','Native C++','#cccccc',1),(24,1,'v8-turbofan-x86','v8-turbofan-x86','#C96B5F',1),(22,1,'v8-turbofan-x64','v8-turbofan-x64','#A9DB1F',1),(20,1,'v8-interpreter-x64','v8-interpreter-x64','#33FF00',1),(18,11,'headless','headless','#FF0000',1),(32,11,'headless-patch','headless-compressed-pointer','#FFFF00',1),(34,1,'v8-turbofan-x64-patch','v8-turbofan-x64-compressed-pointer','#0000FF',1);
/*!40000 ALTER TABLE `awfy_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_run`
--

DROP TABLE IF EXISTS `awfy_run`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_run` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `machine` int(10) unsigned NOT NULL,
  `stamp` int(10) unsigned NOT NULL,
  `status` int(11) NOT NULL,
  `error` mediumtext NOT NULL,
  `finish_stamp` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `machine` (`machine`),
  KEY `status` (`status`)
) ENGINE=MyISAM AUTO_INCREMENT=196457 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_run`
--

LOCK TABLES `awfy_run` WRITE;
/*!40000 ALTER TABLE `awfy_run` DISABLE KEYS */;
/*!40000 ALTER TABLE `awfy_run` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_score`
--

DROP TABLE IF EXISTS `awfy_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_score` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `build_id` int(11) DEFAULT NULL,
  `suite_version_id` int(11) DEFAULT NULL,
  `score` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `build_id` (`build_id`),
  KEY `suite_id` (`suite_version_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2082673 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_score`
--

LOCK TABLES `awfy_score` WRITE;
/*!40000 ALTER TABLE `awfy_score` DISABLE KEYS */;
/*!40000 ALTER TABLE `awfy_score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_suite`
--

DROP TABLE IF EXISTS `awfy_suite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_suite` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(45) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `better_direction` int(11) DEFAULT NULL,
  `sort_order` int(11) NOT NULL,
  `visible` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=39 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_suite`
--

LOCK TABLES `awfy_suite` WRITE;
/*!40000 ALTER TABLE `awfy_suite` DISABLE KEYS */;
INSERT INTO `awfy_suite` VALUES (1,'ss','SunSpider',-1,10,1),(2,'v8','V8 (SS harness)',-1,0,1),(3,'v8real','V8 Benchmark',1,0,1),(4,'kraken','Kraken',-1,30,1),(5,'misc','Assorted tests',-1,40,-1),(6,'octane','Octane2',1,0,1),(7,'asmjs-ubench','asm.js µbench',-1,60,1),(8,'asmjs-apps','asm.js apps',-1,70,1),(9,'embenchen','embenchen',-1,80,1),(10,'jetstream','JetStream-asmjs',-1,90,1),(11,'browsermark','browsermark2.1',1,100,-1),(12,'VellamoSurfWaxBinder','Vellamo 3.1 Surf Wax Binder',1,110,1),(13,'VellamoKruptein','Vellamo 3.1 Kruptein',1,120,1),(14,'VellamoDeepCrossfader','Vellamo 3.1 DeepCrossfader',-1,130,1),(15,'WebXPRTStock','WebXPRT 2013 stock Dashboard',-1,140,1),(16,'WebXPRTStorage','WebXPRT 2013 Storage Notes',-1,150,1),(17,'octane1','Octane1',1,50,1),(18,'browsermark1','browsermark 2.1 dom for content shell',1,160,-1),(19,'browsermark2','browsermark 2.1 scalable solutions for cs',1,170,-1),(20,'JerryBasic','JerryBasic',1,200,-1),(21,'JerrySunspider','JerrySunspider',-1,210,-1),(22,'JerryPassrate','JerryPassrate',1,220,-1),(23,'JetStreamShell','JetStreamShell',1,220,1),(24,'JerrySunspiderMem','JerrySunspiderMem',1,240,1),(25,'JerrySunspiderPerf','JerrySunspiderPerf',-1,250,1),(26,'WebXPRTStockLib','WebXPRT 2015 stocklibrary',-1,151,1),(27,'WebXPRTDNA','WebXPRT 2015 DNA sequence',-1,152,1),(28,'robohornet','RoboHornet benchmark',1,165,1),(29,'speedometer2','speedometer2',1,0,1),(30,'WebTooling','WebTooling',1,0,1),(31,'ARES6','ARES6',-1,30,1),(32,'Unity3D','Unity3D',1,0,1),(33,'d8','file size of d8',-2,0,1),(34,'snapshot_blob','file size of snapshot_blob.bin',-2,0,1),(35,'jetstream2','jetstream2',1,0,1),(36,'polybench','polybench-wasm',-1,0,1),(37,'spec2k6','Spec2k6-wasm',-1,0,1),(38,'Jetstream2D8','jetstream2-d8',1,0,1);
/*!40000 ALTER TABLE `awfy_suite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_suite_test`
--

DROP TABLE IF EXISTS `awfy_suite_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_suite_test` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `suite_version_id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `visible` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `suite_id` (`suite_version_id`,`name`)
) ENGINE=MyISAM AUTO_INCREMENT=724 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_suite_test`
--

LOCK TABLES `awfy_suite_test` WRITE;
/*!40000 ALTER TABLE `awfy_suite_test` DISABLE KEYS */;
INSERT INTO `awfy_suite_test` VALUES (1,1,'box2d-loadtime',1),(2,1,'box2d-throughput',1),(3,1,'bullet-loadtime',1),(4,1,'bullet-throughput',1),(5,1,'lua_binarytrees-loadtime',1),(6,1,'lua_binarytrees-throughput',1),(7,1,'zlib-loadtime',1),(8,1,'zlib-throughput',1),(9,2,'copy',1),(10,2,'corrections',1),(11,2,'fannkuch',1),(12,2,'fasta',1),(13,2,'life',1),(14,2,'memops',1),(15,2,'primes',1),(16,2,'skinning',1),(17,3,'cube',1),(18,3,'morph',1),(19,3,'raytrace',1),(20,3,'binary-trees',1),(21,3,'fannkuch',1),(22,3,'nbody',1),(23,3,'nsieve',1),(24,3,'3bit-bits-in-byte',1),(25,3,'bits-in-byte',1),(26,3,'bitwise-and',1),(27,3,'nsieve-bits',1),(28,3,'recursive',1),(29,3,'aes',1),(30,3,'md5',1),(31,3,'sha1',1),(32,3,'format-tofte',1),(33,3,'format-xparb',1),(34,3,'cordic',1),(35,3,'partial-sums',1),(36,3,'spectral-norm',1),(37,3,'dna',1),(38,3,'base64',1),(39,3,'fasta',1),(40,3,'tagcloud',1),(41,3,'unpack-code',1),(42,3,'validate-input',1),(43,4,'astar',1),(44,4,'beat-detection',1),(45,4,'dft',1),(46,4,'fft',1),(47,4,'oscillator',1),(48,4,'gaussian-blur',1),(49,4,'darkroom',1),(50,4,'desaturate',1),(51,4,'parse-financial',1),(52,4,'stringify-tinderbox',1),(53,4,'crypto-aes',1),(54,4,'crypto-ccm',1),(55,4,'crypto-pbkdf2',1),(56,4,'crypto-sha256-iterative',1),(57,5,'basic-emptyloop',1),(58,5,'basic-intops',1),(59,5,'basic-fpops',1),(60,5,'basic-array',1),(61,5,'basic-strcat',1),(62,5,'basic-arguments',1),(63,5,'basic-closures',1),(64,5,'bugs-612930-solve-sudoku',1),(65,5,'bugs-658844-sha256-bitcoins',1),(66,5,'bugs-654410-nezulator',1),(67,5,'bugs-508716-fluid-dynamics',1),(68,5,'bugs-608733-interpreter',1),(69,5,'bugs-608733-trace-compiler',1),(70,5,'bugs-636096-model2d',1),(71,5,'bugs-652377-jslint-on-jslint',1),(72,5,'bugs-652303-arraymod',1),(73,5,'bugs-659467-jsunzip',1),(74,5,'bugs-663087-decompress-gzip',1),(75,5,'bugs-847389-jpeg2000',1),(76,5,'f32-fft',1),(77,5,'f32-exp',1),(78,5,'f32-markov',1),(79,5,'typedobj-utf8array-typedobj',1),(80,5,'typedobj-utf8array-standard',1),(81,5,'typedobj-write-struct-field-typedobj',1),(82,5,'typedobj-write-struct-field-standard',1),(83,5,'typedobj-simple-struct-typedobj',1),(84,5,'typedobj-simple-struct-standard',1),(85,5,'typedobj-splay-typedobj',1),(86,5,'typedobj-splay-standard',1),(87,5,'forEach-baseline',1),(88,5,'forEach-custom',1),(89,5,'forEach-library',1),(90,6,'Richards',1),(91,6,'DeltaBlue',1),(92,6,'Crypto',1),(93,6,'RayTrace',1),(94,6,'EarleyBoyer',1),(95,6,'RegExp',1),(96,6,'Splay',1),(97,6,'SplayLatency',1),(98,6,'NavierStokes',1),(99,6,'PdfJS',1),(100,6,'Mandreel',1),(101,6,'MandreelLatency',1),(102,6,'Gameboy',1),(103,6,'CodeLoad',1),(104,6,'Box2D',1),(105,6,'zlib',1),(106,6,'Typescript',1),(107,7,'bench_box2d',1),(108,7,'bench_bullet',1),(109,7,'bench_copy',1),(110,7,'bench_corrections',1),(111,7,'bench_fannkuch',1),(112,7,'bench_fasta',1),(113,7,'bench_lua_binarytrees',1),(114,7,'bench_memops',1),(115,7,'bench_primes',1),(116,7,'bench_skinning',1),(117,7,'bench_zlib',1),(118,8,'bigfib.cpp',1),(119,8,'container.cpp',1),(120,8,'dry.c',1),(121,8,'float-mm.c',1),(122,8,'gcc-loops.cpp',1),(123,8,'n-body.c',1),(124,8,'quicksort.c',1),(125,8,'towers.c',1),(126,-1,'',1),(127,9,'array_blur',1),(128,9,'array_weighted',1),(129,9,'string_chat',1),(130,9,'string_filter',1),(131,10,'jsarray_sweep_mrps',1),(132,10,'jsarray_single_mrps',1),(133,10,'jsarray_sweep_mwps',1),(134,10,'jsarray_single_mwps',1),(135,10,'jsarray_sweep_mcps',1),(136,10,'imagedata_seq_mrps',1),(137,10,'imagedata_seq_mwps',1),(138,11,'cryptoJSAESEncryptTime',1),(139,11,'cryptoJSAESDecryptTime',1),(140,11,'cryptoJSSHA2HashTime',1),(141,14,'0',1),(142,14,'1',1),(143,14,'2',1),(144,14,'3',1),(145,14,'4',1),(146,14,'5',1),(147,14,'6',1),(148,14,'7',1),(149,14,'8',1),(150,14,'9',1),(151,12,'1',1),(152,13,'1',1),(153,15,'Richards',1),(154,15,'DeltaBlue',1),(155,15,'Crypto',1),(156,15,'RayTrace',1),(157,15,'EarleyBoyer',1),(158,15,'RegExp',1),(159,15,'Splay',1),(160,15,'NavierStokes',1),(161,15,'PdfJS',1),(162,15,'Mandreel',1),(163,15,'Gameboy',1),(164,15,'CodeLoad',1),(165,15,'Box2D',1),(180,17,'DeltaBlue',1),(181,17,'Crypto',1),(182,17,'RayTrace',1),(183,17,'EarleyBoyer',1),(179,17,'Richards',1),(184,17,'RegExp',1),(185,17,'Splay',1),(186,17,'NavierStokes',1),(187,17,'PdfJS',1),(188,17,'Mandreel',1),(189,17,'Gameboy',1),(190,17,'CodeLoad',1),(191,17,'Box2D',1),(192,18,'DOM Advanced Search 2.1',1),(193,18,'DOM Create Source 2.1',1),(194,18,'DOM Dynamic Create 2.1',1),(195,18,'DOM Search 2.1',1),(196,19,'Scalable Solutions AngularJS 2.1',1),(197,19,'Scalable Solutions Backbone 2.1',1),(198,19,'Scalable Solutions Ember 2.1',1),(199,19,'Scalable Solutions Knockout 2.1',1),(200,20,'binary_size',1),(201,20,'stack',1),(202,20,'heap',1),(203,20,'mmap',1),(204,20,'USS',1),(205,20,'PSS',1),(206,20,'RSS',1),(207,20,'iotjs_stack',1),(208,20,'iotjs_heap',1),(209,20,'iotjs_mmap',1),(210,21,'3d-cube.js',1),(211,21,'3d-morph.js',1),(212,21,'access-fannkuch.js',1),(213,21,'access-binary-trees.js',1),(214,21,'access-nbody.js',1),(215,21,'access-nsieve.js',1),(216,21,'bitops-3bit-bits-in-byte.js',1),(217,21,'bitops-bits-in-byte.js',1),(218,21,'bitops-bitwise-and.js',1),(219,21,'bitops-nsieve-bits.js',1),(220,21,'controlflow-recursive.js',1),(221,21,'crypto-aes.js',1),(222,21,'crypto-sha1.js',1),(223,21,'date-format-tofte.js',1),(224,21,'date-format-xparb.js',1),(225,21,'math-cordic.js',1),(226,21,'math-partial-sums.js',1),(227,21,'math-spectral-norm.js',1),(228,21,'regexp-dna.js',1),(229,21,'string-fasta.js',1),(230,21,'string-tagcloud.js',1),(231,21,'string-unpack-code.js',1),(232,21,'overall',1),(235,23,'3d-cube',1),(234,22,'passrate',1),(236,23,'3d-raytrace',1),(237,23,'base64',1),(238,23,'cdjs',1),(239,23,'code-first-load',1),(240,23,'code-multi-load',1),(241,23,'crypto-aes',1),(242,23,'crypto-md5',1),(243,23,'crypto-sha1',1),(244,23,'date-format-tofte',1),(245,23,'date-format-xparb',1),(246,23,'mandreel-latency',1),(247,23,'mandreel',1),(248,23,'n-body',1),(249,23,'regex-dna',1),(250,23,'splay-latency',1),(251,23,'splay',1),(252,23,'tagcloud',1),(253,23,'typescript',1),(324,24,'3d-cube.js',1),(255,23,'box2d',1),(256,23,'crypto',1),(257,23,'delta-blue',1),(259,23,'earley-boyer',1),(260,23,'gbemu',1),(261,23,'hash-map',1),(262,23,'navier-stokes',1),(263,23,'pdfjs',1),(264,23,'proto-raytracer',1),(265,23,'regexp-2010',1),(266,23,'richards',1),(267,23,'zlib',1),(268,23,'bigfib.cpp',1),(269,23,'container.cpp',1),(270,23,'dry.c',1),(271,23,'float-mm.c',1),(272,23,'gcc-loops.cpp',1),(273,23,'n-body.c',1),(274,23,'quicksort.c',1),(275,23,'towers.c',1),(400,25,'access-nbody.js',1),(326,24,'3d-raytrace.js',1),(327,24,'access-binary-trees.js',1),(328,24,'access-fannkuch.js',1),(329,24,'access-nbody.js',1),(330,24,'bitops-3bit-bits-in-byte.js',1),(331,24,'bitops-bits-in-byte.js',1),(332,24,'bitops-bitwise-and.js',1),(333,24,'controlflow-recursive.js',1),(334,24,'crypto-aes.js',1),(335,24,'date-format-tofte.js',1),(336,24,'date-format-xparb.js',1),(337,24,'math-cordic.js',1),(338,24,'math-partial-sums.js',1),(339,24,'math-spectral-norm.js',1),(401,25,'math-partial-sums.js',1),(341,24,'string-fasta.js',1),(402,28,'Object Scope Access',1),(403,28,'ES5 Property Accessors',1),(404,28,'Argument instantiation',1),(345,24,'bitops-nsieve-bits.js',1),(346,24,'crypto-md5.js',1),(347,24,'crypto-sha1.js',1),(348,24,'string-base64.js',1),(405,29,'0',1),(350,25,'string-base64.js',1),(351,26,'1',1),(352,27,'1',1),(399,25,'3d-raytrace.js',1),(406,29,'1',1),(407,29,'2',1),(408,29,'3',1),(409,29,'4',1),(410,29,'5',1),(411,29,'6',1),(412,29,'7',1),(413,29,'8',1),(414,29,'9',1),(308,25,'3d-cube.js',1),(309,25,'access-binary-trees.js',1),(310,25,'access-fannkuch.js',1),(311,25,'bitops-3bit-bits-in-byte.js',1),(312,25,'bitops-bits-in-byte.js',1),(313,25,'bitops-bitwise-and.js',1),(314,25,'bitops-nsieve-bits.js',1),(315,25,'controlflow-recursive.js',1),(316,25,'crypto-aes.js',1),(317,25,'crypto-md5.js',1),(318,25,'crypto-sha1.js',1),(319,25,'date-format-tofte.js',1),(320,25,'date-format-xparb.js',1),(321,25,'math-cordic.js',1),(322,25,'math-spectral-norm.js',1),(323,25,'string-fasta.js',1),(440,30,'Angular2-TypeScript-TodoMVC',1),(439,30,'AngularJS-TodoMVC',1),(438,30,'BackboneJS-TodoMVC',1),(437,30,'EmberJS-Debug-TodoMVC',1),(436,30,'EmberJS-TodoMVC',1),(435,30,'React-Redux-TodoMVC',1),(434,30,'React-TodoMVC',1),(433,30,'Vanilla-ES2015-Babel-Webpack-TodoMVC',1),(432,30,'Vanilla-ES2015-TodoMVC',1),(431,30,'VanillaJS-TodoMVC',1),(441,30,'VueJS-TodoMVC',1),(442,30,'jQuery-TodoMVC',1),(443,30,'Preact-TodoMVC',1),(444,30,'Inferno-TodoMVC',1),(445,30,'Elm-TodoMVC',1),(446,30,'Flight-TodoMVC',1),(447,31,'acorn',1),(448,31,'babel',1),(449,31,'babylon',1),(450,31,'buble',1),(451,31,'chai',1),(452,31,'coffeescript',1),(453,31,'espree',1),(454,31,'esprima',1),(455,31,'jshint',1),(456,31,'lebab',1),(457,31,'prepack',1),(458,31,'prettier',1),(459,31,'source-map',1),(460,31,'typescript',1),(461,31,'uglify-es',1),(462,31,'uglify-js',1),(463,32,'ML-firstIteration',1),(464,32,'ML-worst4iterations',1),(465,32,'ML-average',1),(466,32,'Babylon-firstIteration',1),(467,32,'Babylon-worst4iterations',1),(468,32,'Babylon-average',1),(469,32,'Basic-firstIteration',1),(470,32,'Basic-worst4iterations',1),(471,32,'Basic-average',1),(472,32,'Air-firstIteration',1),(473,32,'Air-worst4iterations',1),(474,32,'Air-average',1),(475,33,'Mandelbrot Script',1),(491,30,'  port',1),(477,33,'CryptoHash Script',1),(492,36,'3d-cube-SP',1),(479,33,'Asteroid Field',1),(480,33,'Particles',1),(481,33,'Physics Meshes',1),(482,33,'Physics Cubes',1),(483,33,'Physics Spheres',1),(484,33,'2D Physics Spheres',1),(485,33,'2D Physics Boxes',1),(486,33,'AI Agents',1),(476,33,'Instantiate & Destroy',1),(478,33,'Animation & Skinning',1),(493,36,'3d-raytrace-SP',1),(494,36,'acorn-wtb',1),(495,36,'ai-astar',1),(496,36,'Air',1),(497,36,'async-fs',1),(498,36,'Babylon',1),(499,36,'babylon-wtb',1),(500,36,'base64-SP',1),(501,36,'Basic',1),(502,36,'bomb-workers',1),(503,36,'Box2D',1),(504,36,'cdjs',1),(505,36,'chai-wtb',1),(506,36,'coffeescript-wtb',1),(507,36,'crypto',1),(508,36,'crypto-aes-SP',1),(509,36,'crypto-md5-SP',1),(510,36,'crypto-sha1-SP',1),(511,36,'date-format-tofte-SP',1),(512,36,'date-format-xparb-SP',1),(513,36,'delta-blue',1),(514,36,'earley-boyer',1),(515,36,'espree-wtb',1),(516,36,'first-inspector-code-load',1),(517,36,'FlightPlanner',1),(518,36,'float-mm.c',1),(519,36,'gaussian-blur',1),(520,36,'gbemu',1),(521,36,'gcc-loops-wasm',1),(522,36,'hash-map',1),(523,36,'HashSet-wasm',1),(524,36,'jshint-wtb',1),(525,36,'json-parse-inspector',1),(526,36,'json-stringify-inspector',1),(527,36,'lebab-wtb',1),(528,36,'mandreel',1),(529,36,'ML',1),(530,36,'multi-inspector-code-load',1),(531,36,'n-body-SP',1),(532,36,'navier-stokes',1),(533,36,'octane-code-load',1),(534,36,'octane-zlib',1),(535,36,'OfflineAssembler',1),(536,36,'pdfjs',1),(537,36,'prepack-wtb',1),(538,36,'quicksort-wasm',1),(539,36,'raytrace',1),(540,36,'regex-dna-SP',1),(541,36,'regexp',1),(542,36,'richards',1),(543,36,'richards-wasm',1),(544,36,'segmentation',1),(545,36,'splay',1),(546,36,'stanford-crypto-aes',1),(547,36,'stanford-crypto-pbkdf2',1),(548,36,'stanford-crypto-sha256',1),(549,36,'string-unpack-code-SP',1),(550,36,'tagcloud-SP',1),(551,36,'tsf-wasm',1),(552,36,'typescript',1),(553,36,'uglify-js-wtb',1),(554,36,'UniPoker',1),(555,36,'WSL',1),(556,-1,'WSL',1),(557,-1,'UniPoker',1),(558,-1,'uglify-js-wtb',1),(559,-1,'typescript',1),(560,-1,'tsf-wasm',1),(561,-1,'tagcloud-SP',1),(562,-1,'string-unpack-code-SP',1),(563,-1,'stanford-crypto-sha256',1),(564,-1,'stanford-crypto-pbkdf2',1),(565,-1,'stanford-crypto-aes',1),(566,-1,'splay',1),(567,-1,'richards-wasm',1),(568,-1,'richards',1),(569,-1,'regexp',1),(570,-1,'regex-dna-SP',1),(571,-1,'raytrace',1),(572,-1,'quicksort-wasm',1),(573,-1,'prepack-wtb',1),(574,-1,'pdfjs',1),(575,-1,'OfflineAssembler',1),(576,-1,'octane-zlib',1),(577,-1,'octane-code-load',1),(578,-1,'navier-stokes',1),(579,-1,'n-body-SP',1),(580,-1,'multi-inspector-code-load',1),(581,-1,'ML',1),(582,-1,'mandreel',1),(583,-1,'lebab-wtb',1),(584,-1,'json-stringify-inspector',1),(585,-1,'json-parse-inspector',1),(586,-1,'jshint-wtb',1),(587,-1,'HashSet-wasm',1),(588,-1,'hash-map',1),(589,-1,'gcc-loops-wasm',1),(590,-1,'gbemu',1),(591,-1,'gaussian-blur',1),(592,-1,'float-mm.c',1),(593,-1,'FlightPlanner',1),(594,-1,'first-inspector-code-load',1),(595,-1,'espree-wtb',1),(596,-1,'earley-boyer',1),(597,-1,'delta-blue',1),(598,-1,'date-format-xparb-SP',1),(599,-1,'date-format-tofte-SP',1),(600,-1,'crypto-sha1-SP',1),(601,-1,'crypto-md5-SP',1),(602,-1,'crypto-aes-SP',1),(603,-1,'crypto',1),(604,-1,'coffeescript-wtb',1),(605,-1,'chai-wtb',1),(606,-1,'cdjs',1),(607,-1,'Box2D',1),(608,-1,'Basic',1),(609,-1,'base64-SP',1),(610,-1,'babylon-wtb',1),(611,-1,'Babylon',1),(612,-1,'async-fs',1),(613,-1,'Air',1),(614,-1,'ai-astar',1),(615,-1,'acorn-wtb',1),(616,-1,'3d-raytrace-SP',1),(617,-1,'3d-cube-SP',1),(618,38,'WSL',1),(619,38,'UniPoker',1),(620,38,'uglify-js-wtb',1),(621,38,'typescript',1),(622,38,'tsf-wasm',1),(623,38,'tagcloud-SP',1),(624,38,'string-unpack-code-SP',1),(625,38,'stanford-crypto-sha256',1),(626,38,'stanford-crypto-pbkdf2',1),(627,38,'stanford-crypto-aes',1),(628,38,'splay',1),(629,38,'richards-wasm',1),(630,38,'richards',1),(631,38,'regexp',1),(632,38,'regex-dna-SP',1),(633,38,'raytrace',1),(634,38,'quicksort-wasm',1),(635,38,'prepack-wtb',1),(636,38,'pdfjs',1),(637,38,'OfflineAssembler',1),(638,38,'octane-zlib',1),(639,38,'octane-code-load',1),(640,38,'navier-stokes',1),(641,38,'n-body-SP',1),(642,38,'multi-inspector-code-load',1),(643,38,'ML',1),(644,38,'mandreel',1),(645,38,'lebab-wtb',1),(646,38,'json-stringify-inspector',1),(647,38,'json-parse-inspector',1),(648,38,'jshint-wtb',1),(649,38,'HashSet-wasm',1),(650,38,'hash-map',1),(651,38,'gcc-loops-wasm',1),(652,38,'gbemu',1),(653,38,'gaussian-blur',1),(654,38,'float-mm.c',1),(655,38,'FlightPlanner',1),(656,38,'first-inspector-code-load',1),(657,38,'espree-wtb',1),(658,38,'earley-boyer',1),(659,38,'delta-blue',1),(660,38,'date-format-xparb-SP',1),(661,38,'date-format-tofte-SP',1),(662,38,'crypto-sha1-SP',1),(663,38,'crypto-md5-SP',1),(664,38,'crypto-aes-SP',1),(665,38,'crypto',1),(666,38,'coffeescript-wtb',1),(667,38,'chai-wtb',1),(668,38,'cdjs',1),(669,38,'Box2D',1),(670,38,'Basic',1),(671,38,'base64-SP',1),(672,38,'babylon-wtb',1),(673,38,'Babylon',1),(674,38,'async-fs',1),(675,38,'Air',1),(676,38,'ai-astar',1),(677,38,'acorn-wtb',1),(678,38,'3d-raytrace-SP',1),(679,38,'3d-cube-SP',1),(680,39,'gemm',1),(681,39,'gemver',1),(682,39,'gesummv',1),(683,39,'symm',1),(684,39,'syr2k',1),(685,39,'syrk',1),(686,39,'trmm',1),(687,39,'2mm',1),(688,39,'3mm',1),(689,39,'atax',1),(690,39,'bicg',1),(691,39,'doitgen',1),(692,39,'mvt',1),(693,39,'cholesky',1),(694,39,'durbin',1),(695,39,'gramschmidt',1),(696,39,'lu',1),(697,39,'ludcmp',1),(698,39,'trisolv',1),(699,39,'correlation',1),(700,39,'covariance',1),(701,39,'adi',1),(702,39,'fdtd-2d',1),(703,39,'heat-3d',1),(704,39,'jacobi-1d',1),(705,39,'jacobi-2d',1),(706,39,'seidel-2d',1),(707,39,'deriche',1),(708,39,'floyd-warshall',1),(709,39,'nussinov',1),(710,40,'gobmk-compilation',1),(711,40,'gobmk-execution',1),(712,40,'lbm-compilation',1),(713,40,'lbm-execution',1),(714,40,'libquantum-compilation',1),(715,40,'libquantum-execution',1),(716,40,'namd-compilation',1),(717,40,'namd-execution',1),(718,40,'povray-compilation',1),(719,40,'povray-execution',1),(720,40,'sjeng-compilation',1),(721,40,'sjeng-execution',1),(722,31,'Unknown type',1),(723,36,'  port',1);
/*!40000 ALTER TABLE `awfy_suite_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_suite_version`
--

DROP TABLE IF EXISTS `awfy_suite_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_suite_version` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `suite_id` int(10) unsigned NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_suite_version`
--

LOCK TABLES `awfy_suite_version` WRITE;
/*!40000 ALTER TABLE `awfy_suite_version` DISABLE KEYS */;
INSERT INTO `awfy_suite_version` VALUES (1,8,'asmjs-apps 0.2'),(2,7,'asmjs-ubench 0.3'),(3,1,'ss 1.0.1'),(4,4,'kraken 1.1'),(5,5,'misc 0.1'),(6,6,'octane 2.0.1'),(7,9,'embenchen 0.0.2'),(8,10,'jetstream 1.0.1'),(9,11,'browsermark 2.1'),(10,12,'VellamoSurfWaxBinder 3.1'),(12,15,'WebXPRTStock 2013'),(13,16,'WebXPRTStorage 2013'),(14,14,'VellamoDeepCrossfader 3.1'),(11,13,'VellamoKruptein 3.1'),(15,17,'octane1 1.0'),(20,20,'JerryBasic 1.0'),(18,18,'browsermark1 2.1'),(19,19,'browsermark2 2.1'),(21,21,'JerrySunspider 1.0.1'),(22,22,'JerryPassrate 1.0'),(23,23,'JetStreamShell 1.0'),(24,25,'JerrySunspiderPerf 1.0.2'),(25,24,'JerrySunspiderMem 1.0.2'),(26,26,'WebXPRTStockLib 2015'),(27,27,'WebXPRTDNA 2015'),(28,28,'robohornet 1.0'),(29,14,'VellamoDeepCrossfader 3.0'),(30,29,'speedometer2 '),(31,30,'WebTooling '),(32,31,'ARES6 '),(33,32,'Unity3D '),(34,33,'d8'),(35,34,'snapshot_blob'),(36,35,'jetstream2 '),(37,36,'polybench-wasm 1.0'),(38,38,'Jetstream2D8 '),(39,36,'polybench '),(40,37,'spec2k6 ');
/*!40000 ALTER TABLE `awfy_suite_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `awfy_vendor`
--

DROP TABLE IF EXISTS `awfy_vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awfy_vendor` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `vendor` varchar(30) NOT NULL,
  `csetURL` varchar(255) NOT NULL,
  `browser` varchar(30) NOT NULL,
  `rangeURL` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awfy_vendor`
--

LOCK TABLES `awfy_vendor` WRITE;
/*!40000 ALTER TABLE `awfy_vendor` DISABLE KEYS */;
INSERT INTO `awfy_vendor` VALUES (1,'V8','Google','https://chromium.googlesource.com/v8/v8.git/+/','Chrome','http://code.google.com/p/v8/source/list?num=25&start={to}'),(2,'SpiderMonkey','Mozilla','http://hg.mozilla.org/integration/mozilla-inbound/rev/','Firefox','http://hg.mozilla.org/integration/mozilla-inbound/pushloghtml?fromchange={from}&tochange={to}'),(10,'Iotjs','Samsung','https://github.com/Samsung/iotjs/commit/','Samsung','https://github.com/Samsung/iotjs/commit/{to}'),(11,'Chromium','Google','https://chromium.googlesource.com/chromium/src/+/','Chrome','http://code.google.com/p/chromium/source/list?num=25&start={to}'),(9,'JerryScript','Samsung','https://github.com/Samsung/jerryscript/commit/','Samsung','https://github.com/Samsung/jerryscript/commit/{to}');
/*!40000 ALTER TABLE `awfy_vendor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-05 13:57:33
