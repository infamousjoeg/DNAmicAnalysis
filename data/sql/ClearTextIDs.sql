SELECT Name, COUNT(Name) as TotalFound, PasswordLength
FROM HardCodedPasswordAccounts
WHERE NOT (Name LIKE '%*%'
		OR Name LIKE ''
		OR Name LIKE 'S-%'
		OR Name LIKE '')
GROUP BY LOWER(Name)
ORDER BY TotalFound DESC