-- inserting users
INSERT INTO users (username, hashed_password)
VALUES 
    ('Alex', 'HASHED_PASSWORD_HERE'),
    ('Aseal', 'HASHED_PASSWORD_HERE'),
    ('Cory', 'HASHED_PASSWORD_HERE'),
    ('Jocelyn', 'HASHED_PASSWORD_HERE');

-- inserting scores uploaded for grading
INSERT INTO scores (scoreXML, owningUser)
VALUES
    ('uploaded XML', 'Alex'),
    ('uploaded XML', 'Alex');

-- inserting scores from music generation
INSERT INTO scores (scoreXML, owningUser, romanNumeral)
VALUES
    ('generated XML', 'Alex', 'C,I,V'),
    ('generated XML', 'Alex', 'Db,I,vi,ii,V,I');