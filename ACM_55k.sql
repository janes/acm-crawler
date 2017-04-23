-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 06, 2015 at 12:26 AM
-- Server version: 5.5.41
-- PHP Version: 5.3.10-1ubuntu3.15

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ACM`
--

-- --------------------------------------------------------

--
-- Table structure for table `AUTHOR`
--

CREATE TABLE IF NOT EXISTS `AUTHOR` (
  `id_author` bigint(20) NOT NULL,
  `name` varchar(500) NOT NULL,
  PRIMARY KEY (`id_author`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `CONFERENCE`
--

CREATE TABLE IF NOT EXISTS `CONFERENCE` (
  `id_conference` varchar(20) NOT NULL,
  `title` varchar(500) NOT NULL,
  `abbreviation` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id_conference`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `PUBLICATION`
--

CREATE TABLE IF NOT EXISTS `PUBLICATION` (
  `id_publication` varchar(20) NOT NULL,
  `title` varchar(500) NOT NULL,
  `abstract` varchar(10000) NULL,
  `authors` varchar(1000) NOT NULL,
  `publisher` varchar(500) NOT NULL,
  `bibtex` varchar(3000) NULL,
  `date` date NOT NULL,
  `download12m` int NOT NULL DEFAULT '0',
  `download6w` int NOT NULL DEFAULT '0',
  `download` int NOT NULL DEFAULT '0',
  `citationCount` int NOT NULL DEFAULT '0',
  `full_collected` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_publication`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `PUBLICATION_HAS_AUTHORS`
--

CREATE TABLE IF NOT EXISTS `PUBLICATION_HAS_AUTHORS` (
  `id_publication` varchar(20) NOT NULL,
  `id_author` bigint(20) NOT NULL,
  PRIMARY KEY (`id_publication`,`id_author`),
  KEY `id_author` (`id_author`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `PUBLICATION_HAS_CONFERENCE`
--

CREATE TABLE IF NOT EXISTS `PUBLICATION_HAS_CONFERENCE` (
  `id_publication` varchar(20) NOT NULL,
  `id_conference` varchar(20) NOT NULL,
  PRIMARY KEY (`id_publication`,`id_conference`),
  KEY `id_conference` (`id_conference`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `PUBLICATION_HAS_REFERENCES`
--

CREATE TABLE IF NOT EXISTS `PUBLICATION_HAS_REFERENCES` (
  `id_publication` varchar(20) NOT NULL,
  `id_reference` varchar(20) NOT NULL,
  PRIMARY KEY (`id_publication`,`id_reference`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `QUEUE`
--

CREATE TABLE IF NOT EXISTS `QUEUE` (
  `id_publication` varchar(20) NOT NULL,
  PRIMARY KEY (`id_publication`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `PUBLICATION_HAS_AUTHORS`
--
ALTER TABLE `PUBLICATION_HAS_AUTHORS`
  ADD CONSTRAINT `publication_has_authors_ibfk_1` FOREIGN KEY (`id_publication`) REFERENCES `PUBLICATION` (`id_publication`),
  ADD CONSTRAINT `publication_has_authors_ibfk_2` FOREIGN KEY (`id_author`) REFERENCES `AUTHOR` (`id_author`);

--
-- Constraints for table `PUBLICATION_HAS_CONFERENCE`
--
ALTER TABLE `PUBLICATION_HAS_CONFERENCE`
  ADD CONSTRAINT `publication_has_conference_ibfk_1` FOREIGN KEY (`id_publication`) REFERENCES `PUBLICATION` (`id_publication`),
  ADD CONSTRAINT `publication_has_conference_ibfk_2` FOREIGN KEY (`id_conference`) REFERENCES `CONFERENCE` (`id_conference`);

--
-- Constraints for table `PUBLICATION_HAS_REFERENCES`
--
ALTER TABLE `PUBLICATION_HAS_REFERENCES`
  ADD CONSTRAINT `publication_has_references_ibfk_1` FOREIGN KEY (`id_publication`) REFERENCES `PUBLICATION` (`id_publication`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
