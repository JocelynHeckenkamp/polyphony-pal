-- search for scores by user
SELECT scoreXML
FROM scores
WHERE owningUser = 'Alex';

-- search for scores by roman numerals
SELECT scoreXML
FROM scores
WHERE romanNumeral = 'C,I,V';