CREATE TABLE users (
    username VARCHAR(80) PRIMARY KEY,
    hashed_password VARCHAR(80) NOT NULL -- hashed w/ salt 
);

CREATE TABLE scores (
    scoreID INT AUTO_INCREMENT PRIMARY KEY,
    scoreXML VARCHAR(10922) NOT NULL, -- Assuming UTF-8 encoding (3 bytes per character)
    romanNumeral VARCHAR(80) NULL, -- format = r"<key>,<roman>(,<roman>)*"
    owningUser VARCHAR(80) NULL,
    FOREIGN KEY (owningUser) REFERENCES users(username)
);

