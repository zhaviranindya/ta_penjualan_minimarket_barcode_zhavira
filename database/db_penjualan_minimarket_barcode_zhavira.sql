-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 10, 2026 at 06:20 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_penjualan_minimarket_barcode_zhavira`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_barang_zhavira`
--

CREATE TABLE `tb_barang_zhavira` (
  `kode_barang_zhavira` varchar(20) NOT NULL,
  `nama_barang_zhavira` varchar(100) NOT NULL,
  `harga_zhavira` int(100) NOT NULL,
  `stok_zhavira` int(100) NOT NULL,
  `status_zhavira` enum('tersedia','tidak tersedia') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_barang_zhavira`
--

INSERT INTO `tb_barang_zhavira` (`kode_barang_zhavira`, `nama_barang_zhavira`, `harga_zhavira`, `stok_zhavira`, `status_zhavira`) VALUES
('8 996001 358399', 'Wafello Chocoblast 97,6 g', 8000, 10, 'tersedia'),
('8 998009 011702', 'Ultra Milk Taro 200 ml', 5000, 15, 'tersedia'),
('8 999999 519087', 'Lux Botanicals Soft Rose 100 g', 4000, 10, 'tersedia');

-- --------------------------------------------------------

--
-- Table structure for table `tb_detail_transaksi_zhavira`
--

CREATE TABLE `tb_detail_transaksi_zhavira` (
  `id_detail_zhavira` int(11) NOT NULL,
  `id_transaksi_zhavira` int(11) NOT NULL,
  `kode_barang_zhavira` varchar(20) NOT NULL,
  `harga_zhavira` int(11) NOT NULL,
  `jumlah_zhavira` int(11) NOT NULL,
  `subtotal_zhavira` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_laporan_keuangan_zhavira`
--

CREATE TABLE `tb_laporan_keuangan_zhavira` (
  `id_laporan_zhavira` varchar(10) NOT NULL,
  `id_transaksi_zhavira` varchar(10) NOT NULL,
  `tanggal_zhavira` date NOT NULL,
  `total_penjualan_zhavira` int(225) NOT NULL,
  `total_tunai_zhavira` int(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_transaksi_zhavira`
--

CREATE TABLE `tb_transaksi_zhavira` (
  `id_transaksi_zhavira` varchar(10) NOT NULL,
  `id_user_zhavira` varchar(10) NOT NULL,
  `nama_user_zhavira` varchar(100) NOT NULL,
  `tanggal_waktu_zhavira` datetime NOT NULL,
  `total_belanja_zhavira` int(225) NOT NULL,
  `metode_bayar_zhavira` enum('tunai','non tunai') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_user_zhavira`
--

CREATE TABLE `tb_user_zhavira` (
  `id_user_zhavira` varchar(10) NOT NULL,
  `username_zhavira` varchar(50) NOT NULL,
  `password_zhavira` varchar(50) NOT NULL,
  `nama_user_zhavira` varchar(100) NOT NULL,
  `role_zhavira` enum('kasir','staf','manager') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_user_zhavira`
--

INSERT INTO `tb_user_zhavira` (`id_user_zhavira`, `username_zhavira`, `password_zhavira`, `nama_user_zhavira`, `role_zhavira`) VALUES
('U001', 'manajertoko142', 'manajer142', 'Arjuna Bagaskara', 'manager'),
('U002', 'stafbarang182', 'staf182', 'Gibran Adyatma', 'staf'),
('U003', 'kasir1702', 'kasir172', 'Zhavira Nindya', 'kasir');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_barang_zhavira`
--
ALTER TABLE `tb_barang_zhavira`
  ADD PRIMARY KEY (`kode_barang_zhavira`);

--
-- Indexes for table `tb_detail_transaksi_zhavira`
--
ALTER TABLE `tb_detail_transaksi_zhavira`
  ADD PRIMARY KEY (`id_detail_zhavira`),
  ADD KEY `id_transaksi_zhavira` (`id_transaksi_zhavira`,`kode_barang_zhavira`);

--
-- Indexes for table `tb_laporan_keuangan_zhavira`
--
ALTER TABLE `tb_laporan_keuangan_zhavira`
  ADD PRIMARY KEY (`id_laporan_zhavira`),
  ADD KEY `id_transaksi_zhavira` (`id_transaksi_zhavira`);

--
-- Indexes for table `tb_transaksi_zhavira`
--
ALTER TABLE `tb_transaksi_zhavira`
  ADD PRIMARY KEY (`id_transaksi_zhavira`),
  ADD KEY `id_user_zhavira` (`id_user_zhavira`);

--
-- Indexes for table `tb_user_zhavira`
--
ALTER TABLE `tb_user_zhavira`
  ADD PRIMARY KEY (`id_user_zhavira`),
  ADD UNIQUE KEY `username_zhavira` (`username_zhavira`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_detail_transaksi_zhavira`
--
ALTER TABLE `tb_detail_transaksi_zhavira`
  MODIFY `id_detail_zhavira` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
