-- MySQL dump 10.13  Distrib 8.0.24, for Win64 (x86_64)
--
-- Host: localhost    Database: cts
-- ------------------------------------------------------
-- Server version	8.0.24

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
-- Table structure for table `mission`
--

DROP TABLE IF EXISTS `mission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mission` (
  `Mission_Id` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `Description` text,
  `StartDate` date DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `State` int DEFAULT '1',
  `Limit` int DEFAULT NULL,
  `Point` int DEFAULT NULL,
  `LimitDefault` int DEFAULT NULL,
  PRIMARY KEY (`Mission_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mission`
--

LOCK TABLES `mission` WRITE;
/*!40000 ALTER TABLE `mission` DISABLE KEYS */;
INSERT INTO `mission` VALUES (7,'Vệ sinh phòng làm việc','Tham gia vệ sinh văn phòng hàng tuần','2021-04-22','2021-08-26',1,10,14,NULL),(11,'Sharing hàng tuần','Tham gia sharing hàng tuần cho các bạn intern','2021-04-23','2021-04-24',0,0,100,NULL),(12,'Tham gia giải bóng đá TMA','Tham gia bóng đá với các anh em trong team nâng cao thể lực','2021-04-23','2021-04-24',0,25,50,NULL),(13,'Mentor Intern','Mentor thực tập sinh batch 7','2021-04-23','2021-04-24',0,60,250,NULL),(14,'Hiến máu tính nguyện','Tham gia hoạt động hiến máu tình nguyện hàng tuần','2021-05-23','2021-05-25',1,17,150,17),(15,'Phát cơm từ thiện','Tham gia phát cơm từ thiện','2021-05-23','2021-05-26',1,16,120,16),(16,'Chia sẻ kinh nghiệm học TA','Sharing cách học tiếng Anh','2021-05-23','2021-06-04',1,100,80,100),(17,'Tham gia công tác chuẩn bị teambuilding','Tham gia đội chuẩn bị cho team building','2021-04-22','2021-04-24',1,39,55,2),(18,'Ủng hộ đồng bào miền Trung','Tham gia ủng hộ đồng bào miền Trung vượt qua lũ lụt','2021-04-24','2021-06-06',1,1,45,1),(20,'Thi toeic','Chia se kinh nghiem thi toeic','2021-05-23','2021-05-25',1,10,100,10),(49,'Tưới cây','Tưới cây khu vực sau công ty','2021-05-05','2021-05-25',1,100,230,NULL),(50,'Ủng hộ trẻ em đồng bào','Tham gia hỗ trợ cho trẻ em đồng bào miền núi','2021-05-12','2021-05-21',1,49,500,NULL),(51,'Chuẩn bị HH','Mua đồ chuẩn bị cho HH hàng tuần','2021-05-23','2021-05-30',1,100,100,100),(55,'Thi toeic','Thi toeic hàng tuần','2021-05-14','2021-05-15',1,10,100,10),(56,'Hỗ trợ các bạn sinh viên thực tập','Hỗ trợ các bạn sinh viên nắm bắt thông tin của công ty cũng như tuyển dụng những bạn có khả năng','2021-05-14','2021-05-15',1,99,100,100);
/*!40000 ALTER TABLE `mission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-23 20:25:11
