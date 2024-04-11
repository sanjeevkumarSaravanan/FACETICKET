-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 20, 2024 at 05:32 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `face_examhall`
--

-- --------------------------------------------------------

--
-- Table structure for table `fe_admin`
--

CREATE TABLE `fe_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_admin`
--

INSERT INTO `fe_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `fe_attendance`
--

CREATE TABLE `fe_attendance` (
  `id` int(11) NOT NULL,
  `regno` varchar(20) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `attendance` varchar(20) NOT NULL,
  `mask_st` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_attendance`
--

INSERT INTO `fe_attendance` (`id`, `regno`, `rdate`, `attendance`, `mask_st`) VALUES
(1, '101', '20-03-2024', 'Absent', '-');

-- --------------------------------------------------------

--
-- Table structure for table `fe_department`
--

CREATE TABLE `fe_department` (
  `id` int(11) NOT NULL,
  `department` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_department`
--

INSERT INTO `fe_department` (`id`, `department`) VALUES
(1, 'CSE'),
(2, 'IT'),
(3, 'MCA'),
(4, 'MSc'),
(5, 'BCA'),
(6, 'BSc');

-- --------------------------------------------------------

--
-- Table structure for table `fe_detect`
--

CREATE TABLE `fe_detect` (
  `id` int(11) NOT NULL,
  `regno` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `face_img` varchar(20) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_detect`
--

INSERT INTO `fe_detect` (`id`, `regno`, `name`, `face_img`, `dept`, `date_time`) VALUES
(1, '102', 'Rajan', 'd1.jpg', 'CSE', '2024-03-20 16:03:20'),
(2, '102', 'Rajan', 'd2.jpg', 'CSE', '2024-03-20 16:03:25');

-- --------------------------------------------------------

--
-- Table structure for table `fe_exam`
--

CREATE TABLE `fe_exam` (
  `id` int(11) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `exam` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_exam`
--

INSERT INTO `fe_exam` (`id`, `dept`, `exam`) VALUES
(1, 'CSE', 'Board Exam 2024');

-- --------------------------------------------------------

--
-- Table structure for table `fe_face`
--

CREATE TABLE `fe_face` (
  `id` int(11) NOT NULL,
  `vid` int(11) NOT NULL,
  `vface` varchar(30) NOT NULL,
  `mask_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_face`
--

INSERT INTO `fe_face` (`id`, `vid`, `vface`, `mask_st`) VALUES
(1, 1, 'User.1.2.jpg', 0),
(2, 1, 'User.1.3.jpg', 0),
(3, 1, 'User.1.4.jpg', 0),
(4, 1, 'User.1.5.jpg', 0),
(5, 1, 'User.1.6.jpg', 0),
(6, 1, 'User.1.7.jpg', 0),
(7, 1, 'User.1.8.jpg', 0),
(8, 1, 'User.1.9.jpg', 0),
(9, 1, 'User.1.10.jpg', 0),
(10, 1, 'User.1.11.jpg', 0),
(11, 1, 'User.1.12.jpg', 0),
(12, 1, 'User.1.13.jpg', 0),
(13, 1, 'User.1.14.jpg', 0),
(14, 1, 'User.1.15.jpg', 0),
(15, 1, 'User.1.16.jpg', 0),
(16, 1, 'User.1.17.jpg', 0),
(17, 1, 'User.1.18.jpg', 0),
(18, 1, 'User.1.19.jpg', 0),
(19, 1, 'User.1.20.jpg', 0),
(20, 1, 'User.1.21.jpg', 0),
(21, 1, 'User.1.22.jpg', 0),
(22, 1, 'User.1.23.jpg', 0),
(23, 1, 'User.1.24.jpg', 0),
(24, 1, 'User.1.25.jpg', 0),
(25, 1, 'User.1.26.jpg', 0),
(26, 1, 'User.1.27.jpg', 0),
(27, 1, 'User.1.28.jpg', 0),
(28, 1, 'User.1.29.jpg', 0),
(29, 1, 'User.1.30.jpg', 0),
(30, 1, 'User.1.31.jpg', 0),
(31, 1, 'User.1.32.jpg', 0),
(32, 1, 'User.1.33.jpg', 0),
(33, 1, 'User.1.34.jpg', 0),
(34, 1, 'User.1.35.jpg', 0),
(35, 1, 'User.1.36.jpg', 0),
(36, 1, 'User.1.37.jpg', 0),
(37, 1, 'User.1.38.jpg', 0),
(38, 1, 'User.1.39.jpg', 0),
(39, 1, 'User.1.40.jpg', 0),
(40, 1, 'User.1.41.jpg', 0),
(41, 1, 'User.1.42.jpg', 0),
(42, 1, 'User.1.43.jpg', 0),
(43, 1, 'User.1.44.jpg', 0),
(44, 1, 'User.1.45.jpg', 0),
(45, 1, 'User.1.46.jpg', 0),
(46, 1, 'User.1.47.jpg', 0),
(47, 1, 'User.1.48.jpg', 0),
(48, 1, 'User.1.49.jpg', 0),
(49, 1, 'User.1.50.jpg', 0),
(50, 1, 'User.1.51.jpg', 0),
(51, 1, 'User.1.52.jpg', 0),
(52, 1, 'User.1.53.jpg', 0),
(53, 1, 'User.1.54.jpg', 0),
(54, 1, 'User.1.55.jpg', 0),
(55, 1, 'User.1.56.jpg', 0),
(56, 1, 'User.1.57.jpg', 0),
(57, 1, 'User.1.58.jpg', 0),
(58, 1, 'User.1.59.jpg', 0),
(59, 1, 'User.1.60.jpg', 0);

-- --------------------------------------------------------

--
-- Table structure for table `fe_hall`
--

CREATE TABLE `fe_hall` (
  `id` int(11) NOT NULL,
  `hall` varchar(20) NOT NULL,
  `seats` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_hall`
--

INSERT INTO `fe_hall` (`id`, `hall`, `seats`) VALUES
(1, 'EH1', 20);

-- --------------------------------------------------------

--
-- Table structure for table `fe_register`
--

CREATE TABLE `fe_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(200) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `aadhar` varchar(20) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `year` varchar(20) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `face_st` int(11) NOT NULL,
  `fimg` varchar(30) NOT NULL,
  `otp` varchar(20) NOT NULL,
  `allow_st` int(11) NOT NULL,
  `regno` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `hall` varchar(20) NOT NULL,
  `seat` int(11) NOT NULL,
  UNIQUE KEY `regno` (`regno`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_register`
--

INSERT INTO `fe_register` (`id`, `name`, `address`, `mobile`, `email`, `aadhar`, `dept`, `year`, `rdate`, `face_st`, `fimg`, `otp`, `allow_st`, `regno`, `gender`, `dob`, `hall`, `seat`) VALUES
(1, 'Rajan', '45,FG Nagar', 9875896444, 'rajan@gmail.com', '578452155565', 'CSE', '2020-2024', '', 0, 'User.1.60.jpg', '', 0, '101', 'Male', '1999-06-05', 'EH1', 1);

-- --------------------------------------------------------

--
-- Table structure for table `fe_staff`
--

CREATE TABLE `fe_staff` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `location` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `stype` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `dept` varchar(20) NOT NULL,
  UNIQUE KEY `uname` (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_staff`
--

INSERT INTO `fe_staff` (`id`, `name`, `mobile`, `email`, `location`, `uname`, `pass`, `stype`, `rdate`, `dept`) VALUES
(1, 'Ravi', 9894442716, 'ravi@gmail.com', 'Chennai', 'S001', '123456', 'HOD', '20-03-2024', 'CSE'),
(2, 'Usha', 8856977458, 'usha@gmail.com', 'Salem', 'S002', '123456', 'Invigilator', '20-03-2024', 'CSE');

-- --------------------------------------------------------

--
-- Table structure for table `fe_timetable`
--

CREATE TABLE `fe_timetable` (
  `id` int(11) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `hall` varchar(20) NOT NULL,
  `staff` varchar(20) NOT NULL,
  `scode` varchar(20) NOT NULL,
  `subject` varchar(30) NOT NULL,
  `exam_time` varchar(20) NOT NULL,
  `edate` varchar(20) NOT NULL,
  `exam` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fe_timetable`
--

INSERT INTO `fe_timetable` (`id`, `dept`, `hall`, `staff`, `scode`, `subject`, `exam_time`, `edate`, `exam`) VALUES
(1, 'CSE', 'EH1', 'S002', 'P152001', 'Python', 'Forenoon', '20-03-2024', 'Board Exam 2024');
