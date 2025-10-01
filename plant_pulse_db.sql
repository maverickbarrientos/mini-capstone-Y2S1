-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: plant_pulse_db
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `custom_plants`
--

DROP TABLE IF EXISTS `custom_plants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `custom_plants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_by` int DEFAULT NULL,
  `plant_code` varchar(45) DEFAULT NULL,
  `plant_name` varchar(45) NOT NULL,
  `description` text,
  `soil_type` varchar(45) DEFAULT NULL,
  `optimal_water_amount` varchar(45) NOT NULL,
  `soil_min_moisture` varchar(45) DEFAULT NULL,
  `soil_max_moisture` varchar(45) DEFAULT NULL,
  `ideal_min_temp` varchar(45) DEFAULT NULL,
  `ideal_max_temp` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `plant_code_UNIQUE` (`plant_code`),
  KEY `fk_user_id_idx` (`created_by`),
  CONSTRAINT `fk_created_by_user_id` FOREIGN KEY (`created_by`) REFERENCES `user_details` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_plants`
--

LOCK TABLES `custom_plants` WRITE;
/*!40000 ALTER TABLE `custom_plants` DISABLE KEYS */;
/*!40000 ALTER TABLE `custom_plants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_plants`
--

DROP TABLE IF EXISTS `default_plants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `default_plants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plant_code` varchar(45) DEFAULT NULL,
  `plant_name` varchar(45) NOT NULL,
  `description` text,
  `soil_type` varchar(45) DEFAULT NULL,
  `optimal_water_amount` varchar(45) NOT NULL,
  `soil_min_moisture` varchar(45) DEFAULT NULL,
  `soil_max_moisture` varchar(45) DEFAULT NULL,
  `ideal_min_temp` varchar(45) DEFAULT NULL,
  `ideal_max_temp` varchar(45) DEFAULT NULL,
  `is_default` tinyint DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `plant_code_UNIQUE` (`plant_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_plants`
--

LOCK TABLES `default_plants` WRITE;
/*!40000 ALTER TABLE `default_plants` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_plants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_accounts`
--

DROP TABLE IF EXISTS `user_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `created_at` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id_idx` (`user_id`),
  KEY `fk_email_idx` (`email`),
  CONSTRAINT `fk_email` FOREIGN KEY (`email`) REFERENCES `user_details` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_details` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_accounts`
--

LOCK TABLES `user_accounts` WRITE;
/*!40000 ALTER TABLE `user_accounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_details`
--

DROP TABLE IF EXISTS `user_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `birthdate` date NOT NULL,
  `email` varchar(45) NOT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  `profile_picture` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_details`
--

LOCK TABLES `user_details` WRITE;
/*!40000 ALTER TABLE `user_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_plants`
--

DROP TABLE IF EXISTS `user_plants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_plants` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `plant_code` varchar(45) DEFAULT NULL,
  `plant_source_type` enum('default','custom') DEFAULT 'default',
  `watering_status` enum('pending','completed','skipped') DEFAULT 'pending',
  `sensor_name` varchar(45) DEFAULT NULL,
  `sensor_status` enum('active','inactive') DEFAULT 'active',
  `last_watered` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_user_plants_user_id_idx` (`user_id`),
  CONSTRAINT `fk_user_plants_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_details` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_plants`
--

LOCK TABLES `user_plants` WRITE;
/*!40000 ALTER TABLE `user_plants` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_plants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `water_level`
--

DROP TABLE IF EXISTS `water_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `water_level` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `min_water_level` varchar(45) DEFAULT NULL,
  `max_water_level` varchar(45) DEFAULT NULL,
  `status` enum('sufficient','low','empty') DEFAULT 'sufficient',
  `last_refill` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_water_level_user_id_idx` (`user_id`),
  CONSTRAINT `fk_water_level_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_details` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `water_level`
--

LOCK TABLES `water_level` WRITE;
/*!40000 ALTER TABLE `water_level` DISABLE KEYS */;
/*!40000 ALTER TABLE `water_level` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-01 13:34:53
