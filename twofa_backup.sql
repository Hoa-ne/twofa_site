-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: twofa_db
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_backupcode`
--

DROP TABLE IF EXISTS `accounts_backupcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_backupcode` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_backupcode_user_id_7e72a328_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_backupcode_user_id_7e72a328_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_backupcode`
--

LOCK TABLES `accounts_backupcode` WRITE;
/*!40000 ALTER TABLE `accounts_backupcode` DISABLE KEYS */;
INSERT INTO `accounts_backupcode` VALUES (71,'pbkdf2_sha256$1000000$HVFlB86uCSEZBdFfe3aXbV$cjodN73wTXRYG2UHLN/KP/cDMsemltN+d0gokJQuaMI=',0,'2025-11-11 12:42:15.256067',16),(72,'pbkdf2_sha256$1000000$NTBz9rcJ331Osm4N4hJzyK$MTYNE87rjbhdB1lkOp1f2DYKUoBaziRIOLOsLtNOFRM=',0,'2025-11-11 12:42:15.256093',16),(73,'pbkdf2_sha256$1000000$40h28Am83oQIGdhzl770OC$NFZD6P79G9tl5AmCPvLIY5SMB5/Yag0T3n2Dhl08rEo=',0,'2025-11-11 12:42:15.256103',16),(74,'pbkdf2_sha256$1000000$pVBUpFV0d3GvOLdyBe1QJm$mkzmX0+A3LWUVFU4pFuMHlusZoAOpLVCIggpXKa56Rg=',0,'2025-11-11 12:42:15.256111',16),(75,'pbkdf2_sha256$1000000$LPKPLmZ6cW78GBixVWDTU1$jQWGbe4n/HbQUTjlxeM3zLq7TEDaKt1D8AHlDJ6KNT8=',0,'2025-11-11 12:42:15.256119',16),(76,'pbkdf2_sha256$1000000$x9SKMCUUsxiEfG9vGk2XlF$1+RbZzLHZ29WM+nmaUD9InJGsitVVByEhA2xks0rtJ4=',0,'2025-11-11 12:42:15.256127',16),(77,'pbkdf2_sha256$1000000$k3Gziwr8vqZ5QEbnDwCNkO$vkspY2/kT+6rH/s8eIdviCPWWUZLTGfEm7/omKfyfG4=',0,'2025-11-11 12:42:15.256134',16),(78,'pbkdf2_sha256$1000000$5TrcAMbY7TaVYm3QLCbqGF$DJooKYt1ZCrmXbNBr1MPYPAk+0XRWHOlpY/ZNof6XtE=',0,'2025-11-11 12:42:15.256142',16),(79,'pbkdf2_sha256$1000000$uX4TyPbt92kj6YAxFycdIp$cNVbr1YwYO8+QOsKMmFjI3vnRUZLsh2lZw9XFSK5EYI=',0,'2025-11-11 12:42:15.256149',16),(80,'pbkdf2_sha256$1000000$R46wHYjNShoBSHrEn2FMwe$fFvQHm7Wo8Xfo/P8Q0GPyhUKUQZRniDwwEXL9IM/VFs=',0,'2025-11-11 12:42:15.256156',16),(141,'pbkdf2_sha256$1000000$JSlpi0s3KlNGKiIwnoNviv$zU2XprM1DCnUfN5MFi1Y2nFHCYoYAlkobGjk8RGVBqU=',0,'2025-11-17 11:19:39.130664',31),(142,'pbkdf2_sha256$1000000$wZGu7UmdWA3ud2XADV7V8d$tTrjqsSYyHIYGRNGryHtyYeSM3tbgaUCdk8E6qe2wrc=',0,'2025-11-17 11:19:39.130690',31),(143,'pbkdf2_sha256$1000000$oRXBRu5g7BQN7cy6xQgtXq$DqgOvus6goZY9PEhPzm6Nit2VzI7j3Pdt6d9R63u8r8=',0,'2025-11-17 11:19:39.130701',31),(144,'pbkdf2_sha256$1000000$PVdVuMyNd7ZVZ57wbuzqyi$9GZNViTuZKAA34YUY5wAa7cO2W094c2jLLEld3iZ/sc=',0,'2025-11-17 11:19:39.130709',31),(145,'pbkdf2_sha256$1000000$Cc4buYjW5fV6ZTp6YOmbwz$R15CJN1n0KF770DZ381xlm4d4YlRdjdLnahI8Gr84YE=',0,'2025-11-17 11:19:39.130717',31),(146,'pbkdf2_sha256$1000000$KJzRI1BizDBYp2Pw1WyfMN$M/QTSLbq+1A4JxgCXANNSCjOW4ifAYJ2JBLvpt5DAOQ=',0,'2025-11-17 11:19:39.130725',31),(147,'pbkdf2_sha256$1000000$OeBs8bzR3D8h1EG5yLinYP$AB6K7bX+dUhyaSnkvNvz9/TaC4sI9xERoZhhs1NeWps=',0,'2025-11-17 11:19:39.130733',31),(148,'pbkdf2_sha256$1000000$463V0I1fMLaW7KMgVAwpal$V11cSITEM42xMPuGaILF+0/VyhEJDvUbrX5BgjRVbOQ=',0,'2025-11-17 11:19:39.130741',31),(149,'pbkdf2_sha256$1000000$9YO3gN1DbBL15zwkaPVvYt$sqXXhNtjnYIk3W9wZfmeFjM4MepoFPEEcrx4S6EJLRg=',0,'2025-11-17 11:19:39.130749',31),(150,'pbkdf2_sha256$1000000$RL1JMksLoH4nY7B0VUwXuw$OWPBaqMbS0m+ETFB9ggo/abr+Q7xE9zm6ctBZc3Qh9c=',0,'2025-11-17 11:19:39.130757',31),(161,'pbkdf2_sha256$1000000$6sfgHiiaikJ7oYy9aJI9Bt$Nb8QG2glSDWYe1Qi8mWIwyFl5TtX25bRmlYan2xiDCI=',0,'2025-11-20 15:26:13.802616',36),(162,'pbkdf2_sha256$1000000$VAekXQk7oANboTrO29wlxZ$/ubsiAIOxykjOoib+qtFOn+UpjJTWD9bnYl36V63X58=',0,'2025-11-20 15:26:13.802642',36),(163,'pbkdf2_sha256$1000000$vMSvOclcLKhz5qD6jMKYTS$8UOVaS83K/bxSP1y9uKxOHXlCBmWcLKX5A+qoXUH1Xw=',0,'2025-11-20 15:26:13.802652',36),(164,'pbkdf2_sha256$1000000$Ovu1l8XN4O06nmkFmjQ8I5$LHhvMwOmu75bbb9P2Wsu6ePkWWW3ZCmlEbpTLeai/i4=',0,'2025-11-20 15:26:13.802661',36),(165,'pbkdf2_sha256$1000000$vYRRO4nnpE8xn0N9Prb1Nf$0F1I6nSDjmVmWxxH+Q/xNQy2QahhwFnzx6ChBYoIlTA=',0,'2025-11-20 15:26:13.802669',36),(166,'pbkdf2_sha256$1000000$DNSs3pMfXChsmZU6rJZp9L$IiX7SujZUqVuJfUjfoOtA7yFid7+lGSeG7TFAIs5qPU=',0,'2025-11-20 15:26:13.802676',36),(167,'pbkdf2_sha256$1000000$huhFOdqZBgOfoIsZFODmwB$6njWC4qOSjUnhUDPj9Ywa5pE3YEH3GOMMYr6kuP9pSk=',0,'2025-11-20 15:26:13.802684',36),(168,'pbkdf2_sha256$1000000$KvJWFj9quJc9PUOUCpEkzZ$o1DAX4Hr12EWwlpgYcTh8/YAJyAhyys/A5mRUmLYeYQ=',0,'2025-11-20 15:26:13.802702',36),(169,'pbkdf2_sha256$1000000$f56YCEg3ivtKEV4rqWU5Iu$aba7veuPl/3SGgGYxsbVCxJlkKh0hwuEVs/LPE+ytGg=',0,'2025-11-20 15:26:13.802710',36),(170,'pbkdf2_sha256$1000000$xEERH9ALhzerx9NTK8wKJv$Wv7yuVmDTeJBxm71P8dCBIu6YRcmAlw816N3L+sniAw=',0,'2025-11-20 15:26:13.802717',36),(171,'pbkdf2_sha256$1000000$GjS5458Dz6CPHPskDCCqkA$1jtCkwhEFmcNyx1hQL/SmE8+Rd+9XAgASKJe4RFb+Hg=',0,'2025-11-25 13:38:18.130995',17),(172,'pbkdf2_sha256$1000000$n5I6x98lDZK6MWucTB5vNr$kmQfGx0bneWAXZF7oqZYqV24Zv+akba+9OCBgxzBe0g=',0,'2025-11-25 13:38:18.131023',17),(173,'pbkdf2_sha256$1000000$OSw4r6TOjXzPfHvbXFA3uF$p8lZkDJQFki91OVcpqHRYQUXc01O1j02G5WBNRzqNRc=',0,'2025-11-25 13:38:18.131034',17),(174,'pbkdf2_sha256$1000000$ej1Py56ntkZ1kqRLQrSa7e$NiVsuDL1Hd0ghooVTAKfV8vUKTilT+8dWWq7NuDM9PA=',0,'2025-11-25 13:38:18.131055',17),(175,'pbkdf2_sha256$1000000$NdPIAR13DChvpUDNklyTy2$7Uew1daKo0aYHkcmbLHOJb5+phQntTT4LN5cawXTCaQ=',0,'2025-11-25 13:38:18.131063',17),(176,'pbkdf2_sha256$1000000$2WOBYXKvtAOAB0BQ7cLX6t$ITPTCnxxil6/ZD+I+fskzCzWnHhKbyA6UU4WBMQzkws=',0,'2025-11-25 13:38:18.131071',17),(177,'pbkdf2_sha256$1000000$TYA0V0UfXWXWfuAoYPqbiv$eA7Pwq+aT8+1f10R2X3H51R4TnVXf1zv4mZfQ3lEm0A=',0,'2025-11-25 13:38:18.131079',17),(178,'pbkdf2_sha256$1000000$tiq5y9iVzFaIYtGdaoYuPD$rx0/jPlbz7W7xIzWaC7WqTweKD35oT6YS/AXbhIWXwE=',0,'2025-11-25 13:38:18.131086',17),(179,'pbkdf2_sha256$1000000$xsPxpFsgofUr3qK0WYEoq1$CYsEr0Xln2H3fSw/k67ha7N0SeTCmH/1WeZ57SCDMzs=',0,'2025-11-25 13:38:18.131093',17),(180,'pbkdf2_sha256$1000000$9aE9AnNmgMoLO5pCtS7esN$CRZZXE3Q4fdxGDiys1ha8c7274QxkHL6UTATXl3zoWE=',0,'2025-11-25 13:38:18.131101',17);
/*!40000 ALTER TABLE `accounts_backupcode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_securityconfig`
--

DROP TABLE IF EXISTS `accounts_securityconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_securityconfig` (
  `id` smallint unsigned NOT NULL,
  `enforce_2fa` tinyint(1) NOT NULL,
  `otp_digits` smallint unsigned NOT NULL,
  `otp_period` smallint unsigned NOT NULL,
  `lockout_threshold` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `accounts_securityconfig_chk_1` CHECK ((`id` >= 0)),
  CONSTRAINT `accounts_securityconfig_chk_2` CHECK ((`otp_digits` >= 0)),
  CONSTRAINT `accounts_securityconfig_chk_3` CHECK ((`otp_period` >= 0)),
  CONSTRAINT `accounts_securityconfig_chk_4` CHECK ((`lockout_threshold` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_securityconfig`
--

LOCK TABLES `accounts_securityconfig` WRITE;
/*!40000 ALTER TABLE `accounts_securityconfig` DISABLE KEYS */;
INSERT INTO `accounts_securityconfig` VALUES (1,0,6,30,5);
/*!40000 ALTER TABLE `accounts_securityconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_securitylog`
--

DROP TABLE IF EXISTS `accounts_securitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_securitylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ip` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `note` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `event` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_securitylog_user_id_6ab82c19_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_securitylog_user_id_6ab82c19_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_securitylog`
--

LOCK TABLES `accounts_securitylog` WRITE;
/*!40000 ALTER TABLE `accounts_securitylog` DISABLE KEYS */;
INSERT INTO `accounts_securitylog` VALUES (1,'127.0.0.1','Login without 2FA yet','2025-10-29 17:00:45.902726',NULL,NULL,NULL),(2,'127.0.0.1','Login without 2FA yet','2025-10-29 17:10:25.859808',NULL,NULL,NULL),(3,'127.0.0.1','Login without 2FA yet','2025-10-29 17:12:34.487062',NULL,NULL,NULL),(4,'127.0.0.1','Login without 2FA yet','2025-10-29 17:13:12.491285',NULL,NULL,NULL),(5,'127.0.0.1','Login without 2FA yet','2025-10-29 17:14:39.914767',NULL,NULL,NULL),(6,'127.0.0.1','Login without 2FA yet','2025-10-29 17:15:21.578648',NULL,NULL,NULL),(7,'127.0.0.1','Enable 2FA success','2025-10-29 17:15:43.834189',NULL,NULL,NULL),(8,'127.0.0.1','OTP ok, full login','2025-10-30 09:09:15.990959',NULL,NULL,NULL),(9,'127.0.0.1','Login without 2FA yet','2025-10-30 09:31:35.260029',NULL,NULL,NULL),(10,'127.0.0.1','Enable 2FA success','2025-10-30 09:31:50.246801',NULL,NULL,NULL),(11,'127.0.0.1','Login without 2FA yet','2025-10-30 09:42:39.311075',NULL,NULL,NULL),(12,'127.0.0.1','Login without 2FA yet','2025-10-30 09:42:55.175399',NULL,NULL,NULL),(13,'127.0.0.1','Enable 2FA success','2025-10-30 09:43:12.181090',NULL,NULL,NULL),(14,'127.0.0.1','OTP failed attempt 1','2025-10-30 09:50:28.425390',NULL,NULL,NULL),(15,'127.0.0.1','Login without 2FA yet','2025-10-30 10:03:04.060907',NULL,NULL,NULL),(16,'127.0.0.1','OTP ok, full login','2025-10-30 10:03:24.899367',NULL,NULL,NULL),(17,'127.0.0.1','Login without 2FA yet','2025-10-30 10:04:34.297259',NULL,NULL,NULL),(18,'127.0.0.1','Login without 2FA yet','2025-10-30 10:09:25.311097',NULL,NULL,NULL),(19,'127.0.0.1','OTP ok, full login','2025-10-30 10:33:02.937542',NULL,NULL,NULL),(20,'127.0.0.1','Login without 2FA yet','2025-10-30 12:51:57.795028',NULL,NULL,NULL),(21,'127.0.0.1','Login without 2FA yet','2025-10-30 12:57:18.356761',NULL,NULL,NULL),(22,'127.0.0.1','OTP ok, full login','2025-10-30 13:06:29.189617',NULL,NULL,NULL),(23,'127.0.0.1','OTP failed attempt 1','2025-10-30 13:07:16.976353',NULL,NULL,NULL),(24,'127.0.0.1','OTP failed attempt 2','2025-10-30 13:07:22.162037',NULL,NULL,NULL),(25,'127.0.0.1','OTP failed attempt 3','2025-10-30 13:07:26.637943',NULL,NULL,NULL),(26,'127.0.0.1','OTP failed attempt 4','2025-10-30 13:07:29.145378',NULL,NULL,NULL),(27,'127.0.0.1','OTP failed attempt 5 -> LOCKED','2025-10-30 13:07:30.360626',NULL,NULL,NULL),(28,'127.0.0.1','User tried while locked','2025-10-30 13:07:31.419936',NULL,NULL,NULL),(29,'127.0.0.1','OTP failed attempt 6 -> LOCKED','2025-10-30 13:08:19.473393',NULL,NULL,NULL),(30,'127.0.0.1','User tried while locked','2025-10-30 13:08:44.980732',NULL,NULL,NULL),(31,'127.0.0.1','OTP ok, full login','2025-10-30 13:09:13.062260',NULL,NULL,NULL),(32,'127.0.0.1','Login without 2FA yet','2025-10-30 13:09:49.823737',NULL,NULL,NULL),(33,'127.0.0.1','OTP ok, full login','2025-10-30 15:32:40.083286',NULL,NULL,NULL),(34,'127.0.0.1','Login without 2FA yet','2025-10-31 12:41:58.322614',NULL,NULL,NULL),(35,'127.0.0.1','OTP ok, full login','2025-10-31 12:42:56.802183',NULL,NULL,NULL),(36,'127.0.0.1','Login without 2FA yet','2025-10-31 12:43:57.410659',NULL,NULL,NULL),(37,'127.0.0.1','OTP ok, full login','2025-10-31 12:44:31.463980',NULL,NULL,NULL),(38,'127.0.0.1','OTP ok, full login','2025-10-31 12:45:46.039115',NULL,NULL,NULL),(39,'127.0.0.1','OTP ok, full login','2025-10-31 12:46:37.630822',NULL,NULL,NULL),(40,'127.0.0.1','OTP ok, full login','2025-10-31 13:51:15.342789',NULL,NULL,NULL),(41,'127.0.0.1','OTP failed attempt 1','2025-11-01 09:40:22.301762',NULL,NULL,NULL),(42,'127.0.0.1','OTP ok, full login','2025-11-01 09:40:29.849392',NULL,NULL,NULL),(43,'127.0.0.1','OTP failed attempt 1','2025-11-02 10:40:02.415315',NULL,NULL,NULL),(44,'127.0.0.1','OTP ok, full login','2025-11-02 10:40:15.516872',NULL,NULL,NULL),(45,'127.0.0.1','Login without 2FA yet','2025-11-02 10:56:17.902404',NULL,NULL,NULL),(46,'127.0.0.1','OTP failed attempt 1','2025-11-02 10:57:19.339101',NULL,NULL,NULL),(47,'127.0.0.1','OTP ok, full login','2025-11-02 10:57:23.904583',NULL,NULL,NULL),(48,'127.0.0.1','OTP failed attempt 1','2025-11-03 07:36:16.656229',NULL,NULL,NULL),(49,'127.0.0.1','OTP failed attempt 2','2025-11-03 07:36:26.210686',NULL,NULL,NULL),(50,'127.0.0.1','OTP failed attempt 3','2025-11-03 07:36:32.332304',NULL,NULL,NULL),(51,'127.0.0.1','OTP failed attempt 4','2025-11-03 07:36:38.376085',NULL,NULL,NULL),(52,'127.0.0.1','OTP failed attempt 5 -> LOCKED','2025-11-03 07:36:40.389090',NULL,NULL,NULL),(53,'127.0.0.1','User tried while locked','2025-11-03 07:36:41.201811',NULL,NULL,NULL),(54,'127.0.0.1','OTP ok, full login','2025-11-03 07:44:16.093076',NULL,NULL,NULL),(55,'127.0.0.1','OTP ok, full login','2025-11-03 08:10:02.676850',NULL,NULL,NULL),(56,'127.0.0.1','Login without 2FA yet','2025-11-03 08:11:01.871126',NULL,NULL,NULL),(57,'127.0.0.1','OTP ok, full login','2025-11-03 08:14:44.427930',NULL,NULL,NULL),(58,'127.0.0.1','OTP ok, full login','2025-11-03 08:16:15.425705',NULL,NULL,NULL),(59,'127.0.0.1','OTP ok, full login','2025-11-03 08:18:39.858287',NULL,NULL,NULL),(60,'127.0.0.1','OTP ok, full login','2025-11-03 08:26:56.012895',NULL,NULL,NULL),(61,'127.0.0.1','OTP ok, full login','2025-11-04 11:29:07.424942',NULL,NULL,NULL),(62,'127.0.0.1','OTP ok, full login','2025-11-04 11:32:09.443275',NULL,NULL,NULL),(63,'127.0.0.1','OTP failed attempt 1','2025-11-06 09:47:45.154073',NULL,NULL,NULL),(64,'127.0.0.1','OTP ok, full login','2025-11-06 09:47:53.240517',NULL,NULL,NULL),(65,'127.0.0.1','Login without 2FA yet','2025-11-06 09:52:39.930547',NULL,NULL,NULL),(66,'127.0.0.1','Login without 2FA yet','2025-11-06 09:53:45.671285',NULL,NULL,NULL),(67,'127.0.0.1','Login without 2FA yet','2025-11-06 09:55:16.506826',NULL,NULL,NULL),(68,'127.0.0.1','Login without 2FA yet','2025-11-06 09:57:29.987563',NULL,NULL,NULL),(69,'127.0.0.1','Login without 2FA yet','2025-11-06 10:12:39.221091',NULL,NULL,NULL),(70,'127.0.0.1','','2025-11-06 10:16:25.142525',NULL,NULL,NULL),(71,'127.0.0.1','OTP (Email) ok, full login','2025-11-06 10:16:33.250522',NULL,NULL,NULL),(72,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 10:17:15.557273',NULL,NULL,NULL),(73,'127.0.0.1','Backup code failed attempt 1','2025-11-06 10:18:06.464611',NULL,NULL,NULL),(74,'127.0.0.1','Login success (Backup Code)','2025-11-06 10:18:13.910789',NULL,NULL,NULL),(75,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 10:19:08.788143',NULL,NULL,NULL),(76,'127.0.0.1','OTP failed attempt 1','2025-11-06 10:20:49.823352',NULL,NULL,NULL),(77,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 10:20:58.369664',NULL,NULL,NULL),(78,'127.0.0.1','Login without 2FA yet','2025-11-06 10:35:14.412982',17,NULL,NULL),(79,'127.0.0.1','Login without 2FA yet','2025-11-06 12:41:31.947692',NULL,NULL,NULL),(80,'127.0.0.1','','2025-11-06 12:43:29.407029',NULL,NULL,NULL),(81,'127.0.0.1','OTP (Email) ok, full login','2025-11-06 12:43:44.617427',NULL,NULL,NULL),(82,'127.0.0.1','Login success (Backup Code)','2025-11-06 12:44:17.591869',NULL,NULL,NULL),(83,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:44:54.166538',NULL,NULL,NULL),(84,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:46:21.224805',NULL,NULL,NULL),(85,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:46:42.885256',NULL,NULL,NULL),(86,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:47:03.456210',NULL,NULL,NULL),(87,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:48:11.984165',NULL,NULL,NULL),(88,'127.0.0.1','','2025-11-09 07:58:20.828375',17,NULL,NULL),(89,'127.0.0.1','OTP (Email) ok, full login','2025-11-09 07:58:30.176836',17,NULL,NULL),(90,'127.0.0.1','Login without 2FA yet','2025-11-09 09:32:47.991453',NULL,NULL,NULL),(91,'127.0.0.1','','2025-11-09 09:35:10.992001',NULL,NULL,NULL),(92,'127.0.0.1','OTP (Email) ok, full login','2025-11-09 09:35:19.242055',NULL,NULL,NULL),(93,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-09 09:39:22.331538',NULL,NULL,NULL),(94,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-10 08:42:11.021345',17,NULL,NULL),(95,'127.0.0.1','OTP failed attempt 1','2025-11-10 08:55:56.838743',NULL,NULL,NULL),(96,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-10 08:56:05.649104',NULL,NULL,NULL),(97,'127.0.0.1','','2025-11-10 09:24:22.206532',17,NULL,NULL),(98,'127.0.0.1','OTP (Email) ok, full login','2025-11-10 09:24:32.445453',17,NULL,NULL),(99,'127.0.0.1','','2025-11-10 09:25:54.564022',NULL,NULL,NULL),(100,'127.0.0.1','OTP (Email) ok, full login','2025-11-10 09:26:05.009357',NULL,NULL,NULL),(101,'127.0.0.1','','2025-11-10 09:26:43.743879',NULL,NULL,NULL),(102,'127.0.0.1','OTP (Email) ok, full login','2025-11-10 09:26:52.840512',NULL,NULL,NULL),(103,'127.0.0.1','','2025-11-10 10:59:55.919529',17,NULL,NULL),(104,'127.0.0.1','OTP (Email) ok, full login','2025-11-10 11:00:06.356970',17,NULL,NULL),(105,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-10 11:11:47.731994',NULL,NULL,NULL),(106,'127.0.0.1','','2025-11-10 11:38:17.559663',17,NULL,NULL),(107,'127.0.0.1','OTP (Email) ok, full login','2025-11-10 11:38:28.736659',17,NULL,NULL),(108,'127.0.0.1','','2025-11-10 11:42:12.448951',17,NULL,NULL),(109,'127.0.0.1','OTP (Email) ok, full login','2025-11-10 11:42:18.349026',17,NULL,NULL),(110,'127.0.0.1','','2025-11-10 15:27:05.583044',17,NULL,NULL),(111,'127.0.0.1','OTP (Email) ok, full login','2025-11-10 15:27:17.578658',17,NULL,NULL),(112,'127.0.0.1','','2025-11-11 11:18:22.951755',17,NULL,NULL),(113,'127.0.0.1','OTP (Email) ok, full login','2025-11-11 11:18:30.633598',17,NULL,NULL),(114,'127.0.0.1','Login without 2FA yet','2025-11-11 11:47:56.953170',NULL,'LOGIN_SUCCESS',NULL),(115,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-11 11:48:30.348859',NULL,'ENABLE_2FA',NULL),(116,'127.0.0.1','Login without 2FA yet','2025-11-11 12:41:40.786414',16,'LOGIN_SUCCESS',NULL),(117,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-11 12:41:59.797075',16,'ENABLE_2FA',NULL),(118,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-11 12:42:08.082781',16,'ENABLE_2FA',NULL),(119,'127.0.0.1','','2025-11-11 12:58:32.365650',16,'EMAIL_OTP_SENT',NULL),(120,'127.0.0.1','OTP (Email) ok, full login','2025-11-11 12:59:05.563779',16,'OTP_SUCCESS',NULL),(121,'127.0.0.1','Login without 2FA yet','2025-11-11 12:59:30.360504',22,'LOGIN_SUCCESS',NULL),(122,'127.0.0.1','','2025-11-12 18:07:03.396859',16,'EMAIL_OTP_SENT',NULL),(123,'127.0.0.1','OTP (Email) ok, full login','2025-11-12 18:07:16.632277',16,'OTP_SUCCESS',NULL),(124,'127.0.0.1','Login without 2FA yet','2025-11-12 18:11:04.688457',NULL,'LOGIN_SUCCESS',NULL),(125,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-12 18:12:19.437673',NULL,'ENABLE_2FA',NULL),(126,'127.0.0.1','Login without 2FA yet','2025-11-12 18:17:07.616430',NULL,'LOGIN_SUCCESS',NULL),(127,'127.0.0.1','Login without 2FA yet','2025-11-13 08:52:28.458474',NULL,'LOGIN_SUCCESS',NULL),(128,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-13 08:55:34.064514',NULL,'ENABLE_2FA',NULL),(129,'127.0.0.1','OTP failed attempt 1','2025-11-13 08:58:56.914079',NULL,'OTP_FAIL',NULL),(130,'127.0.0.1','','2025-11-13 09:00:02.865822',NULL,'EMAIL_OTP_SENT',NULL),(131,'127.0.0.1','OTP (Email) ok, full login','2025-11-13 09:00:45.030899',NULL,'OTP_SUCCESS',NULL),(132,'127.0.0.1','Login success (Backup Code)','2025-11-13 09:01:32.593633',NULL,'BACKUP_CODE_USED',NULL),(133,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-13 09:25:08.056999',NULL,'OTP_SUCCESS',NULL),(134,'127.0.0.1','OTP failed attempt 1','2025-11-13 09:41:33.467104',NULL,'OTP_FAIL',NULL),(135,'127.0.0.1','OTP failed attempt 2','2025-11-13 09:41:39.355155',NULL,'OTP_FAIL',NULL),(136,'127.0.0.1','OTP failed attempt 3','2025-11-13 09:41:40.236247',NULL,'OTP_FAIL',NULL),(137,'127.0.0.1','OTP failed attempt 4','2025-11-13 09:41:41.023496',NULL,'OTP_FAIL',NULL),(138,'127.0.0.1','OTP failed attempt 5 -> LOCKED','2025-11-13 09:41:41.695555',NULL,'OTP_FAIL',NULL),(139,'127.0.0.1','User tried while locked','2025-11-13 09:45:46.262821',NULL,'OTP_LOCKED',NULL),(140,'127.0.0.1','Login without 2FA yet','2025-11-13 12:41:25.869380',NULL,'LOGIN_SUCCESS',NULL),(141,'127.0.0.1','Login without 2FA yet','2025-11-13 12:42:29.051460',NULL,'LOGIN_SUCCESS',NULL),(142,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-13 12:43:10.397247',NULL,'ENABLE_2FA',NULL),(143,'127.0.0.1','User disabled 2FA (self)','2025-11-13 12:43:50.706892',NULL,'DISABLE_2FA',NULL),(144,'127.0.0.1','Login without 2FA yet','2025-11-13 15:38:07.509497',NULL,'LOGIN_SUCCESS',NULL),(145,'127.0.0.1','Login without 2FA yet','2025-11-14 16:21:51.820932',NULL,'LOGIN_SUCCESS',NULL),(146,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-14 16:24:43.107703',NULL,'ENABLE_2FA',NULL),(147,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-14 16:39:57.417248',NULL,'OTP_SUCCESS',NULL),(148,'127.0.0.1','OTP failed attempt 1','2025-11-16 09:40:41.136480',17,'OTP_FAIL',NULL),(149,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-16 09:41:02.777633',17,'OTP_SUCCESS',NULL),(150,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-16 09:42:34.947433',17,'OTP_SUCCESS',NULL),(151,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-16 09:52:51.482807',17,'OTP_SUCCESS',NULL),(152,'127.0.0.1','Login success (Trusted Device, User Matched)','2025-11-16 09:54:41.552328',17,'LOGIN_SUCCESS',NULL),(153,'127.0.0.1','OTP failed attempt 1','2025-11-16 09:59:58.181085',NULL,'OTP_FAIL',NULL),(154,'127.0.0.1','OTP failed attempt 2','2025-11-16 10:00:05.693507',NULL,'OTP_FAIL',NULL),(155,'127.0.0.1','OTP failed attempt 3','2025-11-16 10:00:07.515444',NULL,'OTP_FAIL',NULL),(156,'127.0.0.1','OTP failed attempt 4','2025-11-16 10:00:28.399488',NULL,'OTP_FAIL',NULL),(157,'127.0.0.1','OTP failed attempt 5 -> LOCKED','2025-11-16 10:00:29.788057',NULL,'OTP_FAIL',NULL),(158,'127.0.0.1','OTP failed attempt 1','2025-11-16 10:01:21.111761',17,'OTP_FAIL',NULL),(159,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-16 10:01:49.583126',17,'OTP_SUCCESS',NULL),(160,'127.0.0.1','Login without 2FA yet','2025-11-16 10:10:23.838519',NULL,'LOGIN_SUCCESS',NULL),(161,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-16 10:10:45.864984',NULL,'ENABLE_2FA',NULL),(162,'127.0.0.1','User disabled 2FA (self)','2025-11-16 10:30:21.893423',NULL,'DISABLE_2FA',NULL),(163,'127.0.0.1','Login without 2FA yet','2025-11-17 10:55:45.740132',NULL,'LOGIN_SUCCESS',NULL),(164,'127.0.0.1','Login without 2FA yet','2025-11-17 11:06:38.322983',NULL,'LOGIN_SUCCESS',NULL),(165,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-17 11:11:10.909626',NULL,'ENABLE_2FA',NULL),(166,'127.0.0.1','Login without 2FA yet','2025-11-17 11:19:14.382763',31,'LOGIN_SUCCESS',NULL),(167,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-17 11:19:32.075200',31,'ENABLE_2FA',NULL),(168,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-17 13:47:16.579714',31,'OTP_SUCCESS',NULL),(169,'127.0.0.1','Login without 2FA yet','2025-11-18 09:55:33.391084',NULL,'LOGIN_SUCCESS',NULL),(170,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-18 09:56:14.013086',NULL,'ENABLE_2FA',NULL),(171,'127.0.0.1','Login without 2FA yet','2025-11-20 15:25:06.686119',36,'LOGIN_SUCCESS',NULL),(172,'127.0.0.1','User enabled 2FA (TOTP)','2025-11-20 15:26:06.700534',36,'ENABLE_2FA',NULL),(173,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-20 15:27:14.035546',36,'OTP_SUCCESS',NULL),(174,'127.0.0.1','OTP failed attempt 1','2025-11-20 15:27:31.832534',36,'OTP_FAIL',NULL),(175,'127.0.0.1','OTP failed attempt 1','2025-11-24 10:14:55.115326',17,'OTP_FAIL',NULL),(176,'127.0.0.1','','2025-11-24 10:15:09.877945',17,'EMAIL_OTP_SENT',NULL),(177,'127.0.0.1','OTP (Email) ok, full login','2025-11-24 10:15:25.347363',17,'OTP_SUCCESS',NULL),(178,'127.0.0.1','OTP failed attempt 1','2025-11-24 10:15:58.827528',17,'OTP_FAIL',NULL),(179,'127.0.0.1','OTP failed attempt 2','2025-11-24 10:16:43.973539',17,'OTP_FAIL',NULL),(180,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-24 10:16:57.605831',17,'OTP_SUCCESS',NULL),(181,'127.0.0.1','OTP failed attempt 1','2025-11-25 12:34:24.131828',17,'OTP_FAIL',NULL),(182,'127.0.0.1','OTP failed attempt 2','2025-11-25 12:38:40.092877',17,'OTP_FAIL',NULL),(183,'127.0.0.1','OTP failed attempt 3','2025-11-25 12:39:30.144367',17,'OTP_FAIL',NULL),(184,'127.0.0.1','OTP failed attempt 4','2025-11-25 12:42:08.871630',17,'OTP_FAIL',NULL),(185,'127.0.0.1','OTP failed attempt 5 -> LOCKED','2025-11-25 12:47:27.618486',17,'OTP_FAIL',NULL),(186,'127.0.0.1','User tried while locked','2025-11-25 12:47:48.817105',17,'OTP_LOCKED',NULL),(187,'127.0.0.1','User tried while locked','2025-11-25 12:47:50.546281',17,'OTP_LOCKED',NULL),(188,'127.0.0.1','OTP failed attempt 6 -> LOCKED','2025-11-25 12:49:30.468472',17,'OTP_FAIL',NULL),(189,'127.0.0.1','User tried while locked','2025-11-25 12:49:32.024875',17,'OTP_LOCKED',NULL),(190,'127.0.0.1','User tried while locked','2025-11-25 12:49:36.074909',17,'OTP_LOCKED',NULL),(191,'127.0.0.1','User tried while locked','2025-11-25 12:49:41.452899',17,'OTP_LOCKED',NULL),(192,'127.0.0.1','OTP failed attempt 7 -> LOCKED','2025-11-25 12:50:21.201163',17,'OTP_FAIL',NULL),(193,'127.0.0.1','User tried while locked','2025-11-25 12:57:52.816825',17,'OTP_LOCKED',NULL),(194,'127.0.0.1','OTP (TOTP) ok, full login','2025-11-25 12:59:31.322888',17,'OTP_SUCCESS',NULL),(195,'127.0.0.1','Login without 2FA yet','2025-11-25 13:00:20.353982',17,'LOGIN_SUCCESS',NULL),(196,'127.0.0.1','Login without 2FA yet','2025-11-25 13:28:44.717583',17,'LOGIN_SUCCESS','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'),(197,'171.233.146.224','Login without 2FA yet','2025-11-25 13:36:27.326928',17,'LOGIN_SUCCESS',NULL),(198,'171.233.146.224','User enabled 2FA (TOTP)','2025-11-25 13:38:11.042321',17,'ENABLE_2FA',NULL),(199,'171.233.146.224','OTP failed attempt 1','2025-11-25 13:39:09.116015',17,'OTP_FAIL',NULL),(200,'171.233.146.224','OTP failed attempt 2','2025-11-25 13:39:10.475205',17,'OTP_FAIL',NULL),(201,'171.233.146.224','OTP failed attempt 3','2025-11-25 13:39:11.295351',17,'OTP_FAIL',NULL),(202,'171.233.146.224','OTP failed attempt 4','2025-11-25 13:39:12.127501',17,'OTP_FAIL',NULL),(203,'171.233.146.224','OTP failed attempt 5 -> LOCKED','2025-11-25 13:40:18.973867',17,'OTP_FAIL',NULL),(204,'171.233.146.224','User tried while locked','2025-11-25 13:40:23.897784',17,'OTP_LOCKED',NULL),(205,'171.233.146.224','User tried while locked','2025-11-25 13:40:24.054265',17,'OTP_LOCKED',NULL),(206,'171.233.146.224','User tried while locked','2025-11-25 13:41:17.981259',17,'OTP_LOCKED',NULL),(207,'171.233.146.224','User tried while locked','2025-11-25 13:41:19.054468',17,'OTP_LOCKED',NULL),(208,'171.233.146.224','User tried while locked','2025-11-25 13:41:21.357588',17,'OTP_LOCKED',NULL),(209,'171.233.146.224','User tried while locked','2025-11-25 13:41:24.574524',17,'OTP_LOCKED',NULL),(210,'171.233.146.224','User tried while locked','2025-11-25 13:41:26.910913',17,'OTP_LOCKED',NULL),(211,'104.28.119.143','User tried while locked','2025-11-25 13:56:11.751335',17,'OTP_LOCKED',NULL),(212,'104.28.119.143','OTP failed attempt 6 -> LOCKED','2025-11-25 13:56:45.123539',17,'OTP_FAIL',NULL),(213,'104.28.119.143','User tried while locked','2025-11-25 13:56:56.161295',17,'OTP_LOCKED',NULL),(214,'104.28.119.143','OTP (TOTP) ok, full login','2025-11-25 13:57:23.247955',17,'OTP_SUCCESS',NULL),(215,'171.233.146.224','OTP (TOTP) ok, full login','2025-11-27 11:02:01.541236',17,'OTP_SUCCESS',NULL),(216,'171.233.146.224','OTP (TOTP) ok, full login','2025-11-30 06:42:57.793895',17,'OTP_SUCCESS',NULL);
/*!40000 ALTER TABLE `accounts_securitylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_securitypolicy`
--

DROP TABLE IF EXISTS `accounts_securitypolicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_securitypolicy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `require_2fa_for_new_users` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_securitypolicy`
--

LOCK TABLES `accounts_securitypolicy` WRITE;
/*!40000 ALTER TABLE `accounts_securitypolicy` DISABLE KEYS */;
INSERT INTO `accounts_securitypolicy` VALUES (8,1,'2025-11-14 16:19:39.822577');
/*!40000 ALTER TABLE `accounts_securitypolicy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified` tinyint(1) NOT NULL,
  `otp_secret` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_2fa_enabled` tinyint(1) NOT NULL,
  `must_setup_2fa` tinyint(1) NOT NULL,
  `failed_otp_attempts` int NOT NULL,
  `must_change_password` tinyint(1) NOT NULL,
  `otp_locked` tinyint(1) NOT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `accounts_user_email_b2644a56_uniq` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1000000$JhDklB2XWM4vYc3Q7p5rIr$M1T7qHKHK0dJ9/oOhnnTUlnTe4MObRdz+9hluFkrQmY=','2025-11-06 09:53:05.610775',1,'admin','','','chaunhathoa@gmail.com',1,1,'2025-10-29 16:41:09.000000','USER',0,'WN66VVBF4QOQSCZNEA5EJECVQ6WPVI4R',0,1,0,0,0,'avatars/default.png',NULL),(16,'pbkdf2_sha256$1000000$G46uO4We84yZ4XW5fywuhK$8uqEnalLjV8vVLzCIm5WvLXngpKhPXb7BvZY0oF0jmw=','2025-11-25 12:48:15.443998',1,'admin1','','','hoa@gmail.com',1,1,'2025-11-06 10:25:02.000000','ADMIN',1,'27CKYLWDCK4KOVNU3XC3SD6VLWD22YN3',1,0,0,0,0,'avatars/default.png',NULL),(17,'pbkdf2_sha256$1000000$7HR5XFtndOxrmwPbQmy4uc$7vhFPcAP6JSHs4zh1INwCJTh+gOMX4Gpq2ETi02Lt0s=','2025-11-30 06:42:57.824045',0,'hoa','','','chaunhathoa24102004@gmail.com',1,1,'2025-11-06 10:34:30.000000','STAFF',1,'PGEODJCVWN7BKIE4EEDBGCBSMSNUWMQM',1,0,0,0,0,'avatars/vietnam-war-alone-at-the-edge-of-the-universe.gif',''),(22,'pbkdf2_sha256$1000000$Igp9vjAZfn3suJroslIpSt$Rnai+e71iFHSe0aBSQZBc9KX/8mPwS3w4BtneiVfPfs=','2025-11-11 12:59:30.379777',0,'demo','','','quinzohartejk@hotmail.com',0,1,'2025-11-11 12:57:22.526048','USER',1,NULL,0,0,0,0,0,'avatars/449805471_1158886545170935_2089116230720232296_n.jpg','hi'),(31,'pbkdf2_sha256$1000000$UyaoQvZYuV850FXp4MGlLb$tmqUzXBZf7LL+al0oytsoMyDzTA3PIM5Uz3Nec9GlA4=','2025-11-17 13:47:16.608461',0,'demon1','','','demo@example.com',0,1,'2025-11-17 11:18:58.454620','USER',1,'OCWXEXDLCBGU4JROTWWNTW33PTTEWYC7',1,0,0,0,0,'avatars/default.png',NULL),(33,'pbkdf2_sha256$1000000$sacjV5uxdfMJA3xkb0vWFk$R0AnngFEgoM6/vT7Q9gcOfRVPFddSygJGyAskmxVQPc=',NULL,0,'nhathoa','','','hoa12231243@gmail.com',0,0,'2025-11-18 09:37:23.991681','USER',0,NULL,0,1,0,0,0,'avatars/default.png',NULL),(34,'pbkdf2_sha256$1000000$rsTpsgO3bjjQdsNTqgjhhF$zbbnxSglTbOfJ2kuyTjZVq8xq8oFCS3FVuEWkX7CTD0=',NULL,0,'demo3','','','dfshsdfh@gmail.com',0,0,'2025-11-18 09:50:15.000000','USER',1,NULL,0,1,0,0,0,'avatars/default.png',''),(36,'pbkdf2_sha256$1000000$wyTSFYwAEL7fsMCcVyKheQ$zBlGvvZIzSmr/Yl2nZ549mhE26UkariTT3OZo1Qm8hI=','2025-11-20 15:27:14.062591',0,'DinhQuoc','','','chauminhhai458@gmail.com',0,1,'2025-11-20 15:24:35.000000','USER',1,'ITQYS23JNJ63KSFEITQVX5PJ7K3ZDILN',1,0,1,0,0,'avatars/default.png','');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
INSERT INTO `accounts_user_user_permissions` VALUES (13,17,16),(1,17,33),(2,17,34),(3,17,35),(4,17,36),(5,17,37),(6,17,38),(7,17,39),(8,17,40),(9,17,41),(10,17,42),(11,17,43),(12,17,44);
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add security policy',7,'add_securitypolicy'),(26,'Can change security policy',7,'change_securitypolicy'),(27,'Can delete security policy',7,'delete_securitypolicy'),(28,'Can view security policy',7,'view_securitypolicy'),(29,'Can add security log',8,'add_securitylog'),(30,'Can change security log',8,'change_securitylog'),(31,'Can delete security log',8,'delete_securitylog'),(32,'Can view security log',8,'view_securitylog'),(33,'Can add category',9,'add_category'),(34,'Can change category',9,'change_category'),(35,'Can delete category',9,'delete_category'),(36,'Can view category',9,'view_category'),(37,'Can add thread',10,'add_thread'),(38,'Can change thread',10,'change_thread'),(39,'Can delete thread',10,'delete_thread'),(40,'Can view thread',10,'view_thread'),(41,'Can add post',11,'add_post'),(42,'Can change post',11,'change_post'),(43,'Can delete post',11,'delete_post'),(44,'Can view post',11,'view_post'),(45,'Can add security config',12,'add_securityconfig'),(46,'Can change security config',12,'change_securityconfig'),(47,'Can delete security config',12,'delete_securityconfig'),(48,'Can view security config',12,'view_securityconfig'),(49,'Can add backup code',13,'add_backupcode'),(50,'Can change backup code',13,'change_backupcode'),(51,'Can delete backup code',13,'delete_backupcode'),(52,'Can view backup code',13,'view_backupcode');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cache_table_ratelimit`
--

DROP TABLE IF EXISTS `cache_table_ratelimit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cache_table_ratelimit` (
  `cache_key` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  PRIMARY KEY (`cache_key`),
  KEY `cache_table_ratelimit_expires` (`expires`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cache_table_ratelimit`
--

LOCK TABLES `cache_table_ratelimit` WRITE;
/*!40000 ALTER TABLE `cache_table_ratelimit` DISABLE KEYS */;
/*!40000 ALTER TABLE `cache_table_ratelimit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-10-29 16:57:22.863471','1','buổi sáng tốt lành',1,'[{\"added\": {}}]',9,1),(2,'2025-10-29 16:57:55.817627','1','ăn sáng ở đâu',1,'[{\"added\": {}}]',10,1),(3,'2025-10-29 16:58:23.508840','1','Post by admin on ăn sáng ở đâu',1,'[{\"added\": {}}]',11,1),(4,'2025-10-30 09:30:31.267180','2','hoa',3,'',6,1),(5,'2025-10-30 09:41:40.160711','1','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(6,'2025-10-30 09:46:18.547509','2','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(7,'2025-10-30 09:46:40.126376','4','hai',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\"]}}]',6,1),(8,'2025-10-30 09:49:34.771681','4','hai',3,'',6,1),(9,'2025-10-30 09:49:50.456381','3','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(10,'2025-10-30 09:50:09.596869','4','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(11,'2025-10-30 09:50:12.752490','4','Chính sách bảo mật hệ thống',2,'[]',7,1),(12,'2025-10-30 09:53:18.796917','5','hai',3,'',6,1),(13,'2025-10-30 10:02:21.416490','5','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(14,'2025-10-30 12:53:38.606268','3','Post by DinhQuoc on ăn sáng ở đâu',2,'[{\"changed\": {\"fields\": [\"Content\"]}}]',11,1),(15,'2025-10-30 12:54:05.945531','3','Post by DinhQuoc on ăn sáng ở đâu',3,'',11,1),(16,'2025-10-30 13:08:13.476939','7','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Otp locked\"]}}]',6,1),(17,'2025-10-30 13:09:00.389491','7','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Otp locked\"]}}]',6,1),(18,'2025-10-30 13:09:31.637641','7','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',6,1),(19,'2025-10-30 13:09:46.827284','7','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\"]}}]',6,1),(20,'2025-10-31 12:20:23.463654','6','hai',3,'',6,1),(21,'2025-10-31 12:43:44.865755','9','hai',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\", \"Must setup 2fa\"]}}]',6,1),(22,'2025-11-02 10:55:01.015512','7','DinhQuoc',3,'',6,1),(23,'2025-11-02 10:55:07.163015','8','MinhQuan',3,'',6,1),(24,'2025-11-03 07:43:35.372700','10','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Otp locked\", \"Must change password\"]}}]',6,1),(25,'2025-11-03 07:45:14.234891','10','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\", \"Must setup 2fa\"]}}]',6,1),(26,'2025-11-03 08:16:09.463573','6','Post by admin on ăn sáng ở đâu',3,'',11,1),(27,'2025-11-03 08:18:20.998374','7','Post by DinhQuoc on ăn sáng ở đâu',3,'',11,1),(28,'2025-11-03 08:30:28.560315','8','Post by hoa on ăn sáng ở đâu',3,'',11,1),(29,'2025-11-06 09:48:38.175532','3','hoa',3,'',6,1),(30,'2025-11-06 09:49:48.055282','1','admin',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',6,1),(31,'2025-11-06 09:50:56.991973','6','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(32,'2025-11-06 09:51:24.658522','11','hoa',3,'',6,1),(33,'2025-11-06 09:53:12.308277','6','Chính sách bảo mật hệ thống',2,'[]',7,1),(34,'2025-11-06 09:54:04.881643','7','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(35,'2025-11-06 09:54:33.218921','12','hoa',3,'',6,1),(36,'2025-11-06 09:55:57.728534','5','Chính sách bảo mật hệ thống',3,'',7,1),(37,'2025-11-06 09:55:57.728577','4','Chính sách bảo mật hệ thống',3,'',7,1),(38,'2025-11-06 09:55:57.728593','3','Chính sách bảo mật hệ thống',3,'',7,1),(39,'2025-11-06 09:55:57.728606','2','Chính sách bảo mật hệ thống',3,'',7,1),(40,'2025-11-06 09:55:57.728619','1','Chính sách bảo mật hệ thống',3,'',7,1),(41,'2025-11-06 09:56:05.036667','7','Chính sách bảo mật hệ thống',3,'',7,1),(42,'2025-11-06 09:56:05.036710','6','Chính sách bảo mật hệ thống',3,'',7,1),(43,'2025-11-06 09:56:08.573818','8','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(44,'2025-11-06 09:56:11.997564','8','Chính sách bảo mật hệ thống',2,'[]',7,1),(45,'2025-11-06 09:56:37.439124','13','hoa',3,'',6,1),(46,'2025-11-06 09:56:57.503561','14','hoa',1,'[{\"added\": {}}]',6,1),(47,'2025-11-06 09:57:09.264476','14','hoa',2,'[{\"changed\": {\"fields\": [\"Email verified\"]}}]',6,1),(48,'2025-11-06 10:11:49.876330','14','hoa',3,'',6,1),(49,'2025-11-06 10:33:03.119120','15','hoa',3,'',6,16),(50,'2025-11-06 12:39:38.720888','10','DinhQuoc',3,'',6,16),(51,'2025-11-09 09:28:21.837721','9','hai',3,'',6,16),(52,'2025-11-10 08:47:03.718005','17','hoa',2,'[{\"changed\": {\"fields\": [\"Role\", \"Staff status\", \"User permissions\"]}}]',6,16),(53,'2025-11-10 08:48:21.209576','2','gà gáy',1,'[{\"added\": {}}]',9,17),(54,'2025-11-10 08:48:47.464217','2','gà serema',1,'[{\"added\": {}}]',10,17),(55,'2025-11-11 11:46:55.601158','19','hai',3,'',6,16),(56,'2025-11-11 12:05:29.987740','16','admin1',2,'[{\"changed\": {\"fields\": [\"Email verified\"]}}]',6,16),(57,'2025-11-11 12:05:43.865459','16','admin1',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',6,16),(58,'2025-11-11 12:49:12.539260','21','demon',1,'[{\"added\": {}}]',6,16),(59,'2025-11-11 12:56:12.940251','8','Chính sách bảo mật hệ thống',2,'[{\"changed\": {\"fields\": [\"Require 2fa for new users\"]}}]',7,16),(60,'2025-11-11 12:56:48.138388','21','demon',3,'',6,16),(61,'2025-11-11 12:57:23.242245','22','demo',1,'[{\"added\": {}}]',6,16),(62,'2025-11-12 18:10:59.467202','20','hai',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\"]}}]',6,16),(63,'2025-11-12 18:16:04.548878','1','Security Config (global)',2,'[{\"changed\": {\"fields\": [\"Enforce 2fa\"]}}]',12,16),(64,'2025-11-12 18:16:21.465875','20','hai',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\"]}}]',6,16),(65,'2025-11-12 18:16:49.664066','1','Security Config (global)',2,'[{\"changed\": {\"fields\": [\"Enforce 2fa\"]}}]',12,16),(66,'2025-11-13 08:45:43.214153','18','DinhQuoc',3,'',6,16),(67,'2025-11-14 16:19:28.222126','20','hai',3,'',6,16),(68,'2025-11-14 16:19:39.823578','8','Chính sách bảo mật hệ thống',2,'[{\"changed\": {\"fields\": [\"Require 2fa for new users\"]}}]',7,16),(69,'2025-11-16 10:03:24.813042','25','demonone',2,'[{\"changed\": {\"fields\": [\"Email verified\"]}}]',6,16),(70,'2025-11-16 10:09:48.670141','25','demonone',3,'',6,16),(71,'2025-11-16 10:09:48.670184','24','hai',3,'',6,16),(72,'2025-11-16 10:10:08.035761','26','hai',1,'[{\"added\": {}}]',6,16),(73,'2025-11-17 10:55:12.951013','27','demon123',3,'',6,16),(74,'2025-11-17 10:55:12.951067','28','fsdfsdfsdsd',3,'',6,16),(75,'2025-11-17 10:55:32.933855','29','demon1',1,'[{\"added\": {}}]',6,16),(76,'2025-11-17 11:17:44.719595','29','demon1',3,'',6,16),(77,'2025-11-17 11:18:05.739995','30','demon1',1,'[{\"added\": {}}]',6,16),(78,'2025-11-17 11:18:38.914144','30','demon1',3,'',6,16),(79,'2025-11-17 11:18:59.210060','31','demon1',1,'[{\"added\": {}}]',6,16),(80,'2025-11-18 09:35:36.776467','32','nhathoa',2,'[{\"changed\": {\"fields\": [\"Email verified\"]}}]',6,16),(81,'2025-11-18 09:36:15.926426','32','nhathoa',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',6,16),(82,'2025-11-18 09:36:38.811447','32','nhathoa',3,'',6,16),(83,'2025-11-18 09:50:57.534239','34','demo3',2,'[{\"changed\": {\"fields\": [\"Email verified\"]}}]',6,16),(84,'2025-11-18 09:53:58.088221','26','hai',3,'',6,16),(85,'2025-11-20 15:20:55.729386','35','hai',3,'',6,16),(86,'2025-11-20 15:21:19.594108','23','DinhQuoc',3,'',6,16),(87,'2025-11-20 15:24:59.426644','36','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Active\", \"Email verified\"]}}]',6,16),(88,'2025-11-25 12:48:29.332126','17','hoa',2,'[{\"changed\": {\"fields\": [\"Otp locked\"]}}]',6,16),(89,'2025-11-25 12:48:53.476739','1','Security Config (global)',2,'[{\"changed\": {\"fields\": [\"Lockout threshold\"]}}]',12,16),(90,'2025-11-25 12:49:56.329420','17','hoa',2,'[{\"changed\": {\"fields\": [\"Otp locked\"]}}]',6,16),(91,'2025-11-25 12:58:18.205536','1','Security Config (global)',2,'[{\"changed\": {\"fields\": [\"Lockout threshold\"]}}]',12,16),(92,'2025-11-25 12:58:58.642454','17','hoa',2,'[{\"changed\": {\"fields\": [\"Failed otp attempts\", \"Otp locked\"]}}]',6,16),(93,'2025-11-25 13:00:07.313280','17','hoa',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\"]}}]',6,16),(94,'2025-11-25 13:56:25.828914','17','hoa',2,'[{\"changed\": {\"fields\": [\"Otp locked\"]}}]',6,16),(95,'2025-11-25 13:57:06.435892','17','hoa',2,'[{\"changed\": {\"fields\": [\"Otp locked\"]}}]',6,16);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (13,'accounts','backupcode'),(12,'accounts','securityconfig'),(8,'accounts','securitylog'),(7,'accounts','securitypolicy'),(6,'accounts','user'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(9,'forum','category'),(11,'forum','post'),(10,'forum','thread'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-29 16:39:25.080621'),(2,'contenttypes','0002_remove_content_type_name','2025-10-29 16:39:25.275546'),(3,'auth','0001_initial','2025-10-29 16:39:25.888737'),(4,'auth','0002_alter_permission_name_max_length','2025-10-29 16:39:26.021310'),(5,'auth','0003_alter_user_email_max_length','2025-10-29 16:39:26.033217'),(6,'auth','0004_alter_user_username_opts','2025-10-29 16:39:26.043715'),(7,'auth','0005_alter_user_last_login_null','2025-10-29 16:39:26.054363'),(8,'auth','0006_require_contenttypes_0002','2025-10-29 16:39:26.061184'),(9,'auth','0007_alter_validators_add_error_messages','2025-10-29 16:39:26.071937'),(10,'auth','0008_alter_user_username_max_length','2025-10-29 16:39:26.082924'),(11,'auth','0009_alter_user_last_name_max_length','2025-10-29 16:39:26.093651'),(12,'auth','0010_alter_group_name_max_length','2025-10-29 16:39:26.118635'),(13,'auth','0011_update_proxy_permissions','2025-10-29 16:39:26.130188'),(14,'auth','0012_alter_user_first_name_max_length','2025-10-29 16:39:26.140494'),(15,'accounts','0001_initial','2025-10-29 16:39:26.856063'),(16,'accounts','0002_user_must_setup_2fa','2025-10-29 16:39:26.977254'),(17,'accounts','0003_securitypolicy','2025-10-29 16:39:27.032884'),(18,'accounts','0004_user_failed_otp_attempts_user_must_change_password_and_more','2025-10-29 16:39:27.569747'),(19,'admin','0001_initial','2025-10-29 16:39:27.876774'),(20,'admin','0002_logentry_remove_auto_add','2025-10-29 16:39:27.890235'),(21,'admin','0003_logentry_add_action_flag_choices','2025-10-29 16:39:27.905311'),(22,'forum','0001_initial','2025-10-29 16:39:28.568907'),(23,'sessions','0001_initial','2025-10-29 16:39:28.658457'),(24,'accounts','0005_securityconfig','2025-10-30 09:37:05.581094'),(25,'accounts','0006_alter_user_email','2025-10-30 09:58:34.471035'),(26,'accounts','0007_alter_securitylog_event_backupcode','2025-11-06 10:10:38.831593'),(27,'accounts','0008_user_avatar_user_bio','2025-11-10 08:40:21.228437'),(28,'forum','0002_post_likes','2025-11-10 11:37:51.604178'),(29,'accounts','0009_remove_securitylog_event_securitylog_event_type','2025-11-11 11:40:53.977575'),(30,'accounts','0010_securitylog_user_agent','2025-11-25 13:25:51.796714');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('00o63x29scl53rem8o8f61f6leed6n64','.eJxVjMEOgyAQBf-Fc2NE0QWPvfcbyAJLpbVgBJM2Tf-9mnjxOjPvfdmEuWh6YZh0KrPOFAsbOPQNCCVUd2EbyjmkqOk9h-XDhnpjuJZRr5kWHRwbGAd2ggbtk-Ju3APjPVU2xbIEU-1Jddhc3ZKj6Xq0p4MR87ithXQk0daudbJHC8arzqIn7JoOyQB3greAIBul-toDb6USXHHve6cADfv9AStbSmU:1vIJfg:t76ToKh3omMuFBpJsZQZF_amqoIcSrPuII_-nWfQZmA','2025-12-10 11:38:28.774430'),('0wy5vml0mhh1z1jmqkuf557zp1wpce9o','.eJxVjMsKwjAURP8l6xKaNE-X7v2GkMetjUoiSQqK-O-mUJDuhnNm5oNMhVpjTgZez1je6KQEG8cB0dmaVtbaIKBTD3BAZq1QTOxqIgMydm3LH6GJoAN01t8hbSbcbLpm7HNqJTq8VfBuK77kAI_z3j0cLLYufU2Yc9IxyrXQXGsqrVcz40ROllPRpZ6UVE4GxTUTo1RaKMcEWKYo57NH3x_wR05R:1vKt1A:D_UJn3IBFRBwiHdUqg7yrt_v-8P0KiXnLoUOB50Q3sM','2025-11-18 13:47:16.616272'),('0zg7t0y4q8230er27baoyhnuk4opied9','.eJxVjDkOwjAUBe_iGiL_ONgxJT1nsP5mwqIYxUGAEHcnSDS0b2bey6Qr1novk6RJq85pLmcdzdbw8yQPWCuh7YMoYiDkrt3YLJ4cEHPORJ1ZmYS3eUi3qlM6ylLC_7Zky-MXyAnHQ2m4jPN0pOarND9am30Rvex-7t_BgHVYasuYY-9ZQ-t8jDlqZAIn4IOLSh336FhRMngbgMRR9ArkoYXY2g7N-wMZtE50:1vEhYW:dFszlZgOL8DEhR4j27WuZaggoBauWWEMyMUgc9V3SUw','2025-11-14 12:20:08.696019'),('1eqndredcd3pt98bhe6uypg7fe9ix31b','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vGqcj:Qc1qYRprBWrA_mUt8T4I6sWwvu3O1SJ39aRneGKHz4I','2025-12-06 10:25:21.696915'),('2hxfnqoyyy1c69pojtx001st87dqluw5','.eJxVjEEOwiAQRe8ya0NKSwt06d4zkIEZLGrAlDbRGO-uTbrp9r_3_gdc5VpTyY5fzzS_YWxO4HBdJrdWnl0iGEFqOIwew53zRuiG-VpEKHmZkxebInZaxaUQP867eziYsE7_Whlig6GhjsyAQfto-4CRsW97ZK8lKdlp1Ka1dmiilp2xSloZ40BWo4fvD119P78:1vNmzL:--c8m6Cu1sXwO9T8dYoKBargBq2osDv8CYCSZJ1fNsU','2025-11-26 13:57:23.279015'),('32igoq2eck540vo35lzej8rc8mg44fgr','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vNluR:4k0QEmD_Q3GaqlOBMydVWyUn1g-zP0psMgvDaClIKVU','2025-11-26 12:48:15.452691'),('51mnu57jx8qhx2idjupns2tixb95w981','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWhsa24tNGFmZGU1MTQ1YzUwNGU1ZGRhY2FhMTBmM2NlYjk1N2QifQ:1vELlT:ghK5QylHqkzbKpBiIV9FzRcWTleWoMcqk9vPZY85B50','2025-11-13 13:04:03.092254'),('626l7il4yj3jo5syyjb0wi6saipgfs3g','eyJwcmVfMmZhX3VzZXJfaWQiOjE3fQ:1vNmju:9HwR3X1ZbPnLehiw9PTpqSeZPzLC8WrN8BjIBIY5LsM','2025-11-26 13:41:26.816779'),('65r6mjgfuoaluld76elbjif7j81nujtp','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vNN4x:UT8BmryR8VyF9NKMbZf75cvtfpYuL6eVQlkIWtCZWmQ','2025-11-25 10:17:27.767153'),('6d6lh1iby6o11cmztsaywfc16x342h04','.eJxVjEEOwiAQRe_C2pBOCwy4dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWgOL0OwaKj1R3wneqtyZjq-syB7kr8qBdXhun5-Vw_w4K9fKtleVkKQ48sTUUMWSnI-VEetSUAgIrmJDQjs6ZISNM1ilwkLNhhxTE-wMtZDiC:1vGqmn:JFeDW-A-b401XLWkuX5OfZAVAU4uq5S60IjXkZdrueo','2025-12-06 10:35:45.285993'),('776y5zd3zr8s6rsqbkjdg8d71r98zob6','.eJxVjMEOwiAQBf-Fs2kKbVno0bvfQBZYLFqhKZhojP9uTXrpdWbe-7AZSzX0wDibXBdTKFU2cpACZCeEOLENlRJzMvRa4vpmY7sxfNbJPAutJno2Mg7sAC26O6W_8TdM19y4nOoabfNPmt2W5pI9zee9PRxMWKZt3StPCl3rO68kOrBBDw4D4SAGJAvc97wDBCW0lm0A3indc81DkF4DWvb9AR82SlU:1vINF7:Y53b7nnN7mAbZZyt1SSBkCuSIYwd9dyqhe1X-Q3T2Jo','2025-12-10 15:27:17.613882'),('9fucyczeqasp6csyyi08u2hnclysri0w','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjejN0cjItMmQ3NGQyN2FiMWUxOTI4YTc2NGExNTdjZWE1NTAwNjkifQ:1vIhWp:DBGB6hbFNxf15_5rZb1zbkkdrFA2Dm8R4dgoyu6bZJc','2025-12-11 13:06:55.173660'),('9oyjtjnifregw43hipokzv52x8lnfb6h','.eJxVjDEOwjAMRe-SGUVxUyU1IztniGzHIQXUSk07Ie4OlTrA-t97_2USbWtNW9MljdmcDZjT78YkD512kO803WYr87QuI9tdsQdt9jpnfV4O9--gUqvf2gkVHIJo7HxALKgoDD5DiB6VexnIi1IuEFwEzp4xKHCADrBzPZn3B_RzOAY:1vFOxr:jQ7eRssTBo98CDHBP8MMJupe9AY_Lnc_tbOFyXebHhE','2025-11-16 10:41:11.864924'),('a0ptfx3g5nqwinan12z4x9mrxz0cfuuu','eyJwcmVfMmZhX3VzZXJfaWQiOjN9:1vFAU8:XYT78yi61oe4Gau0VsrI7OjhHFy61VLEIZBMy61x8Dw','2025-11-15 19:13:32.374378'),('brr0lpk7nzcwgdjhas1kk9fj3i3a5w5m','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vLzty:V2XCGD2cC8NRFuJWhnOHwwQPj8tJ6akTPu1QNwcUHvs','2025-11-21 15:20:26.882710'),('bxft7oguw7mahpt42jtnytnvqwtc90zn','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vGsiS:ZZ7j9gCUhIXSASECm7evTkObPpdpX-xMk1vZP3fNVag','2025-12-06 12:39:24.042771'),('c00jakwhdv8v03ci0cs8o7v3i6mg4cx6','.eJxVjEEOwiAQRe_C2pDSMi106d4zkBmYWtSAgTbRGO-uTbrp9r_3_ke4yrXGnBy_nrG8xdichMN1md1aubgYxChULw4job9z2ki4Ybpm6XNaSiS5KXKnVV5y4Md5dw8HM9b5X_dmaNkOuvFsO2uQgLxXaCcmACLTK90aDsOkoNOEpsFWgdU2gFYIoMT3BzmWPu8:1vIh8x:lMCqiby_ZF9FHC7Kao0SddEQObXOkXcrlWGV6nGJ0qc','2025-12-11 12:42:15.379475'),('cdhsxfq0drkpmlwq8zkyypu0vx1rv5d0','.eJxVjDEOwjAMRe-SGUVxUyU1IztniGzHIQXUSk07Ie4OlTrA-t97_2USbWtNW9MljdmcDZjT78YkD512kO803WYr87QuI9tdsQdt9jpnfV4O9--gUqvf2gkVHIJo7HxALKgoDD5DiB6VexnIi1IuEFwEzp4xKHCADrBzPZn3B_RzOAY:1vELYC:rnn253hSHRKRQguRni2paKLVQklY_uEss0T2cLOS0Bw','2025-11-13 12:50:20.932500'),('cdyrrap2yk0dlgwfc52lq733dhh5adw6','.eJxVjssKwyAURP_FdRGj9ZEsu-83iMZ7G9uiQRNoKf33GgiUbOfMHOZDbIVaY04WXnMsbzKwE7FuXSa7Vig2BjIQocgh9G58QNpIuLt0y3TMaSnR061Cd1rpNQd4XvbuQTC5Om1eLnthhEbkGqUGZ_zoOROglWdcojFdaEAa2QV0oHxvmD5zhQw72TZNOhewHN3_rFDfH5tmRc8:1vM00n:pFRRNLB80HOVuaN3itSg7kHtKPbkxdkRh86Wo8tQhT8','2025-11-21 15:27:29.200675'),('e5bxty4o034ccafm94904g5uojbpfrw7','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vIght:NnIk7mVdKfg4lVjVZ3bQxUmkFlJuJc_SfIUCvwrIr4E','2025-12-11 12:14:17.259020'),('f8y1t2a5x9rqleadjymrei5ej4silggk','.eJxVjMEOgyAQBf-Fc2NE0QWPvfcbyAJLpbVgBJM2Tf-9mnjxOjPvfdmEuWh6YZh0KrPOFAsbOPQNCAVtfWEbyjmkqOk9h-XDhp3hWka9Zlp0cGxgHNgJGrRPirtxD4z3VNkUyxJMtSfVYXN1S46m69GeDkbM47YW0pFEW7vWyR4tGK86i56wazokA9wJ3gKCbJTqaw-8lUpwxb3vnQI07PcHJVNKXQ:1vIJjO:dWfPJcGIF5fTSkeLl_ZCjpEruqezDDZGx24w9N2t3oU','2025-12-10 11:42:18.399415'),('fbjehsdud5x2ph1hdbmr0789v1iwc6ur','.eJxVjEEOwiAQRe_C2hAGOoy6dO8ZmoEBqRpISrsy3l2bdKHb_977LzXyupRx7WkeJ1FndVKH3y1wfKS6AblzvTUdW13mKehN0Tvt-tokPS-7-3dQuJdvjRbJDykKCVnIEQGdBSRHJrF4gIxIgOIpZuvA-OwjmWB54Hy0xqn3B7_5Nts:1vEiyh:3IiPXqRSZgBcVwNkkomNKbu81vZVjPtLyScCXGamilg','2025-11-14 13:51:15.382683'),('ff6ax44l93p9380ekgobohmt17wfuvrf','.eJxVjMsKwjAQRf8lawnNqyZduu83hJnJYKOSSNOCIv67Frrp9p5z7kfExq3lWiK_nnl-i6E7iQjrMsW18RxzEoNQThxGBLpz2Ui6QblWSbUsc0a5KXKnTY418eOyu4eDCdr0r9GDMuQCgCcPhr0l1KQSpeCMScwKe0dad6gwkNKK0SKF3p6T9cFr8f0BW4E_yA:1vGqYU:z2zgMokQg4wDwh2_k6D78CMupUJ9aMHlSHglx_BEOiQ','2025-12-06 10:20:58.401567'),('frxqucsgrdd7gb3qdo4syv7k2quqgtwc','.eJxVjDEOwjAMRe-SGUVxUyU1IztniGzHIQXUSk07Ie4OlTrA-t97_2USbWtNW9MljdmcDZjT78YkD512kO803WYr87QuI9tdsQdt9jpnfV4O9--gUqvf2gkVHIJo7HxALKgoDD5DiB6VexnIi1IuEFwEzp4xKHCADrBzPZn3B_RzOAY:1vGq7V:vu484zx_iTE5OALo1Fz6PO3HbHpWjZ2L-kKwl8hYhlw','2025-11-20 09:53:05.620245'),('ftxpfe1m7zcbepu1fllkyb455ymhzglh','.eJxVjMEOgyAQBf-Fc2NE0QWPvfcbyAJLpbVgBJM2Tf-9mnjxOjPvfdmEuWh6YZh0KrPOFAsbOPQNCOCqvbAN5RxS1PSew_JhQ70xXMuo10yLDo4NjAM7QYP2SXE37oHxniqbYlmCqfakOmyubsnRdD3a08GIedzWQjqSaGvXOtmjBeNVZ9ETdk2HZIA7wVtAkI1Sfe2Bt1IJrrj3vVOAhv3-JghKXg:1vIJ4Y:mQ8C9ywJpu9UXFUm28srWekV_3FRNtXC9yWhoAQKQcU','2025-12-10 11:00:06.399457'),('gwdtq8dhfsu9vw1nnd9pvmk0u44i5rzb','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vG8iH:Dm6Yu0sRSD4jK5id-GvPtWkMB2f9z8_EVXFts-de-Q8','2025-11-18 11:32:09.467684'),('i4ziuu5qa1hp0cbbnah1i18hdkwcudxi','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWhsa24tNGFmZGU1MTQ1YzUwNGU1ZGRhY2FhMTBmM2NlYjk1N2QifQ:1vELlQ:e6IVwPr-GEq6Hbg7-CdkO8zqAfMpPN_B_fB8tecMPD0','2025-11-13 13:04:00.488042'),('iuvgswoy1sztmvwannaodo8o840wryi0','.eJxVjEEOwiAQRe_C2hBKO7R06d4zkIEZLGrAlDbRGO-uTbrp9r_3_ke4yrWmkh2_nml-i1GdhMN1mdxaeXaJxCi0EofRY7hz3gjdMF-LDCUvc_JyU-ROq7wU4sd5dw8HE9bpX0ewlhgaRtOGiGyICXtLnUaDurPQqxC08Qo8BxN1VLEdIgUAaBTCIL4_ZmRANQ:1vJQ73:-VjBVAtPIVfIZMwQXhE76VkI-1c2fM1DdAoRMFt81_Q','2025-12-13 12:43:17.579992'),('jpauqi8idlidsv3ey3n05jlkf3qjl7qc','.eJxVjDEOwjAMRe-SGUVxUyU1IztniGzHIQXUSk07Ie4OlTrA-t97_2USbWtNW9MljdmcDZjT78YkD512kO803WYr87QuI9tdsQdt9jpnfV4O9--gUqvf2gkVHIJo7HxALKgoDD5DiB6VexnIi1IuEFwEzp4xKHCADrBzPZn3B_RzOAY:1vEI7c:gNd2rPEhIcZzjaCpt5cmCXiX7A5HZd9kpTsr65ZT_H0','2025-11-13 09:10:40.131034'),('kwit8sjez1fibwmkfougwly6mp9280o2','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vFOwx:IUSkYA95Gq1qZy-jxEyNj6SwJzuYlsyYFr7MIZxaVeM','2025-11-16 10:40:15.552354'),('m64hcwpifbmhnppl9697u795q07k7jyi','.eJxVjEEOwiAQRe_C2hBK26F06d4zkGFgLGrAlDbRGO-uTbrp9r_3_ke4GmtNJbv4eqb5LUZ1Eg7XZXJrjbNLQYxCd-IweqR7zBsJN8zXIqnkZU5eborcaZWXEuLjvLuHgwnr9K9NaGzUZIM3AxtocWgBqCFskRvsvGarmIC4NwAI5BX3PmoOCllpY8X3B1RuQDg:1vJqHd:93Si6B06G6Fz7fkb1tJxxmmik0bSToQMYt99LFMAyJE','2025-12-14 16:39:57.452104'),('n3ppnx7zyg5qu8k0klo8xsziwd9ejaag','.eJxVjMsOwiAQRf-FtSGU8uh06d5vIANMLWrAQJtojP-uTbrp9p5z7oe5Rq2lkh29nqm-2ShOzOG6zG5tVF2KbGTSsMPoMdwpbyTeMF8LDyUvNXm-KXynjV9KpMd5dw8HM7b5X1stSSs7KSSjNJL2egDVK09aio4sSC1NHwCVsAATSJCqs4MRcTBTsD37_gASeT3s:1vKTAD:IEx__UOe77A7rvvDk3Jy5IYzzzmeLi0FvIe9LdHDxec','2025-12-16 10:10:53.185813'),('n3tsom38tzhp5eobhlk16oxpnvvtwgfo','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWhlbnEtYTI4Nzk0NmEzMzk4OWJiNzM4MTcwZGFhNTI0MjUzMjAifQ:1vEJPu:xxmqeqQRcuneHiVslD7P-u2l2MoJOq78V1e2RvJHqhw','2025-11-13 10:33:38.749825'),('npi4lvcgcote0l5gumpf8u2coskgxz65','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vG8fL:DGz5oaRgrM5c5czCgxZvJ78YME6wrQ0K8J2vKaGV_JM','2025-11-18 11:29:07.452852'),('nu7mjxmsnpo0uk4rk5m0dnocw0syjpwq','.eJxVj8sKwyAQRf_FdRA18dVl9_0GGXVsbEsSNIGW0n9vAoGQ3XDOncvMl7iKteZxcPiecvmQi5BWMMYaIhK4uSx1xkgu64An5JaKxeVVcd0QB8vcH4hwTU7QQ3jisJn4gOE-0jAOc8mebhG620pvY8TXdc-eCnqo_brdmYgGAottNAqC9snKAAlBCgnoNY8dbzVoI6xVLGneGttxy1NS0Wrwa-lU0G1_HPer3x-Svld3:1vKTCl:UWyPFqsOPV2-zSBhO1vXU_FqkuKiWi2SugGIoAXlXP4','2025-12-16 10:13:31.089662'),('o5elxn96zgvfeu8hjbq2hd9xgemtwa2b','eyJwcmVfMmZhX3VzZXJfaWQiOjN9:1vF1Jl:3Rs6mWQ29SlyCAWYkf5TB70n5EPXuWZPoARxUpR5Rmw','2025-11-15 09:26:13.272923'),('oexknjchp5b5tzljqunf25ks035wlbsq','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vEO5I:cDi-iOqs2CBxVAslcQsvZQpaO1NaLWzCn5TXuk0-QF0','2025-11-13 15:32:40.122905'),('ofpg2hm66cvahymxrc60nnre1jzs3jfs','.eJxVjEEOwiAQRe_C2hBKoWVcuu8ZyAwMUjWQlHZlvLtt0oVu_3vvv4XHbc1-a7z4OYqrAHH53QjDk8sB4gPLvcpQy7rMJA9FnrTJqUZ-3U737yBjy3uNyegxErikXEddoD1lHAI7rW0gSI6NQdUPCaJSFrQmMNHgCBb7XgXx-QIOlThh:1vEhy9:AAtuw7GYmZzdMuBJgPnFQeLqaliE-jt8BtT2MbA_hOk','2025-11-14 12:46:37.641525'),('oowdqh19an67nj0w67lk1vfx2w6jclcw','eyJwcmVfMmZhX3VzZXJfaWQiOjJ9:1vE3Gd:prPX9-El66kQaz8bYon9D7QDsbqAEC3xsGeNGxtO0oY','2025-11-12 17:18:59.520634'),('pccp42u7q1zpd8esrzwq0t6otoq0w3xm','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWpkeDEtZWJhMDg3ZGVhYTdiYWM0MjUwZmQ2YjMxYmNjZmZiYjQifQ:1vEhRf:sJOjNJt3CqDuHtSieV2fuyGQNr3wFdYKNhh0nHZsS8E','2025-11-14 12:13:03.090856'),('pnnkp1i8ld04cuz201lwviomd6sepc7k','.eJxVjEEOwiAQRe8ya0NKSwt06d4zkIEZLGrAlDbRGO-uTbrp9r_3_gdc5VpTyY5fzzS_YWxO4HBdJrdWnl0iGEFqOIwew53zRuiG-VpEKHmZkxebInZaxaUQP867eziYsE7_Whlig6GhjsyAQfto-4CRsW97ZK8lKdlp1Ka1dmiilp2xSloZ40BWo4fvD119P78:1vOTCj:-nNKB1lxAyLG_MzsShZbJnH7BpHxk8r9yR1GjHcnW7c','2025-11-28 11:02:01.582832'),('q6n5cum40cu0rtyrmg93442nlt9sb0cw','eyJwcmVfMmZhX3VzZXJfaWQiOjIzfQ:1vJNLG:Jbr76gLzMBRRZ_tKC1A-MYEsvtYrB2CZjy6MWPIjVlE','2025-12-13 09:45:46.168023'),('r9x8y8zql0z4u1nfmc73zz69htvrc5en','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vHv9x:8m4A2fbFzMOGTSrexcg49Oko1VEtCqqsoojdNnenQ2g','2025-12-09 09:28:05.924281'),('rmj122lvogl00qf8bkjsjj03hbczvs9t','eyJwcmVfMmZhX3VzZXJfaWQiOjN9:1vF101:E7ELSeY6ggPfExzZvT-2Dk_NOXQBvNX4J_msJT7ZM2s','2025-11-15 09:05:49.700458'),('soz2cymi1j8byidaim4w9qy4kcqplwly','.eJxVjEEKwyAURO_iOoiaGLXL7nsG-eq3sS2mqIGW0rs3gUDJbnhvZj7EVqw1zdni65nKm5yENIIx1hERwbay1IaBnNaAB2SXisWmVXHVEQtLm_6IcEUO0IG_Y95MuEG-ztTPuZXk6Fahu630Mgd8nPfu4WCCOq3rQQfU4Fnogx7BKxeN9BARpJCATvEw8F6B0sKYkUXFe20GbniMYzAKHPn-AKzIUH0:1vKSuX:zQNnmgOWuVOj_yNLBDLo-Ngxi5rYHU1lyTUF-mXIlbg','2025-12-16 09:54:41.567943'),('stfa7zkzqemy1zdga1w56h3imf8e0gpn','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWpkeDEtZWJhMDg3ZGVhYTdiYWM0MjUwZmQ2YjMxYmNjZmZiYjQifQ:1vEhRf:sJOjNJt3CqDuHtSieV2fuyGQNr3wFdYKNhh0nHZsS8E','2025-11-14 12:13:03.584487'),('u3iujbrjfig9wqllm7z1shats246v1ov','.eJxVjMsOwiAQRf-FtSFQXm2X7v0GMjCjRQ0YaBON8d9tk266Pefc-2W-UWupZE_vV6ofNooT87DMk18aVZ-QjUz27AADxAflzeAd8q3wWPJcU-Bbwnfb-KUgPc97eziYoE3rWlNPRkk9mKtzzpCyUunOKkQn4tAjhYCkQSq7sthJgdGCHaQBQhI6st8fJRE_SA:1vGsqy:rwgC3KgIwkqlXfb7mri6E8LBxB0EpBc0qumQKgjDY24','2025-12-06 12:48:12.019904'),('ub4d4ms9mq3t8brxh8ivzplm9dak7woq','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vF1XZ:O7P8emgpdOyavom9OASyjqnHZBy5xu-TC_GCLPSCzqE','2025-11-15 09:40:29.886526'),('ucrpgwrhazzcbtr83r08y8pdr63tipxr','eyJwcmVfMmZhX3VzZXJfaWQiOjE3fQ:1vKSpz:wVIa8uoRmkcG-219owzf4veDMp_Th4hgClfl_asv7lE','2025-12-16 09:49:59.197527'),('uh9guvrmioj7xb33ha6f406dv5c5lff4','eyJwcmVfMmZhX3VzZXJfaWQiOjE3fQ:1vIJL0:B5vNo66ZusoCi43DXNC2RGVeTxiuhGK-BSmUvJgPqSA','2025-12-10 11:17:06.516212'),('ulr4cm44y3r6wlufx4yoax6qx0t938vp','eyJwcmVfMmZhX3VzZXJfaWQiOjJ9:1vE3NC:Ts7_XYj9AUGCvm8ahZheeOT_Q_g3LtWr6cpYQ1ktK30','2025-11-12 17:25:46.847369'),('v2848q14kl5o6cfhu1owpy8h528ftj1e','.eJxVjMsOgyAUBf-FdWNAebrsvt9ALnCttBaMYNKm6b9XEzduZ-acL5mgVIsviJPNdbYFUyU9U7LVnCpqLmRDpcScLL7nuHxITzcGax3tWnCxMZCeMElO0IF_YtpNeEC658bnVJfomj1pDluaWw44XY_2dDBCGbe11KpFozj1aDqjwQnnPQMzoBPCOS0ZbzUGNTDRcQeaQsuE4SYIzkAIRn5__8JJiw:1vIhPF:ggdtg-FkflpVPeVXghgh0Qett6oXK1RPj-gj6ZOigiI','2025-12-11 12:59:05.602645'),('vnab5feixdy6miemn1857cr5bwimk2qi','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwSNW0po-V8d-1SRPT7Tnn3rd6TRJNobjOMsU-qzO4k4q0LvWPFHTqAJnSQ4bN5DsNt1GncVimnvWW6N3O-jpmeV729nBQaa6_deedkeBskyS0wRMjpwQUijAis-_AGi_ZFcDWMvmGDGCwIaMFQgT1-QIPkD6t:1vLBZn:L0Se-0kq6Nf7fN8gSHwParNipfsTzD8Mr76DHATaFkE','2025-11-19 09:36:15.954653'),('vukiu4xrhmviwzzayt8ytyeuyudd2wmj','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vFjLU:yFeQPUNqoVR9-hKzXnqevKHzaVw1FotEdkjTdlCBPfk','2025-11-17 08:26:56.046112'),('z9btudxjq6qz86adwwzkmtolif1r0p1g','.eJxVjsEOgjAQRP-lZ9OwLSmsR-9-Q7O73QpqwBQ4Ef9dSEjU67yZl1lNpGXu4jJpiX0yZwPm9JsxyUOHHaQ7DbfRyjjMpWe7V-xBJ3sdkz4vR_dP0NHUbetKKGMbRBvnA2JGRWHwCULjUbmWlrwopQyhaoCTZwwKHMABuqqmTfoqGl2m71f__gCZ0z7M:1vEO3S:yyJ_lYKtvNh9C4mjcRvNfLCm-lcTxBKXdPS6-SQ-kq0','2025-11-13 15:30:46.463995'),('zs51a01cg6y3tu32n95hhuj5dykg15o9','.eJxVjs0KwjAQhN8lZwlN_zbx6N1nCJvsxkYlLUkLivjutlCQXueb-ZiPsIVLiWOy_JpifotzdRIWl3mwS-FsI4mzUCAOoUP_4LQRumO6jdKPac7Rya0id1rkdSR-XvbuQTBgGdZ1q4k1-ooa0j16cMF0HgNjV3fIDhS1qgEEXRvTVwFUo02rjAqhJwPoVumU2dYB_2cVfH_jwUa6:1vKSm4:8q5ZcwQc4IgGXADfnHbiLfomrIC8U_8lssbtL9LXH9E','2025-12-16 09:45:56.623806'),('zu9e5ujqmd5of4o0tg05py4id4k3r4oa','eyJwcmVfMmZhX3VzZXJfaWQiOjE3fQ:1vPJ3P:2EtVsXxLbTZl46nmmBK5i716EF_Jl1u-oIMwsRYkp6Y','2025-11-30 18:23:51.752712');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_bookmark`
--

DROP TABLE IF EXISTS `forum_bookmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_bookmark` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `thread_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `forum_bookmark_user_id_thread_id_f904cfe8_uniq` (`user_id`,`thread_id`),
  KEY `forum_bookmark_thread_id_f9f7be0c_fk_forum_thread_id` (`thread_id`),
  CONSTRAINT `forum_bookmark_thread_id_f9f7be0c_fk_forum_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `forum_thread` (`id`),
  CONSTRAINT `forum_bookmark_user_id_09f8b934_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_bookmark`
--

LOCK TABLES `forum_bookmark` WRITE;
/*!40000 ALTER TABLE `forum_bookmark` DISABLE KEYS */;
/*!40000 ALTER TABLE `forum_bookmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_category`
--

DROP TABLE IF EXISTS `forum_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_category`
--

LOCK TABLES `forum_category` WRITE;
/*!40000 ALTER TABLE `forum_category` DISABLE KEYS */;
INSERT INTO `forum_category` VALUES (1,'buổi sáng tốt lành','morning'),(2,'gà gáy','gg');
/*!40000 ALTER TABLE `forum_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_notification`
--

DROP TABLE IF EXISTS `forum_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notification_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `post_id` bigint DEFAULT NULL,
  `sender_id` bigint DEFAULT NULL,
  `thread_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_notification_post_id_2cc74c40_fk_forum_post_id` (`post_id`),
  KEY `forum_notification_sender_id_21387523_fk_accounts_user_id` (`sender_id`),
  KEY `forum_notification_thread_id_a87691a7_fk_forum_thread_id` (`thread_id`),
  KEY `forum_notification_user_id_448eeb71_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `forum_notification_post_id_2cc74c40_fk_forum_post_id` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`id`),
  CONSTRAINT `forum_notification_sender_id_21387523_fk_accounts_user_id` FOREIGN KEY (`sender_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `forum_notification_thread_id_a87691a7_fk_forum_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `forum_thread` (`id`),
  CONSTRAINT `forum_notification_user_id_448eeb71_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_notification`
--

LOCK TABLES `forum_notification` WRITE;
/*!40000 ALTER TABLE `forum_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `forum_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_post`
--

DROP TABLE IF EXISTS `forum_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `thread_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_post_author_id_609b7963_fk_accounts_user_id` (`author_id`),
  KEY `forum_post_thread_id_f9fa0a56_fk_forum_thread_id` (`thread_id`),
  CONSTRAINT `forum_post_author_id_609b7963_fk_accounts_user_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `forum_post_thread_id_f9fa0a56_fk_forum_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `forum_thread` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_post`
--

LOCK TABLES `forum_post` WRITE;
/*!40000 ALTER TABLE `forum_post` DISABLE KEYS */;
INSERT INTO `forum_post` VALUES (1,'làm tí phở không ae','2025-10-29 16:58:23.508095',1,1),(15,'lo','2025-11-10 11:33:25.166173',16,2),(18,'gggggggggggggggggggggg','2025-11-10 15:20:23.459957',16,4),(19,'looooooooooooooo','2025-11-11 12:59:39.241314',22,1),(20,'https://youtu.be/cL8DpF9gdas?si=94iapL8htqaHhnJ8','2025-11-11 13:01:27.071042',22,5),(22,'hi','2025-11-30 06:43:19.533266',17,5);
/*!40000 ALTER TABLE `forum_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_post_likes`
--

DROP TABLE IF EXISTS `forum_post_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_post_likes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `forum_post_likes_post_id_user_id_fa33a7ea_uniq` (`post_id`,`user_id`),
  KEY `forum_post_likes_user_id_56514e1a_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `forum_post_likes_post_id_eeecd63b_fk_forum_post_id` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`id`),
  CONSTRAINT `forum_post_likes_user_id_56514e1a_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_post_likes`
--

LOCK TABLES `forum_post_likes` WRITE;
/*!40000 ALTER TABLE `forum_post_likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `forum_post_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_postreaction`
--

DROP TABLE IF EXISTS `forum_postreaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_postreaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `forum_postreaction_post_id_user_id_74888e5b_uniq` (`post_id`,`user_id`),
  KEY `forum_postreaction_user_id_e3c48e37_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `forum_postreaction_post_id_a01f9257_fk_forum_post_id` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`id`),
  CONSTRAINT `forum_postreaction_user_id_e3c48e37_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_postreaction`
--

LOCK TABLES `forum_postreaction` WRITE;
/*!40000 ALTER TABLE `forum_postreaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `forum_postreaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_profilepost`
--

DROP TABLE IF EXISTS `forum_profilepost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_profilepost` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_profilepost_author_id_2f2f3943_fk_accounts_user_id` (`author_id`),
  KEY `forum_profilepost_user_id_cb2bdfec_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `forum_profilepost_author_id_2f2f3943_fk_accounts_user_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `forum_profilepost_user_id_cb2bdfec_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_profilepost`
--

LOCK TABLES `forum_profilepost` WRITE;
/*!40000 ALTER TABLE `forum_profilepost` DISABLE KEYS */;
/*!40000 ALTER TABLE `forum_profilepost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_report`
--

DROP TABLE IF EXISTS `forum_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `report_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_note` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `post_id` bigint DEFAULT NULL,
  `reporter_id` bigint NOT NULL,
  `resolved_by_id` bigint DEFAULT NULL,
  `thread_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_report_post_id_02026d83_fk_forum_post_id` (`post_id`),
  KEY `forum_report_reporter_id_f7e3028b_fk_accounts_user_id` (`reporter_id`),
  KEY `forum_report_resolved_by_id_00b8332d_fk_accounts_user_id` (`resolved_by_id`),
  KEY `forum_report_thread_id_289a0c22_fk_forum_thread_id` (`thread_id`),
  CONSTRAINT `forum_report_post_id_02026d83_fk_forum_post_id` FOREIGN KEY (`post_id`) REFERENCES `forum_post` (`id`),
  CONSTRAINT `forum_report_reporter_id_f7e3028b_fk_accounts_user_id` FOREIGN KEY (`reporter_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `forum_report_resolved_by_id_00b8332d_fk_accounts_user_id` FOREIGN KEY (`resolved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `forum_report_thread_id_289a0c22_fk_forum_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `forum_thread` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_report`
--

LOCK TABLES `forum_report` WRITE;
/*!40000 ALTER TABLE `forum_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `forum_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_thread`
--

DROP TABLE IF EXISTS `forum_thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_thread` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `locked` tinyint(1) NOT NULL,
  `author_id` bigint NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_thread_author_id_c72b456f_fk_accounts_user_id` (`author_id`),
  KEY `forum_thread_category_id_dcc73d52_fk_forum_category_id` (`category_id`),
  CONSTRAINT `forum_thread_author_id_c72b456f_fk_accounts_user_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `forum_thread_category_id_dcc73d52_fk_forum_category_id` FOREIGN KEY (`category_id`) REFERENCES `forum_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_thread`
--

LOCK TABLES `forum_thread` WRITE;
/*!40000 ALTER TABLE `forum_thread` DISABLE KEYS */;
INSERT INTO `forum_thread` VALUES (1,'ăn sáng ở đâu','2025-10-29 16:57:55.816847',0,1,1),(2,'gà serema','2025-11-10 08:48:47.463536',0,17,2),(4,'hi','2025-11-10 15:20:23.453207',0,16,1),(5,'gà serema','2025-11-11 13:01:27.063948',0,22,2);
/*!40000 ALTER TABLE `forum_thread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_threadfollow`
--

DROP TABLE IF EXISTS `forum_threadfollow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_threadfollow` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `thread_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `forum_threadfollow_user_id_thread_id_f0e17e27_uniq` (`user_id`,`thread_id`),
  KEY `forum_threadfollow_thread_id_8a351a48_fk_forum_thread_id` (`thread_id`),
  CONSTRAINT `forum_threadfollow_thread_id_8a351a48_fk_forum_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `forum_thread` (`id`),
  CONSTRAINT `forum_threadfollow_user_id_1d1c1d76_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_threadfollow`
--

LOCK TABLES `forum_threadfollow` WRITE;
/*!40000 ALTER TABLE `forum_threadfollow` DISABLE KEYS */;
/*!40000 ALTER TABLE `forum_threadfollow` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-30  4:24:44
