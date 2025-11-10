-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: twofa_db
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.2

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
  `code_hash` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_backupcode_user_id_7e72a328_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_backupcode_user_id_7e72a328_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_backupcode`
--

LOCK TABLES `accounts_backupcode` WRITE;
/*!40000 ALTER TABLE `accounts_backupcode` DISABLE KEYS */;
INSERT INTO `accounts_backupcode` VALUES (21,'pbkdf2_sha256$1000000$4BEbEYShFMVeHqhbQZaWFw$QGGiV8zJqImXDYaeoIbiqI8n6Wb+pJf00l3SQeBH0rI=',0,'2025-11-06 10:35:45.176609',17),(22,'pbkdf2_sha256$1000000$6w9k1jKfpWJ7pJq9nIzWmZ$8/al3Oe2/zK4TVJ0AmeLkV2bT1ttuTh4MSv+5CdqwGY=',0,'2025-11-06 10:35:45.176636',17),(23,'pbkdf2_sha256$1000000$g8weGFsbFlFSjGzxwDxdJL$dy5futwqQzSGAeEOGoiJXDS2nIWFqG3IoE8sLPUU7Ns=',0,'2025-11-06 10:35:45.176647',17),(24,'pbkdf2_sha256$1000000$3ZWPxbIoC0svAySybAnmKf$Oyt/YRvdkwz989JjXmv4KaS4FvkWYwtkdoTgQv3u2eY=',0,'2025-11-06 10:35:45.176655',17),(25,'pbkdf2_sha256$1000000$gkuiHz6bB0UxyaHxVRhKHx$NREgsO24Mi8UQPJ/DNhtnIF9M8Cizwsha6vJfKTE+Do=',0,'2025-11-06 10:35:45.176674',17),(26,'pbkdf2_sha256$1000000$sgFixTlEVnYp3NQu0K5AvK$ZBmT6wReguqHTEg/cHQ00k++yD0OHoMfY1c4rKnt1FE=',0,'2025-11-06 10:35:45.176682',17),(27,'pbkdf2_sha256$1000000$bbdQy4DwGtkGXwR6QxzgFZ$J+tKvpkqqiqTb0knhNwkgFmTfHeWSnQx/wJQULXFdYo=',0,'2025-11-06 10:35:45.176690',17),(28,'pbkdf2_sha256$1000000$BYlWkhdQoD57EKxcR9112D$SXS2Z8lB9hthhxLGELenvI5vhWIaFeXIN64RslEdLc0=',0,'2025-11-06 10:35:45.176697',17),(29,'pbkdf2_sha256$1000000$4ECJ76hC6OEfdXqyM1wNYj$UxFRqZ3vxjDDZ9TVJ01+YTyaXCS0oR+7B6iPKnUYWR4=',0,'2025-11-06 10:35:45.176705',17),(30,'pbkdf2_sha256$1000000$GNiMZRWljQRebnnmmosDn9$4+E3snExT6CvmdaCDM3D3+FpctfzYKF/o47IGzzll3w=',0,'2025-11-06 10:35:45.176713',17),(31,'pbkdf2_sha256$1000000$RbVlpqu5jvfsacM4KyJHDR$AWQ/35Kccesqhpu6wDUd0pwIVQj4CnHA3Uof6zX/7o0=',1,'2025-11-06 12:42:29.180266',18),(32,'pbkdf2_sha256$1000000$lbkyFNc4urVPfDmF32YrMl$AonTbTldk3IYNE0qn8Nhsao9SufyDxOgsa270jvzITs=',0,'2025-11-06 12:42:29.180294',18),(33,'pbkdf2_sha256$1000000$Nf3PYdQLq1VQdCaZtIajhs$BMo4mbAJNFwjHTjdkLxUsUKQDDBIUcSydyKpnASwwNM=',0,'2025-11-06 12:42:29.180305',18),(34,'pbkdf2_sha256$1000000$I87DEVu4e9Df396Q60jeGR$XR4wfgSqfD8lC1UAZ7I/e8evZtlig6dnilo6tx4cKAU=',0,'2025-11-06 12:42:29.180314',18),(35,'pbkdf2_sha256$1000000$hGFygM9CGqhNeQrDS4aqzI$pZwWDAkAMwf6zPZinYzyYrz8tpyzwu6tHQ2+sl5+2Fs=',0,'2025-11-06 12:42:29.180322',18),(36,'pbkdf2_sha256$1000000$buxUbwBsYWBjW0LZ7r4CBI$FhLc+koiClKbW6T0rugrz7qkGSt9CZ3cMTKrFoj3fAo=',0,'2025-11-06 12:42:29.180331',18),(37,'pbkdf2_sha256$1000000$O7vonsZLtVUobh2dgjoigY$si+BOGm5FDVZuUn4GKb4qyssdBUwco3ujJWHXTk5dqw=',0,'2025-11-06 12:42:29.180339',18),(38,'pbkdf2_sha256$1000000$FrDDf2peknb8yfrUxXSrDF$TlT4kW5gFSQchCgPUEWIYRDIOtBzYmDWD5VXxjo7kw0=',0,'2025-11-06 12:42:29.180347',18),(39,'pbkdf2_sha256$1000000$voxiQF3UjZuUpEeiZguEvg$B/FM91Nb2CaZYUvSyja7r5MUwC7IbryPwZT3lXXzlOg=',0,'2025-11-06 12:42:29.180355',18),(40,'pbkdf2_sha256$1000000$Y7LLKnARTbKE67iZzVeGY3$y6jDt3YtyRD+TCBzp/61W5OvykP1M/vbMQdfYeLfTL0=',0,'2025-11-06 12:42:29.180363',18);
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
  `event` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `note` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_securitylog_user_id_6ab82c19_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_securitylog_user_id_6ab82c19_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_securitylog`
--

LOCK TABLES `accounts_securitylog` WRITE;
/*!40000 ALTER TABLE `accounts_securitylog` DISABLE KEYS */;
INSERT INTO `accounts_securitylog` VALUES (1,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-29 17:00:45.902726',NULL),(2,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-29 17:10:25.859808',NULL),(3,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-29 17:12:34.487062',NULL),(4,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-29 17:13:12.491285',NULL),(5,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-29 17:14:39.914767',NULL),(6,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-29 17:15:21.578648',NULL),(7,'OTP_SUCCESS','127.0.0.1','Enable 2FA success','2025-10-29 17:15:43.834189',NULL),(8,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-30 09:09:15.990959',NULL),(9,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 09:31:35.260029',NULL),(10,'OTP_SUCCESS','127.0.0.1','Enable 2FA success','2025-10-30 09:31:50.246801',NULL),(11,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 09:42:39.311075',NULL),(12,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 09:42:55.175399',NULL),(13,'OTP_SUCCESS','127.0.0.1','Enable 2FA success','2025-10-30 09:43:12.181090',NULL),(14,'OTP_FAIL','127.0.0.1','OTP failed attempt 1','2025-10-30 09:50:28.425390',NULL),(15,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 10:03:04.060907',NULL),(16,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-30 10:03:24.899367',NULL),(17,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 10:04:34.297259',NULL),(18,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 10:09:25.311097',NULL),(19,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-30 10:33:02.937542',NULL),(20,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 12:51:57.795028',NULL),(21,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 12:57:18.356761',NULL),(22,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-30 13:06:29.189617',NULL),(23,'OTP_FAIL','127.0.0.1','OTP failed attempt 1','2025-10-30 13:07:16.976353',NULL),(24,'OTP_FAIL','127.0.0.1','OTP failed attempt 2','2025-10-30 13:07:22.162037',NULL),(25,'OTP_FAIL','127.0.0.1','OTP failed attempt 3','2025-10-30 13:07:26.637943',NULL),(26,'OTP_FAIL','127.0.0.1','OTP failed attempt 4','2025-10-30 13:07:29.145378',NULL),(27,'OTP_FAIL','127.0.0.1','OTP failed attempt 5 -> LOCKED','2025-10-30 13:07:30.360626',NULL),(28,'OTP_LOCKED','127.0.0.1','User tried while locked','2025-10-30 13:07:31.419936',NULL),(29,'OTP_FAIL','127.0.0.1','OTP failed attempt 6 -> LOCKED','2025-10-30 13:08:19.473393',NULL),(30,'OTP_LOCKED','127.0.0.1','User tried while locked','2025-10-30 13:08:44.980732',NULL),(31,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-30 13:09:13.062260',NULL),(32,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-30 13:09:49.823737',NULL),(33,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-30 15:32:40.083286',NULL),(34,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-31 12:41:58.322614',9),(35,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-31 12:42:56.802183',9),(36,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-10-31 12:43:57.410659',9),(37,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-31 12:44:31.463980',9),(38,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-31 12:45:46.039115',9),(39,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-31 12:46:37.630822',9),(40,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-10-31 13:51:15.342789',9),(41,'OTP_FAIL','127.0.0.1','OTP failed attempt 1','2025-11-01 09:40:22.301762',NULL),(42,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-01 09:40:29.849392',NULL),(43,'OTP_FAIL','127.0.0.1','OTP failed attempt 1','2025-11-02 10:40:02.415315',NULL),(44,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-02 10:40:15.516872',NULL),(45,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-02 10:56:17.902404',NULL),(46,'OTP_FAIL','127.0.0.1','OTP failed attempt 1','2025-11-02 10:57:19.339101',NULL),(47,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-02 10:57:23.904583',NULL),(48,'OTP_FAIL','127.0.0.1','OTP failed attempt 1','2025-11-03 07:36:16.656229',NULL),(49,'OTP_FAIL','127.0.0.1','OTP failed attempt 2','2025-11-03 07:36:26.210686',NULL),(50,'OTP_FAIL','127.0.0.1','OTP failed attempt 3','2025-11-03 07:36:32.332304',NULL),(51,'OTP_FAIL','127.0.0.1','OTP failed attempt 4','2025-11-03 07:36:38.376085',NULL),(52,'OTP_FAIL','127.0.0.1','OTP failed attempt 5 -> LOCKED','2025-11-03 07:36:40.389090',NULL),(53,'OTP_LOCKED','127.0.0.1','User tried while locked','2025-11-03 07:36:41.201811',NULL),(54,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-03 07:44:16.093076',NULL),(55,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-03 08:10:02.676850',NULL),(56,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-03 08:11:01.871126',NULL),(57,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-03 08:14:44.427930',NULL),(58,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-03 08:16:15.425705',NULL),(59,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-03 08:18:39.858287',NULL),(60,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-03 08:26:56.012895',NULL),(61,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-04 11:29:07.424942',NULL),(62,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-04 11:32:09.443275',NULL),(63,'OTP_FAIL','127.0.0.1','OTP failed attempt 1','2025-11-06 09:47:45.154073',NULL),(64,'OTP_SUCCESS','127.0.0.1','OTP ok, full login','2025-11-06 09:47:53.240517',NULL),(65,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-06 09:52:39.930547',NULL),(66,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-06 09:53:45.671285',NULL),(67,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-06 09:55:16.506826',NULL),(68,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-06 09:57:29.987563',NULL),(69,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-06 10:12:39.221091',NULL),(70,'EMAIL_OTP_SENT','127.0.0.1','','2025-11-06 10:16:25.142525',NULL),(71,'OTP_SUCCESS','127.0.0.1','OTP (Email) ok, full login','2025-11-06 10:16:33.250522',NULL),(72,'OTP_SUCCESS','127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 10:17:15.557273',NULL),(73,'OTP_FAIL','127.0.0.1','Backup code failed attempt 1','2025-11-06 10:18:06.464611',NULL),(74,'BACKUP_CODE_USED','127.0.0.1','Login success (Backup Code)','2025-11-06 10:18:13.910789',NULL),(75,'OTP_SUCCESS','127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 10:19:08.788143',NULL),(76,'OTP_FAIL','127.0.0.1','OTP failed attempt 1','2025-11-06 10:20:49.823352',NULL),(77,'OTP_SUCCESS','127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 10:20:58.369664',NULL),(78,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-06 10:35:14.412982',17),(79,'LOGIN_SUCCESS','127.0.0.1','Login without 2FA yet','2025-11-06 12:41:31.947692',18),(80,'EMAIL_OTP_SENT','127.0.0.1','','2025-11-06 12:43:29.407029',18),(81,'OTP_SUCCESS','127.0.0.1','OTP (Email) ok, full login','2025-11-06 12:43:44.617427',18),(82,'BACKUP_CODE_USED','127.0.0.1','Login success (Backup Code)','2025-11-06 12:44:17.591869',18),(83,'OTP_SUCCESS','127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:44:54.166538',18),(84,'OTP_SUCCESS','127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:46:21.224805',18),(85,'OTP_SUCCESS','127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:46:42.885256',18),(86,'OTP_SUCCESS','127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:47:03.456210',18),(87,'OTP_SUCCESS','127.0.0.1','OTP (TOTP) ok, full login','2025-11-06 12:48:11.984165',18);
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
INSERT INTO `accounts_securitypolicy` VALUES (8,1,'2025-11-06 09:56:11.996384');
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
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified` tinyint(1) NOT NULL,
  `otp_secret` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_2fa_enabled` tinyint(1) NOT NULL,
  `must_setup_2fa` tinyint(1) NOT NULL,
  `failed_otp_attempts` int NOT NULL,
  `must_change_password` tinyint(1) NOT NULL,
  `otp_locked` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `accounts_user_email_b2644a56_uniq` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1000000$JhDklB2XWM4vYc3Q7p5rIr$M1T7qHKHK0dJ9/oOhnnTUlnTe4MObRdz+9hluFkrQmY=','2025-11-06 09:53:05.610775',1,'admin','','','chaunhathoa@gmail.com',1,1,'2025-10-29 16:41:09.000000','USER',0,'WN66VVBF4QOQSCZNEA5EJECVQ6WPVI4R',0,1,0,0,0),(9,'pbkdf2_sha256$1000000$Vr97n6fD4Cls9HZk51lyBW$gWCW1hYnKI5na/hdopOoxFc9cQBA49ncy4Ld1dnGThY=','2025-10-31 13:51:15.373738',0,'hai','','','chauminhhai458@gmail.com',0,1,'2025-10-31 12:21:07.000000','USER',1,'ZH6JE7RKQWQOF5X3HH37B57WJB42BOFK',1,0,0,0,0),(16,'pbkdf2_sha256$1000000$G46uO4We84yZ4XW5fywuhK$8uqEnalLjV8vVLzCIm5WvLXngpKhPXb7BvZY0oF0jmw=','2025-11-06 12:39:24.032783',1,'admin1','','','hoa@gmail.com',1,1,'2025-11-06 10:25:02.549148','USER',0,NULL,0,1,0,0,0),(17,'pbkdf2_sha256$1000000$7HR5XFtndOxrmwPbQmy4uc$7vhFPcAP6JSHs4zh1INwCJTh+gOMX4Gpq2ETi02Lt0s=','2025-11-06 10:35:14.430465',0,'hoa','','','chaunhathoa24102004@gmail.com',0,1,'2025-11-06 10:34:30.008127','USER',1,'PGEODJCVWN7BKIE4EEDBGCBSMSNUWMQM',1,0,0,0,0),(18,'pbkdf2_sha256$1000000$7URh702KIJ9RRJ6PX29qGR$UHiJ/2k7eA9Z/j79ng2zEqOjqZXzxlOhe6ZCHxSvKwc=','2025-11-06 12:48:12.011958',0,'DinhQuoc','','','nguyendinhquoc1905@gmail.com',0,1,'2025-11-06 12:40:37.571356','USER',1,'MZP5OZFOKVEECNHYWCPK2X4T6VAAPDFP',1,0,0,0,0);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
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
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
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
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
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
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-10-29 16:57:22.863471','1','buổi sáng tốt lành',1,'[{\"added\": {}}]',9,1),(2,'2025-10-29 16:57:55.817627','1','ăn sáng ở đâu',1,'[{\"added\": {}}]',10,1),(3,'2025-10-29 16:58:23.508840','1','Post by admin on ăn sáng ở đâu',1,'[{\"added\": {}}]',11,1),(4,'2025-10-30 09:30:31.267180','2','hoa',3,'',6,1),(5,'2025-10-30 09:41:40.160711','1','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(6,'2025-10-30 09:46:18.547509','2','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(7,'2025-10-30 09:46:40.126376','4','hai',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\"]}}]',6,1),(8,'2025-10-30 09:49:34.771681','4','hai',3,'',6,1),(9,'2025-10-30 09:49:50.456381','3','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(10,'2025-10-30 09:50:09.596869','4','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(11,'2025-10-30 09:50:12.752490','4','Chính sách bảo mật hệ thống',2,'[]',7,1),(12,'2025-10-30 09:53:18.796917','5','hai',3,'',6,1),(13,'2025-10-30 10:02:21.416490','5','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(14,'2025-10-30 12:53:38.606268','3','Post by DinhQuoc on ăn sáng ở đâu',2,'[{\"changed\": {\"fields\": [\"Content\"]}}]',11,1),(15,'2025-10-30 12:54:05.945531','3','Post by DinhQuoc on ăn sáng ở đâu',3,'',11,1),(16,'2025-10-30 13:08:13.476939','7','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Otp locked\"]}}]',6,1),(17,'2025-10-30 13:09:00.389491','7','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Otp locked\"]}}]',6,1),(18,'2025-10-30 13:09:31.637641','7','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',6,1),(19,'2025-10-30 13:09:46.827284','7','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\"]}}]',6,1),(20,'2025-10-31 12:20:23.463654','6','hai',3,'',6,1),(21,'2025-10-31 12:43:44.865755','9','hai',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\", \"Must setup 2fa\"]}}]',6,1),(22,'2025-11-02 10:55:01.015512','7','DinhQuoc',3,'',6,1),(23,'2025-11-02 10:55:07.163015','8','MinhQuan',3,'',6,1),(24,'2025-11-03 07:43:35.372700','10','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Otp locked\", \"Must change password\"]}}]',6,1),(25,'2025-11-03 07:45:14.234891','10','DinhQuoc',2,'[{\"changed\": {\"fields\": [\"Is 2fa enabled\", \"Must setup 2fa\"]}}]',6,1),(26,'2025-11-03 08:16:09.463573','6','Post by admin on ăn sáng ở đâu',3,'',11,1),(27,'2025-11-03 08:18:20.998374','7','Post by DinhQuoc on ăn sáng ở đâu',3,'',11,1),(28,'2025-11-03 08:30:28.560315','8','Post by hoa on ăn sáng ở đâu',3,'',11,1),(29,'2025-11-06 09:48:38.175532','3','hoa',3,'',6,1),(30,'2025-11-06 09:49:48.055282','1','admin',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',6,1),(31,'2025-11-06 09:50:56.991973','6','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(32,'2025-11-06 09:51:24.658522','11','hoa',3,'',6,1),(33,'2025-11-06 09:53:12.308277','6','Chính sách bảo mật hệ thống',2,'[]',7,1),(34,'2025-11-06 09:54:04.881643','7','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(35,'2025-11-06 09:54:33.218921','12','hoa',3,'',6,1),(36,'2025-11-06 09:55:57.728534','5','Chính sách bảo mật hệ thống',3,'',7,1),(37,'2025-11-06 09:55:57.728577','4','Chính sách bảo mật hệ thống',3,'',7,1),(38,'2025-11-06 09:55:57.728593','3','Chính sách bảo mật hệ thống',3,'',7,1),(39,'2025-11-06 09:55:57.728606','2','Chính sách bảo mật hệ thống',3,'',7,1),(40,'2025-11-06 09:55:57.728619','1','Chính sách bảo mật hệ thống',3,'',7,1),(41,'2025-11-06 09:56:05.036667','7','Chính sách bảo mật hệ thống',3,'',7,1),(42,'2025-11-06 09:56:05.036710','6','Chính sách bảo mật hệ thống',3,'',7,1),(43,'2025-11-06 09:56:08.573818','8','Chính sách bảo mật hệ thống',1,'[{\"added\": {}}]',7,1),(44,'2025-11-06 09:56:11.997564','8','Chính sách bảo mật hệ thống',2,'[]',7,1),(45,'2025-11-06 09:56:37.439124','13','hoa',3,'',6,1),(46,'2025-11-06 09:56:57.503561','14','hoa',1,'[{\"added\": {}}]',6,1),(47,'2025-11-06 09:57:09.264476','14','hoa',2,'[{\"changed\": {\"fields\": [\"Email verified\"]}}]',6,1),(48,'2025-11-06 10:11:49.876330','14','hoa',3,'',6,1),(49,'2025-11-06 10:33:03.119120','15','hoa',3,'',6,16),(50,'2025-11-06 12:39:38.720888','10','DinhQuoc',3,'',6,16);
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
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
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
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-29 16:39:25.080621'),(2,'contenttypes','0002_remove_content_type_name','2025-10-29 16:39:25.275546'),(3,'auth','0001_initial','2025-10-29 16:39:25.888737'),(4,'auth','0002_alter_permission_name_max_length','2025-10-29 16:39:26.021310'),(5,'auth','0003_alter_user_email_max_length','2025-10-29 16:39:26.033217'),(6,'auth','0004_alter_user_username_opts','2025-10-29 16:39:26.043715'),(7,'auth','0005_alter_user_last_login_null','2025-10-29 16:39:26.054363'),(8,'auth','0006_require_contenttypes_0002','2025-10-29 16:39:26.061184'),(9,'auth','0007_alter_validators_add_error_messages','2025-10-29 16:39:26.071937'),(10,'auth','0008_alter_user_username_max_length','2025-10-29 16:39:26.082924'),(11,'auth','0009_alter_user_last_name_max_length','2025-10-29 16:39:26.093651'),(12,'auth','0010_alter_group_name_max_length','2025-10-29 16:39:26.118635'),(13,'auth','0011_update_proxy_permissions','2025-10-29 16:39:26.130188'),(14,'auth','0012_alter_user_first_name_max_length','2025-10-29 16:39:26.140494'),(15,'accounts','0001_initial','2025-10-29 16:39:26.856063'),(16,'accounts','0002_user_must_setup_2fa','2025-10-29 16:39:26.977254'),(17,'accounts','0003_securitypolicy','2025-10-29 16:39:27.032884'),(18,'accounts','0004_user_failed_otp_attempts_user_must_change_password_and_more','2025-10-29 16:39:27.569747'),(19,'admin','0001_initial','2025-10-29 16:39:27.876774'),(20,'admin','0002_logentry_remove_auto_add','2025-10-29 16:39:27.890235'),(21,'admin','0003_logentry_add_action_flag_choices','2025-10-29 16:39:27.905311'),(22,'forum','0001_initial','2025-10-29 16:39:28.568907'),(23,'sessions','0001_initial','2025-10-29 16:39:28.658457'),(24,'accounts','0005_securityconfig','2025-10-30 09:37:05.581094'),(25,'accounts','0006_alter_user_email','2025-10-30 09:58:34.471035'),(26,'accounts','0007_alter_securitylog_event_backupcode','2025-11-06 10:10:38.831593');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
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
INSERT INTO `django_session` VALUES ('0zg7t0y4q8230er27baoyhnuk4opied9','.eJxVjDkOwjAUBe_iGiL_ONgxJT1nsP5mwqIYxUGAEHcnSDS0b2bey6Qr1novk6RJq85pLmcdzdbw8yQPWCuh7YMoYiDkrt3YLJ4cEHPORJ1ZmYS3eUi3qlM6ylLC_7Zky-MXyAnHQ2m4jPN0pOarND9am30Rvex-7t_BgHVYasuYY-9ZQ-t8jDlqZAIn4IOLSh336FhRMngbgMRR9ArkoYXY2g7N-wMZtE50:1vEhYW:dFszlZgOL8DEhR4j27WuZaggoBauWWEMyMUgc9V3SUw','2025-11-14 12:20:08.696019'),('1eqndredcd3pt98bhe6uypg7fe9ix31b','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vGqcj:Qc1qYRprBWrA_mUt8T4I6sWwvu3O1SJ39aRneGKHz4I','2025-12-06 10:25:21.696915'),('51mnu57jx8qhx2idjupns2tixb95w981','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWhsa24tNGFmZGU1MTQ1YzUwNGU1ZGRhY2FhMTBmM2NlYjk1N2QifQ:1vELlT:ghK5QylHqkzbKpBiIV9FzRcWTleWoMcqk9vPZY85B50','2025-11-13 13:04:03.092254'),('6d6lh1iby6o11cmztsaywfc16x342h04','.eJxVjEEOwiAQRe_C2pBOCwy4dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWgOL0OwaKj1R3wneqtyZjq-syB7kr8qBdXhun5-Vw_w4K9fKtleVkKQ48sTUUMWSnI-VEetSUAgIrmJDQjs6ZISNM1ilwkLNhhxTE-wMtZDiC:1vGqmn:JFeDW-A-b401XLWkuX5OfZAVAU4uq5S60IjXkZdrueo','2025-12-06 10:35:45.285993'),('9oyjtjnifregw43hipokzv52x8lnfb6h','.eJxVjDEOwjAMRe-SGUVxUyU1IztniGzHIQXUSk07Ie4OlTrA-t97_2USbWtNW9MljdmcDZjT78YkD512kO803WYr87QuI9tdsQdt9jpnfV4O9--gUqvf2gkVHIJo7HxALKgoDD5DiB6VexnIi1IuEFwEzp4xKHCADrBzPZn3B_RzOAY:1vFOxr:jQ7eRssTBo98CDHBP8MMJupe9AY_Lnc_tbOFyXebHhE','2025-11-16 10:41:11.864924'),('a0ptfx3g5nqwinan12z4x9mrxz0cfuuu','eyJwcmVfMmZhX3VzZXJfaWQiOjN9:1vFAU8:XYT78yi61oe4Gau0VsrI7OjhHFy61VLEIZBMy61x8Dw','2025-11-15 19:13:32.374378'),('bxft7oguw7mahpt42jtnytnvqwtc90zn','.eJxVjMsOwiAQRf-FtSEdyhRw6d5vIDMwlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5TlmdFQzq9DsypYfUneQ71VvTqdV1nljvij7ooq8ty_NyuH8HhZbyrQfvjARnuyShD54YOSWgMAojMvsBrPGS3QjYWybfkQEMNmS0QIig3h8JfTey:1vGsiS:ZZ7j9gCUhIXSASECm7evTkObPpdpX-xMk1vZP3fNVag','2025-12-06 12:39:24.042771'),('cdhsxfq0drkpmlwq8zkyypu0vx1rv5d0','.eJxVjDEOwjAMRe-SGUVxUyU1IztniGzHIQXUSk07Ie4OlTrA-t97_2USbWtNW9MljdmcDZjT78YkD512kO803WYr87QuI9tdsQdt9jpnfV4O9--gUqvf2gkVHIJo7HxALKgoDD5DiB6VexnIi1IuEFwEzp4xKHCADrBzPZn3B_RzOAY:1vELYC:rnn253hSHRKRQguRni2paKLVQklY_uEss0T2cLOS0Bw','2025-11-13 12:50:20.932500'),('fbjehsdud5x2ph1hdbmr0789v1iwc6ur','.eJxVjEEOwiAQRe_C2hAGOoy6dO8ZmoEBqRpISrsy3l2bdKHb_977LzXyupRx7WkeJ1FndVKH3y1wfKS6AblzvTUdW13mKehN0Tvt-tokPS-7-3dQuJdvjRbJDykKCVnIEQGdBSRHJrF4gIxIgOIpZuvA-OwjmWB54Hy0xqn3B7_5Nts:1vEiyh:3IiPXqRSZgBcVwNkkomNKbu81vZVjPtLyScCXGamilg','2025-11-14 13:51:15.382683'),('ff6ax44l93p9380ekgobohmt17wfuvrf','.eJxVjMsKwjAQRf8lawnNqyZduu83hJnJYKOSSNOCIv67Frrp9p5z7kfExq3lWiK_nnl-i6E7iQjrMsW18RxzEoNQThxGBLpz2Ui6QblWSbUsc0a5KXKnTY418eOyu4eDCdr0r9GDMuQCgCcPhr0l1KQSpeCMScwKe0dad6gwkNKK0SKF3p6T9cFr8f0BW4E_yA:1vGqYU:z2zgMokQg4wDwh2_k6D78CMupUJ9aMHlSHglx_BEOiQ','2025-12-06 10:20:58.401567'),('frxqucsgrdd7gb3qdo4syv7k2quqgtwc','.eJxVjDEOwjAMRe-SGUVxUyU1IztniGzHIQXUSk07Ie4OlTrA-t97_2USbWtNW9MljdmcDZjT78YkD512kO803WYr87QuI9tdsQdt9jpnfV4O9--gUqvf2gkVHIJo7HxALKgoDD5DiB6VexnIi1IuEFwEzp4xKHCADrBzPZn3B_RzOAY:1vGq7V:vu484zx_iTE5OALo1Fz6PO3HbHpWjZ2L-kKwl8hYhlw','2025-11-20 09:53:05.620245'),('gwdtq8dhfsu9vw1nnd9pvmk0u44i5rzb','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vG8iH:Dm6Yu0sRSD4jK5id-GvPtWkMB2f9z8_EVXFts-de-Q8','2025-11-18 11:32:09.467684'),('i4ziuu5qa1hp0cbbnah1i18hdkwcudxi','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWhsa24tNGFmZGU1MTQ1YzUwNGU1ZGRhY2FhMTBmM2NlYjk1N2QifQ:1vELlQ:e6IVwPr-GEq6Hbg7-CdkO8zqAfMpPN_B_fB8tecMPD0','2025-11-13 13:04:00.488042'),('jpauqi8idlidsv3ey3n05jlkf3qjl7qc','.eJxVjDEOwjAMRe-SGUVxUyU1IztniGzHIQXUSk07Ie4OlTrA-t97_2USbWtNW9MljdmcDZjT78YkD512kO803WYr87QuI9tdsQdt9jpnfV4O9--gUqvf2gkVHIJo7HxALKgoDD5DiB6VexnIi1IuEFwEzp4xKHCADrBzPZn3B_RzOAY:1vEI7c:gNd2rPEhIcZzjaCpt5cmCXiX7A5HZd9kpTsr65ZT_H0','2025-11-13 09:10:40.131034'),('kwit8sjez1fibwmkfougwly6mp9280o2','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vFOwx:IUSkYA95Gq1qZy-jxEyNj6SwJzuYlsyYFr7MIZxaVeM','2025-11-16 10:40:15.552354'),('n3tsom38tzhp5eobhlk16oxpnvvtwgfo','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWhlbnEtYTI4Nzk0NmEzMzk4OWJiNzM4MTcwZGFhNTI0MjUzMjAifQ:1vEJPu:xxmqeqQRcuneHiVslD7P-u2l2MoJOq78V1e2RvJHqhw','2025-11-13 10:33:38.749825'),('npi4lvcgcote0l5gumpf8u2coskgxz65','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vG8fL:DGz5oaRgrM5c5czCgxZvJ78YME6wrQ0K8J2vKaGV_JM','2025-11-18 11:29:07.452852'),('o5elxn96zgvfeu8hjbq2hd9xgemtwa2b','eyJwcmVfMmZhX3VzZXJfaWQiOjN9:1vF1Jl:3Rs6mWQ29SlyCAWYkf5TB70n5EPXuWZPoARxUpR5Rmw','2025-11-15 09:26:13.272923'),('oexknjchp5b5tzljqunf25ks035wlbsq','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vEO5I:cDi-iOqs2CBxVAslcQsvZQpaO1NaLWzCn5TXuk0-QF0','2025-11-13 15:32:40.122905'),('ofpg2hm66cvahymxrc60nnre1jzs3jfs','.eJxVjEEOwiAQRe_C2hBKoWVcuu8ZyAwMUjWQlHZlvLtt0oVu_3vvv4XHbc1-a7z4OYqrAHH53QjDk8sB4gPLvcpQy7rMJA9FnrTJqUZ-3U737yBjy3uNyegxErikXEddoD1lHAI7rW0gSI6NQdUPCaJSFrQmMNHgCBb7XgXx-QIOlThh:1vEhy9:AAtuw7GYmZzdMuBJgPnFQeLqaliE-jt8BtT2MbA_hOk','2025-11-14 12:46:37.641525'),('oowdqh19an67nj0w67lk1vfx2w6jclcw','eyJwcmVfMmZhX3VzZXJfaWQiOjJ9:1vE3Gd:prPX9-El66kQaz8bYon9D7QDsbqAEC3xsGeNGxtO0oY','2025-11-12 17:18:59.520634'),('pccp42u7q1zpd8esrzwq0t6otoq0w3xm','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWpkeDEtZWJhMDg3ZGVhYTdiYWM0MjUwZmQ2YjMxYmNjZmZiYjQifQ:1vEhRf:sJOjNJt3CqDuHtSieV2fuyGQNr3wFdYKNhh0nHZsS8E','2025-11-14 12:13:03.090856'),('rmj122lvogl00qf8bkjsjj03hbczvs9t','eyJwcmVfMmZhX3VzZXJfaWQiOjN9:1vF101:E7ELSeY6ggPfExzZvT-2Dk_NOXQBvNX4J_msJT7ZM2s','2025-11-15 09:05:49.700458'),('stfa7zkzqemy1zdga1w56h3imf8e0gpn','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjeWpkeDEtZWJhMDg3ZGVhYTdiYWM0MjUwZmQ2YjMxYmNjZmZiYjQifQ:1vEhRf:sJOjNJt3CqDuHtSieV2fuyGQNr3wFdYKNhh0nHZsS8E','2025-11-14 12:13:03.584487'),('u3iujbrjfig9wqllm7z1shats246v1ov','.eJxVjMsOwiAQRf-FtSFQXm2X7v0GMjCjRQ0YaBON8d9tk266Pefc-2W-UWupZE_vV6ofNooT87DMk18aVZ-QjUz27AADxAflzeAd8q3wWPJcU-Bbwnfb-KUgPc97eziYoE3rWlNPRkk9mKtzzpCyUunOKkQn4tAjhYCkQSq7sthJgdGCHaQBQhI6st8fJRE_SA:1vGsqy:rwgC3KgIwkqlXfb7mri6E8LBxB0EpBc0qumQKgjDY24','2025-12-06 12:48:12.019904'),('ub4d4ms9mq3t8brxh8ivzplm9dak7woq','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vF1XZ:O7P8emgpdOyavom9OASyjqnHZBy5xu-TC_GCLPSCzqE','2025-11-15 09:40:29.886526'),('ulr4cm44y3r6wlufx4yoax6qx0t938vp','eyJwcmVfMmZhX3VzZXJfaWQiOjJ9:1vE3NC:Ts7_XYj9AUGCvm8ahZheeOT_Q_g3LtWr6cpYQ1ktK30','2025-11-12 17:25:46.847369'),('vukiu4xrhmviwzzayt8ytyeuyudd2wmj','.eJxVjDEOwjAMRe-SGUUhRY7LyM4ZIsd2SAElUtNOiLtDpQ6w_vfef5lI61Li2nWOk5izGczhd0vED60bkDvVW7Pc6jJPyW6K3Wm31yb6vOzu30GhXr61MmXMR0ecxJM4BQkoXgf0Iegpq4wDAWbBlFCZMWcGdjAG8ATE5v0BMK85xw:1vFjLU:yFeQPUNqoVR9-hKzXnqevKHzaVw1FotEdkjTdlCBPfk','2025-11-17 08:26:56.046112'),('z9btudxjq6qz86adwwzkmtolif1r0p1g','.eJxVjsEOgjAQRP-lZ9OwLSmsR-9-Q7O73QpqwBQ4Ef9dSEjU67yZl1lNpGXu4jJpiX0yZwPm9JsxyUOHHaQ7DbfRyjjMpWe7V-xBJ3sdkz4vR_dP0NHUbetKKGMbRBvnA2JGRWHwCULjUbmWlrwopQyhaoCTZwwKHMABuqqmTfoqGl2m71f__gCZ0z7M:1vEO3S:yyJ_lYKtvNh9C4mjcRvNfLCm-lcTxBKXdPS6-SQ-kq0','2025-11-13 15:30:46.463995');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_category`
--

DROP TABLE IF EXISTS `forum_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_category`
--

LOCK TABLES `forum_category` WRITE;
/*!40000 ALTER TABLE `forum_category` DISABLE KEYS */;
INSERT INTO `forum_category` VALUES (1,'buổi sáng tốt lành','morning');
/*!40000 ALTER TABLE `forum_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_post`
--

DROP TABLE IF EXISTS `forum_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `thread_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_post_author_id_609b7963_fk_accounts_user_id` (`author_id`),
  KEY `forum_post_thread_id_f9fa0a56_fk_forum_thread_id` (`thread_id`),
  CONSTRAINT `forum_post_author_id_609b7963_fk_accounts_user_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `forum_post_thread_id_f9fa0a56_fk_forum_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `forum_thread` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_post`
--

LOCK TABLES `forum_post` WRITE;
/*!40000 ALTER TABLE `forum_post` DISABLE KEYS */;
INSERT INTO `forum_post` VALUES (1,'làm tí phở không ae','2025-10-29 16:58:23.508095',1,1),(4,'lo','2025-10-31 12:42:11.031725',9,1),(5,'gg','2025-10-31 12:46:52.599017',9,1),(11,'siuuuuu cr7','2025-11-06 10:36:15.796221',17,1);
/*!40000 ALTER TABLE `forum_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_thread`
--

DROP TABLE IF EXISTS `forum_thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_thread` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `locked` tinyint(1) NOT NULL,
  `author_id` bigint NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_thread_author_id_c72b456f_fk_accounts_user_id` (`author_id`),
  KEY `forum_thread_category_id_dcc73d52_fk_forum_category_id` (`category_id`),
  CONSTRAINT `forum_thread_author_id_c72b456f_fk_accounts_user_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `forum_thread_category_id_dcc73d52_fk_forum_category_id` FOREIGN KEY (`category_id`) REFERENCES `forum_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_thread`
--

LOCK TABLES `forum_thread` WRITE;
/*!40000 ALTER TABLE `forum_thread` DISABLE KEYS */;
INSERT INTO `forum_thread` VALUES (1,'ăn sáng ở đâu','2025-10-29 16:57:55.816847',0,1,1);
/*!40000 ALTER TABLE `forum_thread` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-06  6:21:39
