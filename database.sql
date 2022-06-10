BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "accounts" (
	"id"	INTEGER NOT NULL,
	"email"	varchar(45),
	"mobile"	varchar(45),
	"username"	varchar(45),
	"password"	varchar(45),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "reviews" (
	"review_id"	INTEGER NOT NULL,
	"book_id"	varchar(100),
	"original_title"	varchar(100),
	"username"	varchar(45),
	"review"	varchar(100),
	"sentiment"	varchar(45),
	PRIMARY KEY("review_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "orders" (
	"order_id"	INTEGER NOT NULL,
	"productName"	TEXT,
	"subCategory"	varchar(100),
	"image_url"	varchar(100),
	"username"	varchar(45),
	"status"	varchar(45),
	"productid"	varchar(45),
	"size"	TEXT,
	"finalPrice"	TEXT,
	PRIMARY KEY("order_id" AUTOINCREMENT)
);
INSERT INTO "accounts" VALUES (1,'sahil@gmail.com','9393939293','Sahil','123');
INSERT INTO "accounts" VALUES (2,'admin@gmail.com','7972846137','admin','123');
INSERT INTO "accounts" VALUES (3,'jay@gmail.com','7972846137','jay','123');
INSERT INTO "accounts" VALUES (4,'jay1@gmail.com','9393939293','jay1','123');
INSERT INTO "accounts" VALUES (5,'new@gmail.com','9420597784','new user','123');
INSERT INTO "accounts" VALUES (6,'sahil@gmail.com','9393939293','kirtisir','123');
INSERT INTO "accounts" VALUES (7,'shraddhachobhe@gmail.com','9588669494','shraddha','1234');
INSERT INTO "accounts" VALUES (8,'fagunibhartiya@gmail.com','7887669494','Faguni','1234');
INSERT INTO "reviews" VALUES (1,'100915','The Lion, the Witch and the Wardrobe','Sahil','Good Book for reading and motivation','Positive');
INSERT INTO "reviews" VALUES (2,'8252','Farmer Boy','jay1','Good book for reading and motivation.','Positive');
INSERT INTO "reviews" VALUES (3,'8252','Farmer Boy','jay1','Bad book for reading time waste','Negative');
INSERT INTO "reviews" VALUES (4,'136251','Harry Potter and the Deathly Hallows','jay','This is sample of good comments and nice comment
','Positive');
INSERT INTO "reviews" VALUES (5,'136251','Harry Potter and the Deathly Hallows','jay','Bad review example this book is bad ','Negative');
INSERT INTO "reviews" VALUES (6,'18512','The Return of the King','kirtisir','Good book for reading
','Positive');
INSERT INTO "reviews" VALUES (7,'','','Sahil','Nice Product','Positive');
INSERT INTO "reviews" VALUES (8,'1556','Colgate Maxfresh','Sahil','Nice Product','Positive');
INSERT INTO "reviews" VALUES (9,'1682','Krack Jack Biscuit','Sahil','Nice Product','Positive');
INSERT INTO "reviews" VALUES (10,'1617','Park Avenue Storm','Sahil','Testing','Neutral');
INSERT INTO "reviews" VALUES (11,'1572','Everest chhole Masala','Sahil','nice
','Neutral');
INSERT INTO "reviews" VALUES (12,'1588','Rin Powder','Sahil','NIce Product
','Positive');
INSERT INTO "reviews" VALUES (13,'1588','Rin Powder','Sahil','Bad Product
','Negative');
INSERT INTO "reviews" VALUES (14,'1512','Nescafe Classic Coffee','shraddha','sometime nice sometime worst','Negative');
INSERT INTO "reviews" VALUES (15,'1583','Rin Big Bar','shraddha','Nice product','Positive');
INSERT INTO "reviews" VALUES (16,'1583','Rin Big Bar','shraddha','not good','Neutral');
INSERT INTO "reviews" VALUES (17,'1622','Fogg Napoleon','shraddha','Nice fragrance','Positive');
INSERT INTO "reviews" VALUES (18,'1622','Fogg Napoleon','shraddha','pleasant','Neutral');
INSERT INTO "reviews" VALUES (19,'1622','Fogg Napoleon','shraddha','I liked it so much
','Positive');
INSERT INTO "reviews" VALUES (20,'1622','Fogg Napoleon','shraddha','Too strong smell','Neutral');
INSERT INTO "reviews" VALUES (21,'1622','Fogg Napoleon','shraddha','Bad smell','Negative');
INSERT INTO "reviews" VALUES (22,'1511','Lipton green tea','shraddha','Nice product','Positive');
INSERT INTO "orders" VALUES (1,'Something Borrowed','Emily Giffin','https://images.gr-assets.com/books/1305063535l/42156.jpg','Sahil
1
','Delivered','42156','test.pdf',NULL);
INSERT INTO "orders" VALUES (2,'The Tale of Peter Rabbit','Beatrix Potter','https://images.gr-assets.com/books/1485118382l/19321.jpg','Sahil
1
','Delivered','19321','test.pdf',NULL);
INSERT INTO "orders" VALUES (3,'The Lion, the Witch and the Wardrobe','C.S. Lewis','https://images.gr-assets.com/books/1353029077l/100915.jpg','Sahil
1

','Delivered','100915','test.pdf',NULL);
INSERT INTO "orders" VALUES (4,'Farmer Boy','Laura Ingalls Wilder, Garth Williams','https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1388446891l/8252.jpg','jay1','Delivered','8252','test.pdf',NULL);
INSERT INTO "orders" VALUES (5,'Machine Learning','Sahil Sheikh','https://m.media-amazon.com/images/I/51GxW8immiL.jpg','new user','Delivered','161085','test.pdf',NULL);
INSERT INTO "orders" VALUES (6,'The Hot Zone: The Terrifying True Story of the Origins of the Ebola Virus','Richard   Preston','https://images.gr-assets.com/books/1413747743l/16213.jpg','jay','Delivered','16213','test.pdf',NULL);
INSERT INTO "orders" VALUES (7,'One Day','David Nicholls','https://images.gr-assets.com/books/1327873020l/6280118.jpg','jay','Delivered','6280118','test.pdf',NULL);
INSERT INTO "orders" VALUES (8,'Animal Farm: A Fairy Story','George Orwell','https://images.gr-assets.com/books/1424037542l/7613.jpg','jay','Delivered','7613','test.pdf',NULL);
INSERT INTO "orders" VALUES (9,'Python For Beginner','Sahil Sheikh','https://images.gr-assets.com/books/1308858322l/12691.jpg','jay','Delivered','150273','ebanking phishing 1 (1).pdf',NULL);
INSERT INTO "orders" VALUES (10,'Harry Potter and the Deathly Hallows','J.K. Rowling, Mary GrandPré','https://images.gr-assets.com/books/1474171184l/136251.jpg','jay','Delivered','136251','test.pdf',NULL);
INSERT INTO "orders" VALUES (11,'The Return of the King','J.R.R. Tolkien','https://images.gr-assets.com/books/1389977161l/18512.jpg','kirtisir','Delivered','18512','test.pdf',NULL);
INSERT INTO "orders" VALUES (12,'Shalgam / Turnip','Vegetables','http://143.110.186.55:8080/vf-api/android/productImage/Turnip/jpg','Sahil','Delivered','1194','400 gm','15.0');
INSERT INTO "orders" VALUES (13,'Tulsi Ricebran Oil','Cooking Oil','http://143.110.186.55:8080/vf-api/android/productImage/cooking-oil-250x250/png','Sahil','Delivered','1523','1 Ltr','200.0');
INSERT INTO "orders" VALUES (14,'Arial Washing Powder','Cloth Wash','http://143.110.186.55:8080/vf-api/android/productImage/Ariel Washing Powder/jpg','Sahil','Delivered','1606','1 Kg','136.0');
INSERT INTO "orders" VALUES (15,'Krack Jack Biscuit','Biscuits ,Cookies & Chocolates','http://143.110.186.55:8080/vf-api/android/productImage/Crack Jack 5 Rs/jpg','Sahil','Delivered','1682','1 pkt','10.0');
INSERT INTO "orders" VALUES (16,'Rin Powder','Cloth Wash','http://143.110.186.55:8080/vf-api/android/productImage/Rin Powder/png','Sahil','Delivered','1588','500 gm','42.0');
INSERT INTO "orders" VALUES (17,'Fogg Napoleon','Deo','http://143.110.186.55:8080/vf-api/android/productImage/Fogg Napoleon/jpg','shraddha','Delivered','1622','120 ml','199');
INSERT INTO "orders" VALUES (18,'Nescafe Classic Coffee','Tea & Coffee','http://143.110.186.55:8080/vf-api/android/productImage/Nescafe Classic/jpg','shraddha','Pending','1512','50 gm','165');
INSERT INTO "orders" VALUES (19,'Lipton green tea','Tea & Coffee','http://143.110.186.55:8080/vf-api/android/productImage/Lipton green tea/jpg','shraddha','Delivered','1511','100 gm','150');
COMMIT;
