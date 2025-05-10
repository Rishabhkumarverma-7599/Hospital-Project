/* Query For Database Creation */

CREATE DATABASE hospitalDB;
USE hospitalDB;

/* Query For Patient Table */

CREATE TABLE Patient (
   		 p_id VARCHAR(20) PRIMARY KEY,
   		 name VARCHAR(50) NOT NULL,
 		  age INT NOT NULL,
                 	   gender VARCHAR(10) NOT NULL,
    		   email VARCHAR(50),
   		   aadhaar VARCHAR(20) UNIQUE
);

/* Query For Doctor Table */

CREATE TABLE Doctor (
   		     d_id VARCHAR(20) PRIMARY KEY,
    		     name VARCHAR(50) NOT NULL,
   	  	      specification VARCHAR(50) NOT NULL
             );

/* Query For Lab Assistant Table */

CREATE TABLE Lab_Assistant (
       s_id VARCHAR(20) PRIMARY KEY,
    		       name VARCHAR(50) NOT NULL,
    		       patient_name VARCHAR(50)
);

/* Query For Medicine Table */

CREATE TABLE Medicine (
    		        code VARCHAR(20) PRIMARY KEY,
    		         name VARCHAR(50) NOT NULL,
   		         p_id VARCHAR(20),
    		         FOREIGN KEY (p_id) REFERENCES Patient(p_id)
);

/* Query For Visit Table */

CREATE TABLE Visit (
   			 p_id VARCHAR(20),
   			 d_id VARCHAR(20),
    			 problem VARCHAR(100),
   			 disease VARCHAR(50),
   			 treatment VARCHAR(100),
   			 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    			 PRIMARY KEY (p_id, d_id, timestamp),
   			 FOREIGN KEY (p_id) REFERENCES Patient(p_id),
    			 FOREIGN KEY (d_id) REFERENCES Doctor(d_id)
);

/* Query For Bill Table */

CREATE TABLE Bill (
 	 		  b_id VARCHAR(20) PRIMARY KEY,
   			  p_id VARCHAR(20),
    			  p_name VARCHAR(50),
    			  cost DECIMAL(10,2) NOT NULL,
   			   code VARCHAR(20),
   			   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
   			   FOREIGN KEY (p_id) REFERENCES Patient(p_id),
   			   FOREIGN KEY (code) REFERENCES Medicine(code)
);

/* Query For Lab Test Table*/

CREATE TABLE Lab_Test (
   			     p_id VARCHAR(20),
    			     test VARCHAR(50) NOT NULL,
    			     result VARCHAR(100),
   			      PRIMARY KEY (p_id, test),
  			      FOREIGN KEY (p_id) REFERENCES Patient(p_id)
                );
