-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 04 jan. 2023 à 14:30
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
(1, 1003, 12, 100, 356, 468),
(5, 1005, 10, 20, 50, 80);

-- --------------------------------------------------------

--
-- Structure de la table `train_info`
--

CREATE TABLE `train_info` (
  `id` int(10) NOT NULL,
  `departure_station` varchar(400) DEFAULT NULL,
  `arrival_station` varchar(400) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `train_info`
--

INSERT INTO `train_info` (`id`, `departure_station`, `arrival_station`, `date`, `time`) VALUES
(1003, 'Aéroport Charles-de-Gaulle 2 TGV', 'Reims', '2023-02-08', '21:33:24.0000'),
(1005, 'Reims', 'La_Roche-sur-Yon', '2023-02-21', '12:02:00.0000');

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
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `seat_info`
--
ALTER TABLE `seat_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `train_info`
--
ALTER TABLE `train_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1006;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `seat_info`
--
ALTER TABLE `seat_info`
  ADD CONSTRAINT `seat_info_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `train_info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
