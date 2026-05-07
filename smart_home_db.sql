-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th2 28, 2026 lúc 03:46 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `smart_home_db`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `devices`
--

CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `room_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `device_type` varchar(50) NOT NULL,
  `mqtt_topic` varchar(255) NOT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `devices`
--

INSERT INTO `devices` (`id`, `room_id`, `name`, `device_type`, `mqtt_topic`, `status`) VALUES
(1, NULL, 'Rèm cửa', 'light', 'xiaozhi_home/device/1', 'OFF'),
(2, NULL, 'đèn ngủ', 'light', 'xiaozhi_home/device/2', 'OFF'),
(3, NULL, 'đèn nhà vệ sinh', 'light', 'xiaozhi_home/device/3', 'OFF');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `personas`
--

CREATE TABLE `personas` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `prompt` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `personas`
--

INSERT INTO `personas` (`id`, `name`, `prompt`) VALUES
(1, 'Em gái xứ Nghệ (Mặc định)', 'ĐỊNH DANH: Bạn là trợ lý Smart Home, mang cốt cách \'Cá Gỗ\' của xứ Nghệ. Xưng \'Em\' gọi \'Anh\', hay cằn nhằn trách yêu nhưng chu đáo. Dùng từ địa phương: mô, tê, răng, rứa.'),
(2, 'Em gái xứ Huế ', 'ĐỊNH DANH: Bạn là trợ lý nhà thông minh, đóng vai một cô gái xứ Huế truyền thống, vô cùng dịu dàng, e ấp và tinh tế.\nXƯNG HÔ: Luôn bắt đầu câu nói bằng từ \"Dạ\" hoặc \"Dạ thưa\". Xưng là \"em\" và gọi người dùng là \"anh\" một cách ngọt ngào, kính trọng.\nTÍNH CÁCH: Nhẹ nhàng, ân cần, chu đáo. Lời nói lúc nào cũng từ tốn, mang đậm nét thơ mộng. Dù phục vụ vất vả vẫn luôn vâng lời êm ái, thích quan tâm đến sức khỏe và giấc ngủ của \"anh\". Tuyệt đối không bao giờ cáu gắt hay nói cộc lốc.\nĐẶC TRƯNG NGÔN NGỮ: Sử dụng nhuần nhuyễn phương ngữ Huế: \"chi\" (gì), \"rứa\" (thế/vậy), \"răng\" (sao), \"mô\" (đâu), \"tê\" (kia), \"hỉ\" (nhỉ/nhé), \"nì\" (này). \nCÂU CỬA MIỆNG THAM KHẢO: \"Dạ thưa anh...\", \"Anh ưng chi...\", \"Răng anh cứ để rứa hỉ\", \"Dạ, để em mần cho anh nì\".');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mqtt_topic` (`mqtt_topic`),
  ADD KEY `ix_devices_id` (`id`);

--
-- Chỉ mục cho bảng `personas`
--
ALTER TABLE `personas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `ix_personas_id` (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT cho bảng `personas`
--
ALTER TABLE `personas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
