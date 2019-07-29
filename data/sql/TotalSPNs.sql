SELECT COUNT(Name)
FROM SPN
WHERE LastPasswordSet <= datetime('{scanDateTime}', '-90 days')
	AND NOT (Name LIKE '%*%'
		OR Name LIKE ''
		OR Name LIKE 'S-%')
	{disabled}
ORDER BY LOWER(Name) ASC