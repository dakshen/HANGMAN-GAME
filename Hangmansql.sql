create database hangman;
use hangman;

create table logintable(
PlayerName varchar(30),
PlayerAge int,
Score int,
Login_Date_Time datetime);

create table words(
Word varchar(30) UNIQUE NOT NULL,
Clue varchar(30) NOT NULL);


select * from logintable;
select * from words;

select playername,max(score) as Score from logintable group by playername order by max(Score) desc;