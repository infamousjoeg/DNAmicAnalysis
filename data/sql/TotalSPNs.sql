SELECT Name
FROM SPN
WHERE LastPasswordSet <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND NOT (Name LIKE '%*%'
		OR Name LIKE ''
		OR Name LIKE 'S-%')
	AND Enabled = {disabled}
ORDER BY LOWER(Name) ASC