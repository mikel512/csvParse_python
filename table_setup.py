import models.CompanyRecord as CompanyRecord
import models.Sales as Sales
import models.RealEstateTransaction as RealEstateTransaction
import csv
import os


# this class holds the methods to return lists of objects of the parsed csv files
class DataSetup:
    # returns a dict of table creation scripts
    @staticmethod
    def get_table_creation():
        tables = {'TechCrunchcontinentalUSA': (
            "CREATE TABLE `TechCrunchcontinentalUSA` ("
            "  `rec_no` int(11) NOT NULL AUTO_INCREMENT,"
            "  `permalink` varchar(50) NOT NULL,"
            "  `company` varchar(50) NOT NULL,"
            "  `num_empls` int(11) ,"
            "  `category` varchar(30) NOT NULL,"
            "  `city` varchar(30) NOT NULL,"
            "  `state` varchar(30) NOT NULL,"
            "  `funded_date` date NOT NULL,"
            "  `raised_amount` int(11) ,"
            "  `raised_currency` varchar(30) NOT NULL,"
            "  `round` varchar(20) NOT NULL,"
            "  PRIMARY KEY (`rec_no`)"
            ") "),
            'SalesJan2009': (
            "CREATE TABLE `SalesJan2009` ("
            "  `sale_no` int(11) NOT NULL AUTO_INCREMENT,"
            "  `transaction_date` date NOT NULL,"
            "  `product` varchar(50) NOT NULL,"
            "  `price` int(20) NOT NULL,"
            "  `payment_type` varchar(30) NOT NULL,"
            "  `name` varchar(30) NOT NULL,"
            "  `city` varchar(50) NOT NULL,"
            "  `state` varchar(30) NOT NULL,"
            "  `country` varchar(30) NOT NULL,"
            "  `account_created` date NOT NULL,"
            "  `last_login` date NOT NULL,"
            "  `latitude` int(11) ,"
            "  `longitude` int(11) ,"
            "  PRIMARY KEY (`sale_no`)"
            ") "),
            'Sacramentorealestatetransactions': (
            "CREATE TABLE `Sacramentorealestatetransactions` ("
            "  `transaction_no` int(11) NOT NULL AUTO_INCREMENT,"
            "  `street` varchar(50) NOT NULL,"
            "  `city` varchar(30) NOT NULL,"
            "  `state` varchar(30) NOT NULL,"
            "  `zip` varchar(30) NOT NULL,"
            "  `beds` int(11) ,"
            "  `baths` int(11) ,"
            "  `sq_feet` int(11) ,"
            "  `type` varchar(30) NOT NULL,"
            "  `sale_date` date NOT NULL,"
            "  `price` int(20) ,"
            "  `latitude` int(11) ,"
            "  `longitude` int(11) ,"
            "  PRIMARY KEY (`transaction_no`)"
            ")"),
            'SacramentocrimeJanuary2006': (
            "CREATE TABLE `SacramentocrimeJanuary2006` ("
            "  `crime_no` int(11) NOT NULL AUTO_INCREMENT,"
            "  `crime_date` date NOT NULL,"
            "  `address` varchar(50) NOT NULL,"
            "  `district` int(2) NOT NULL,"
            "  `beat` varchar(2) NOT NULL,"
            "  `grid` int(11) ,"
            "  `crime_description` varchar(100) NOT NULL,"
            "  `ucr_ncic_code` int(11) ,"
            "  `latitude` int(11) ,"
            "  `longitude` int(11) ,"
            "  PRIMARY KEY (`crime_no`)"
            ")")
        }
        return tables

    def get_sba_table_creation(self):
        tables = {'publisher': (
            "CREATE TABLE `publisher` ("
            "  `pub_no` int(12) NOT NULL AUTO_INCREMENT,"
            "  `name` varchar(50) NOT NULL,"
            "  PRIMARY KEY (`pub_no`)"
            ") "),
            'contact_point': (
            "CREATE TABLE `contact_point` ("
            "  `contact_no` int(12) NOT NULL AUTO_INCREMENT,"
            "  `fn` varchar(50) NOT NULL,"
            "  `has_email` varchar(50) NOT NULL,"
            "  PRIMARY KEY (`contact_no`)"
            ") "),
            'sba_entry': (
            "CREATE TABLE `sba_entry` ("
            "  `entry_no` int(12) NOT NULL AUTO_INCREMENT,"
            "  `title` varchar(50) NOT NULL,"
            "  `description` varchar(50) NOT NULL,"
            "  `modified` datetime NOT NULL,"
            "  `access_level` varchar(50) NOT NULL,"
            "  `identifier` varchar(50) NOT NULL,"
            "  `issued` datetime,"
            "  `landing_page` varchar(50),"
            "  `license` varchar(50) NOT NULL,"
            "  `publisher_no` int(12),"
            "  `accrual_periodicity` varchar(5),"
            "  `is_part_of` varchar(50),"
            "  `contact_no` int(12),"
            "  `bureau_code` varchar(30) NOT NULL,"
            "  `program_code` varchar(30) NOT NULL,"
            "  PRIMARY KEY (`entry_no`),"
            "  CONSTRAINT `publisher_ibfk_1` FOREIGN KEY (`publisher_no`) "
            "     REFERENCES `publisher` (`pub_no`) ON DELETE CASCADE,"
            "  CONSTRAINT `contactp_ibfk_1` FOREIGN KEY (`contact_no`) "
            "     REFERENCES `contact_point` (`contact_no`) ON DELETE CASCADE" 
            ") "),
            'keyword': (
            "CREATE TABLE `keyword` ("
            "  `kw_no` int(12) NOT NULL AUTO_INCREMENT,"
            "  `name` varchar(50),"
            "  PRIMARY KEY (`kw_no`)"
            ") "),
            'theme': (
            "CREATE TABLE `theme` ("
            "  `theme_no` int(12) NOT NULL AUTO_INCREMENT,"
            "  `name` varchar(50),"
            "  PRIMARY KEY (`theme_no`)"
            ") "),
            'distribution': (
            "CREATE TABLE `distribution` ("
            "  `dist_no` int(12) NOT NULL AUTO_INCREMENT,"
            "  `media_type` varchar(50),"
            "  `title` varchar(50),"
            "  `description` varchar(50),"
            "  `download_url` varchar(50),"
            "  `access_url` varchar(50),"
            "  PRIMARY KEY (`dist_no`)"
            ") "),
            'entry_distribution': (
            "CREATE TABLE `entry_distribution` ("
            "  `dist_no` int(12) NOT NULL,"
            "  `entry_no` int(12) NOT NULL,"
            "  PRIMARY KEY (`dist_no`, `entry_no`),"
            "  KEY `dist_no` (`dist_no`),"
            "  KEY `entry_no` (`entry_no`),"
            "  CONSTRAINT `entrydist_ibfk_1` FOREIGN KEY (`dist_no`) "
            "     REFERENCES `distribution` (`dist_no`) ON DELETE CASCADE,"
            "  CONSTRAINT `entrydist_ibfk_2` FOREIGN KEY (`entry_no`) "
            "     REFERENCES `sba_entry` (`entry_no`) ON DELETE CASCADE"
            ") "),
            'keyword_entry': (
            "CREATE TABLE `keyword_entry` ("
            "  `kw_no` int(12) NOT NULL,"
            "  `entry_no` int(12) NOT NULL,"
            "  PRIMARY KEY (`kw_no`, `entry_no`),"
            "  KEY `kw_no` (`kw_no`),"
            "  KEY `sba_entry` (`entry_no`),"
            "  CONSTRAINT `entrykw_ibfk_1` FOREIGN KEY (`kw_no`) "
            "     REFERENCES `keyword` (`kw_no`) ON DELETE CASCADE,"
            "  CONSTRAINT `entrykw_ibfk_2` FOREIGN KEY (`entry_no`) "
            "     REFERENCES `sba_entry` (`entry_no`) ON DELETE CASCADE"
            ") "),
            'entry_theme': (
            "CREATE TABLE `entry_theme` ("
            "  `theme_no` int(12) NOT NULL ,"
            "  `entry_no` int(12) NOT NULL ,"
            "  PRIMARY KEY (`theme_no`, `entry_no`), "
            "  KEY `theme_no` (`theme_no`),"
            "  KEY `sba_entry` (`entry_no`),"
            "  CONSTRAINT `entrytheme_ibfk_1` FOREIGN KEY (`theme_no`) "
            "     REFERENCES `theme` (`theme_no`) ON DELETE CASCADE,"
            "  CONSTRAINT `entrytheme_ibfk_2` FOREIGN KEY (`entry_no`) "
            "     REFERENCES `sba_entry` (`entry_no`) ON DELETE CASCADE"
            ") ")
        }
        return tables

