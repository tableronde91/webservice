-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : dim. 15 jan. 2023 à 19:35
-- Version du serveur : 10.4.24-MariaDB
-- Version de PHP : 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `secf`
--

-- --------------------------------------------------------

--
-- Structure de la table `seat_info`
--

CREATE TABLE `seat_info` (
  `id` int(10) NOT NULL,
  `train_id` int(10) DEFAULT NULL,
  `first_class_seat` int(10) DEFAULT NULL,
  `business_class_seat` int(10) DEFAULT NULL,
  `standard_class_seat` int(10) DEFAULT NULL,
  `all_seats` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `seat_info`
--

INSERT INTO `seat_info` (`id`, `train_id`, `first_class_seat`, `business_class_seat`, `standard_class_seat`, `all_seats`) VALUES
(1, 1001, 3, 100, 356, 459),
(5, 1005, 7, 20, 50, 77),
(6, 1004, 5, 20, 50, 80),
(7, 1006, 10, 20, 50, 80),
(8, 1010, 14, 100, 356, 470);

-- --------------------------------------------------------

--
-- Structure de la table `train_info`
--

CREATE TABLE `train_info` (
  `id` int(11) NOT NULL,
  `departure_station` varchar(400) DEFAULT NULL,
  `arrival_station` varchar(400) DEFAULT NULL,
  `departure_date` date DEFAULT NULL,
  `departure_time` time DEFAULT NULL,
  `flex` tinyint(1) DEFAULT NULL,
  `price` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `train_info`
--

INSERT INTO `train_info` (`id`, `departure_station`, `arrival_station`, `departure_date`, `departure_time`, `flex`, `price`) VALUES
(1001, 'Reims', 'Paris', '2023-01-18', '10:44:00', 0, 56.3),
(1004, 'Paris', 'Marseille', '2023-01-15', '15:22:00', 0, 130),
(1005, 'Paris', 'Reims', '2023-01-20', '11:24:00', 1, 75.1),
(1006, 'Paris', 'Reims', '2023-01-20', '13:24:00', 1, 78.3),
(1010, 'Reims', 'Paris', '2023-01-26', '12:13:00', 0, 55.4);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `seat_info`
--
ALTER TABLE `seat_info`
  ADD PRIMARY KEY (`id`),
  ADD KEY `train_id` (`train_id`);

--
-- Index pour la table `train_info`
--
ALTER TABLE `train_info`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `seat_info`
--
ALTER TABLE `seat_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `train_info`
--
ALTER TABLE `train_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1011;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
