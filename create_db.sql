
-- MySQL dump 10.13  Distrib 8.0.21, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: CPTOURNAMENT
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

drop database if exists `Restaurant`;
create database `Restaurant`;
use `Restaurant`;


drop table if exists `Customer`;
create table `Customer` (
    `CustomerID` int,
    `FName` varchar(255),
    `Minit` varchar(2),
    `LName` varchar(255),
    `Phone` varchar(15),
    primary key (`CustomerID`)
);

drop table if exists `Order_Details`;
create table `Order_Details` (
    `CustomerID` int,
    `RestaurantID` int,
    `Order_Time` time,
    `Order_Type` int,
    `Total_Price` int,
    `StaffID` int,
    `OrderID` int,
    primary key (`OrderID`)
);

drop table if exists `Expenditure`;
create table `Expenditure` (
    `RestaurantID` int,
    `Month` varchar(15),
    `Total_Profit` int,
    `Total_Expenses` int,
    `Total_Sell` int,
    primary key (`RestaurantID`, `Month`)
);

drop table if exists `Menu`;
create table `Menu` (
    `ItemID` int,
    `Item_Name` varchar(255),
    `Discount` int,
    `Price` int,
    `Availability` varchar(255),
    `RestaurantID` int,
    primary key (`ItemID`)
);

drop table if exists `Staff`;
create table `Staff` (
    `RestaurantID` int,
    `StaffID` int,
    `Contact` varchar(15),
    `FName` varchar(255),
    `MInit` varchar(3),
    `LName` varchar(255),
    `DOB` date,
    primary key (`StaffID`)
);

drop table if exists `Customer_Orders`;
create table `Customer_Orders` (
    `CustomerID` int,
    `OrderID` int,
    primary key (`CustomerID`, `OrderID`)
);

drop table if exists `Billing`;
create table `Billing` (
    `OrderID` int,
    `Payment_Method` varchar(255),
    `Payment_Status` varchar(255),
    primary key (`OrderID`)
);

drop table if exists `Restaurant`;
create table `Restaurant` (
    `RestaurantID` int,
    `Restaurant_Name` varchar(255),
    `Open_Time` time,
    `Close_Time` time,
    `Contact` varchar(15),
    `State` varchar(255),
    `District` varchar(255),
    `City` varchar(255),
    primary key (`RestaurantID`)
); 

drop table if exists `Order_Items`;
create table `Order_Items` (
    `ItemID` int,
    `OrderID` int,
    primary key (`OrderID`, `ItemID`)
);

alter table `Customer_Orders`
add foreign key (`OrderID`) references `Order_Details`(`OrderID`),
add foreign key (`CustomerID`) references `Customer`(`CustomerID`);

alter table `Order_Details`
add foreign key (`RestaurantID`) references `Restaurant`(`RestaurantID`),
add foreign key (`StaffID`) references `Staff`(`StaffID`);

alter table `Order_Items` 
add foreign key (`OrderID`) references `Order_Details`(`OrderID`),
add foreign key (`ItemID`) references `Menu`(`ItemID`);

alter table `Billing`
add foreign key (`OrderID`) references `Order_Details`(`OrderID`);

alter table `Staff`
add foreign key (`RestaurantID`) references `Restaurant`(`RestaurantID`);

alter table `Expenditure`
add foreign key (`RestaurantID`) references `Restaurant`(`RestaurantID`);

alter table `Menu` 
add foreign key (`RestaurantID`) references `Restaurant`(`RestaurantID`);








