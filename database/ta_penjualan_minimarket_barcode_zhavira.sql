-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 21, 2026 at 09:46 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ta_penjualan_minimarket_barcode_zhavira`
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
('8809698873345', 'Glad2Glow Cherry Blossom Micellar Water Pembersih Makeup 300 ml', 51500, 0, 'tersedia'),
('88999908082800', 'Marina UV White Lotion Pelembap Tubuh Healthy & Glow 185 ml', 11000, 20, 'tersedia'),
('8968601001', 'Indomie Mi Instan Ayam Bawang 69 g', 3200, 16, 'tersedia'),
('8968604320', 'Indomie Mi Instan Goreng Aceh 90 g', 3400, 15, 'tersedia'),
('8968691070', 'Indomie Mi Instan Goreng Rendang 91 g\r\n\r\n', 3400, 22, 'tersedia'),
('8992727002837', 'Biore Plester Komedo Charcoal 4 pcs', 15400, 19, 'tersedia'),
('8992832605275', 'Casablanca Femme Eau de Toilette Wanita Pure 100 ml', 28900, 10, 'tersedia'),
('8994942028593', 'Vio Acne Shield Patch Jerawat Karakter 24 pcs', 38000, 8, 'tersedia'),
('8996001358399', 'Wafello Wafer Cokelat Blast 97.6 g', 10300, 50, 'tersedia'),
('8997236033587', 'White Inc Alpha Glowhite Lotion Tubuh Mencerahkan 180 ml', 29900, 13, 'tersedia'),
('8998009011702', 'Ultra Milk Susu UHT Taro Kotak 200 ml', 7000, 20, 'tersedia'),
('8998824551261', 'Hanasui Serum Wajah Anti Jerawat 20 ml', 29900, 10, 'tersedia'),
('8998866107938', 'Posh Deodoran Roll On Wanita Whitening 50 ml', 18000, 10, 'tersedia'),
('8998866202343', 'Sedaap Mi Instan Goreng Selection Korean Ayam Pedas 87 g', 3200, 12, 'tersedia'),
('8998866203579', 'Sedaap Mi Instan Korean Keju Buldak 86 g', 3200, 20, 'tersedia'),
('8998866626842', 'Sedaap Mi Instan Ayam Jerit Rawit 77 g', 3100, 10, 'tersedia'),
('8999999580742', 'Rexona Deodoran Roll On Pria Sport Defence 45 ml', 22500, 10, 'tersedia'),
('8999999611378', 'Sunsilk Vitamin & Parfum Rambut Silky Gloss 100 ml', 36700, 30, 'tersedia');

-- --------------------------------------------------------

--
-- Table structure for table `tb_detail_transaksi_zhavira`
--

CREATE TABLE `tb_detail_transaksi_zhavira` (
  `id_detail_zhavira` int(11) NOT NULL,
  `id_transaksi_zhavira` varchar(20) NOT NULL,
  `kode_barang_zhavira` varchar(20) NOT NULL,
  `harga_zhavira` int(11) NOT NULL,
  `jumlah_zhavira` int(11) NOT NULL,
  `subtotal_zhavira` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_detail_transaksi_zhavira`
--

INSERT INTO `tb_detail_transaksi_zhavira` (`id_detail_zhavira`, `id_transaksi_zhavira`, `kode_barang_zhavira`, `harga_zhavira`, `jumlah_zhavira`, `subtotal_zhavira`) VALUES
(2, 'TX0002', '8996001358399', 8000, 4, 32000),
(3, 'TX0003', '8997236033587', 40000, 3, 120000),
(6, 'TX0006', '8997236033587', 40000, 1, 40000),
(8, 'TX0007', '8997236033587', 40000, 1, 40000),
(11, 'TX0009', '8997236033587', 40000, 2, 80000),
(16, 'TX0012', '8997236033587', 40000, 1, 40000),
(18, 'TX0013', '8997236033587', 40000, 2, 80000),
(19, 'TX0014', '8992727002837', 15400, 1, 15400),
(20, 'TX0014', '8997236033587', 29900, 2, 59800),
(21, 'TX0015', '8998866202343', 3200, 3, 9600);

-- --------------------------------------------------------

--
-- Table structure for table `tb_laporan_keuangan_zhavira`
--

CREATE TABLE `tb_laporan_keuangan_zhavira` (
  `id_laporan_zhavira` int(11) NOT NULL,
  `id_transaksi_zhavira` varchar(20) NOT NULL,
  `periode_zhavira` enum('perjam','persesi','perhari','perminggu','perbulan','pertahun') NOT NULL,
  `tanggal_awal_zhavira` datetime NOT NULL,
  `tanggal_akhir_zhavira` datetime NOT NULL,
  `total_penjualan_zhavira` int(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_laporan_keuangan_zhavira`
--

INSERT INTO `tb_laporan_keuangan_zhavira` (`id_laporan_zhavira`, `id_transaksi_zhavira`, `periode_zhavira`, `tanggal_awal_zhavira`, `tanggal_akhir_zhavira`, `total_penjualan_zhavira`) VALUES
(1, 'TX0001', 'perjam', '2026-04-19 15:35:44', '2026-02-20 00:00:00', 13500),
(2, 'TX0002', 'perjam', '2026-04-19 15:35:44', '2026-02-21 00:00:00', 32000),
(3, 'TX0003', 'perjam', '2026-04-19 15:35:44', '2026-02-21 00:00:00', 120000),
(4, 'TX0004', 'perjam', '2026-04-19 15:35:44', '2026-02-21 00:00:00', 9000),
(5, 'TX0005', 'perjam', '2026-04-19 15:35:44', '2026-02-21 00:00:00', 9000),
(6, 'TX0006', 'perjam', '2026-04-19 15:35:44', '2026-02-21 00:00:00', 44500),
(7, 'TX0007', 'perjam', '2026-04-19 15:35:44', '2026-02-21 00:00:00', 49000),
(8, 'TX0008', 'perjam', '2026-04-19 15:35:44', '2026-02-21 00:00:00', 13500),
(9, 'TX0009', 'perjam', '2026-04-19 15:35:44', '2026-02-21 00:00:00', 89000),
(10, 'TX0010', 'perjam', '2026-04-19 15:35:44', '2026-03-24 00:00:00', 4000),
(11, 'TX0011', 'perjam', '2026-04-19 15:35:44', '2026-03-24 00:00:00', 8000),
(12, 'TX0012', 'perjam', '2026-04-19 15:35:44', '2026-03-24 00:00:00', 44000),
(13, 'TX0013', 'perjam', '2026-04-19 15:35:44', '2026-03-24 00:00:00', 88000),
(14, 'TX0014', 'perjam', '2026-04-19 15:35:44', '2026-04-15 00:00:00', 75200),
(15, 'TX0015', 'perjam', '2026-04-19 15:35:44', '2026-04-15 00:00:00', 9600);

-- --------------------------------------------------------

--
-- Table structure for table `tb_perusahaan_zhavira`
--

CREATE TABLE `tb_perusahaan_zhavira` (
  `id_perusahaan_zhavira` varchar(10) NOT NULL,
  `nama_perusahaan_zhavira` varchar(100) NOT NULL,
  `nama_market_zhavira` varchar(100) NOT NULL,
  `alamat_zhavira` text NOT NULL,
  `no_telp_zhavira` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_perusahaan_zhavira`
--

INSERT INTO `tb_perusahaan_zhavira` (`id_perusahaan_zhavira`, `nama_perusahaan_zhavira`, `nama_market_zhavira`, `alamat_zhavira`, `no_telp_zhavira`) VALUES
('PC001', 'PT. PERTIWI MART INDONESIA', 'PERTIWI MART', 'JL. CIHANJUANG NO.1', '08123456789');

-- --------------------------------------------------------

--
-- Table structure for table `tb_transaksi_zhavira`
--

CREATE TABLE `tb_transaksi_zhavira` (
  `id_transaksi_zhavira` varchar(20) NOT NULL,
  `id_user_zhavira` varchar(10) NOT NULL,
  `nama_user_zhavira` varchar(100) NOT NULL,
  `metode_bayar_zhavira` enum('tunai','non tunai') NOT NULL,
  `tanggal_waktu_zhavira` datetime DEFAULT current_timestamp(),
  `total_belanja_zhavira` int(225) NOT NULL,
  `uang_bayar_zhavira` int(225) NOT NULL,
  `kembalian_zhavira` int(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_transaksi_zhavira`
--

INSERT INTO `tb_transaksi_zhavira` (`id_transaksi_zhavira`, `id_user_zhavira`, `nama_user_zhavira`, `metode_bayar_zhavira`, `tanggal_waktu_zhavira`, `total_belanja_zhavira`, `uang_bayar_zhavira`, `kembalian_zhavira`) VALUES
('TX0001', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-20 21:34:20', 13500, 15000, 1500),
('TX0002', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-21 12:18:01', 32000, 40000, 8000),
('TX0003', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-21 12:29:28', 120000, 200000, 80000),
('TX0004', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-21 13:12:39', 9000, 10000, 1000),
('TX0005', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-21 13:15:26', 9000, 10000, 1000),
('TX0006', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-21 13:22:00', 44500, 50000, 5500),
('TX0007', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-21 13:35:26', 49000, 50000, 1000),
('TX0008', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-21 13:41:00', 13500, 20000, 6500),
('TX0009', 'U003', 'Zhavira Nindya', 'tunai', '2026-02-21 13:47:45', 89000, 100000, 11000),
('TX0010', 'U003', 'Zhavira Nindya', 'tunai', '2026-03-24 10:30:48', 4000, 10000, 6000),
('TX0011', 'U003', 'Zhavira Nindya', 'tunai', '2026-03-24 10:52:16', 8000, 8000, 0),
('TX0012', 'U003', 'Zhavira Nindya', 'tunai', '2026-03-24 10:56:24', 44000, 50000, 6000),
('TX0013', 'U003', 'Zhavira Nindya', 'tunai', '2026-03-24 11:02:53', 88000, 100000, 12000),
('TX0014', 'U003', 'Zhavira Nindya', 'tunai', '2026-04-15 15:57:48', 75200, 100000, 24800),
('TX0015', 'U003', 'Zhavira Nindya', 'tunai', '2026-04-15 16:08:41', 9600, 10000, 400);

-- --------------------------------------------------------

--
-- Table structure for table `tb_user_zhavira`
--

CREATE TABLE `tb_user_zhavira` (
  `id_user_zhavira` varchar(10) NOT NULL,
  `id_perusahaan_zhavira` varchar(10) NOT NULL,
  `username_zhavira` varchar(50) NOT NULL,
  `password_zhavira` varchar(50) NOT NULL,
  `nama_user_zhavira` varchar(100) NOT NULL,
  `role_zhavira` enum('kasir','staf','manager','admin') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_user_zhavira`
--

INSERT INTO `tb_user_zhavira` (`id_user_zhavira`, `id_perusahaan_zhavira`, `username_zhavira`, `password_zhavira`, `nama_user_zhavira`, `role_zhavira`) VALUES
('U001', 'PC001', 'managertoko142', 'manager142', 'Arjuna Bagaskara', 'manager'),
('U002', 'PC001', 'stafbarang182', 'staf182', 'Gibran Adyatma', 'staf'),
('U003', 'PC001', 'kasir1702', 'kasir172', 'Zhavira Nindya', 'kasir'),
('U004', 'PC001', 'admin0702', 'admin72', 'Syahidan', 'admin');

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
  ADD KEY `id_transaksi_zhavira` (`id_transaksi_zhavira`,`kode_barang_zhavira`),
  ADD KEY `tb_detail_transaksi_zhavira_ibfk_2` (`kode_barang_zhavira`);

--
-- Indexes for table `tb_laporan_keuangan_zhavira`
--
ALTER TABLE `tb_laporan_keuangan_zhavira`
  ADD PRIMARY KEY (`id_laporan_zhavira`),
  ADD KEY `id_transaksi_zhavira` (`id_transaksi_zhavira`);

--
-- Indexes for table `tb_perusahaan_zhavira`
--
ALTER TABLE `tb_perusahaan_zhavira`
  ADD PRIMARY KEY (`id_perusahaan_zhavira`);

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
  ADD UNIQUE KEY `username_zhavira` (`username_zhavira`),
  ADD KEY `id_perusahaan_zhavira` (`id_perusahaan_zhavira`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_detail_transaksi_zhavira`
--
ALTER TABLE `tb_detail_transaksi_zhavira`
  MODIFY `id_detail_zhavira` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `tb_laporan_keuangan_zhavira`
--
ALTER TABLE `tb_laporan_keuangan_zhavira`
  MODIFY `id_laporan_zhavira` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_detail_transaksi_zhavira`
--
ALTER TABLE `tb_detail_transaksi_zhavira`
  ADD CONSTRAINT `tb_detail_transaksi_zhavira_ibfk_1` FOREIGN KEY (`id_transaksi_zhavira`) REFERENCES `tb_transaksi_zhavira` (`id_transaksi_zhavira`),
  ADD CONSTRAINT `tb_detail_transaksi_zhavira_ibfk_2` FOREIGN KEY (`kode_barang_zhavira`) REFERENCES `tb_barang_zhavira` (`kode_barang_zhavira`) ON DELETE CASCADE;

--
-- Constraints for table `tb_laporan_keuangan_zhavira`
--
ALTER TABLE `tb_laporan_keuangan_zhavira`
  ADD CONSTRAINT `tb_laporan_keuangan_zhavira_ibfk_1` FOREIGN KEY (`id_transaksi_zhavira`) REFERENCES `tb_transaksi_zhavira` (`id_transaksi_zhavira`);

--
-- Constraints for table `tb_transaksi_zhavira`
--
ALTER TABLE `tb_transaksi_zhavira`
  ADD CONSTRAINT `tb_transaksi_zhavira_ibfk_1` FOREIGN KEY (`id_user_zhavira`) REFERENCES `tb_user_zhavira` (`id_user_zhavira`);

--
-- Constraints for table `tb_user_zhavira`
--
ALTER TABLE `tb_user_zhavira`
  ADD CONSTRAINT `tb_user_zhavira_ibfk_1` FOREIGN KEY (`id_perusahaan_zhavira`) REFERENCES `tb_perusahaan_zhavira` (`id_perusahaan_zhavira`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
