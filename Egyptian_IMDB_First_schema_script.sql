CREATE DATABASE IF not exists EgyptianIMDB;
USE EgyptianIMDB;
CREATE table IF not exists user ( EmailAddress VARCHAR(255) NOT NULL,
					UserName VARCHAR(100) NOT NULL PRIMARY KEY ,
                    Gender CHAR(1) NOT NULL, 
                    date_Of_Birth date NOT NULL);
                    
                    
CREATE table IF not exists Movie( MovieName VARCHAR(255) NOT NULL ,
									ID INTEGER NOT NULL PRIMARY KEY,
									ReleaseDate DATE NOT NULL ,
									MovieDescription VARCHAR(255),
                                    Duration TIME , 
                                    TotalRevenue DECIMAL,
                                    AgeRating VARCHAR(3),
                                    PremiereDate BOOLEAN );
                                    
CREATE table IF not exists CastMember ( FullName VARCHAR(255) NOT NULL,
					ID INTEGER NOT NULL PRIMARY KEY,
					Nationality VARCHAR(100)  ,
                    BirthCountry VARCHAR(100)  ,
                    Biography VARCHAR(255)  ,
                    FacebookAccount VARCHAR(255),
                    TwitterAccount VARCHAR(255),
                    InstagramAccount VARCHAR(255),
                    date_Of_Birth date NOT NULL);
                    
                    
CREATE table IF not exists MovieGenre ( Genre VARCHAR(255),
										movieID INTEGER NOT NULL,
						FOREIGN KEY(movieID) REFERENCES Movie (ID) ON DELETE CASCADE ON UPDATE CASCADE,
                        PRIMARY KEY (Genre , movieID));
						

CREATE table IF not exists Review ( RateValue INT , 
									TextualReview VARCHAR(255),
                                    movieID INTEGER NOT NULL,
									UserName VARCHAR(100) NOT NULL , 
									FOREIGN KEY(UserName) REFERENCES user(UserName) ON DELETE CASCADE ON UPDATE CASCADE,
                                    FOREIGN KEY(movieID) REFERENCES Movie (ID) ON DELETE CASCADE ON UPDATE CASCADE,
									CONSTRAINT pk_user_movie PRIMARY KEY (UserName , movieID) ) ;





CREATE table IF not exists MovieCast( movieID INTEGER NOT NULL,
										castID INTEGER NOT NULL ,
						Role VARCHAR (10) ,
						 FOREIGN KEY(movieID) REFERENCES Movie (ID) ON DELETE CASCADE ON UPDATE CASCADE,
                         FOREIGN KEY(castID) REFERENCES CastMember (ID) ON DELETE CASCADE ON UPDATE CASCADE,
						PRIMARY KEY (castID , movieID, Role) );
                                        
                                            
											
									

