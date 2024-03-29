--
-- Database: `Weight`
--

CREATE DATABASE IF NOT EXISTS `weight`;

-- --------------------------------------------------------

--
-- Table structure for table `containers-registered`
--

USE weight;


CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;



-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  --   "neto": <int> or "na" // na if some of containers unknown
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;


show tables;

describe containers_registered;
describe transactions;



--
-- Dumping data for table `containers_registered`
--

INSERT INTO `containers_registered` (`container_id`, `weight`, `unit`  )
VALUES 
("T-123523", 543 , "kg"),
("T-234234", 123 , "kg"),
("T-345345", 234 , "kg"),
("T-465445", 765 , "kg"),
("T-675676", 543 , "kg"),
("T-985598",  null , "kg"),
("T-983338",  null , "kg"),
("T-912228",  null , "kg");


INSERT INTO `transactions` (`id`, `datetime`, `direction`, `truck`, `containers`, `bruto`, `truckTara`, `neto`, `produce`)
VALUES 
(1, '20010101010101' , "in" , "12345678" , "T-123523,T-465445" , 1200 , 1000 , 200 , "orange"),
(2, '20010101010101' , "out" , "12345678" , "T-465445,T-675676" , 1200 , 1000 , 200 , "tomato"),
(3, '20010101010101' , "none" , "2300021" , "T-465445,T-675676" , 0 , 444 , 0 , "na"),
(4, '20010101010101' , "in" , "2300021" , "T-465445,T-912228" , 0 , 900 , 0 , "na"),
(5, '20010101010101' , "in" , "2302222" , "T-123523,T-675676" , 0 , 700 , 0 , "tomato");

show tables;

SELECT * FROM `containers_registered`;