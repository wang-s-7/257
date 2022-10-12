--for all nocs: 
SELECT * FROM nocs
ORDER BY nocs.abbreviation;

--for jamaican athletes:
SELECT DISTINCT athletes.name, nocs.name 
FROM athletes, nocs, event_results
WHERE athletes.id = event_results.athlete_id
AND nocs.id = event_results.noc_id
AND nocs.name = 'Jamaica';

--for louganis medals:
SELECT athletes.name, events.name, games.year, games.season, event_results.medal
FROM athletes, events, games, event_results
WHERE athletes.id = event_results.athlete_id
AND events.id = event_results.event_id
AND games.id = event_results.game_id
AND athletes.name LIKE '%Louganis%'
AND event_results.medal IS NOT NULL
ORDER BY games.year;

--for nocs' medal counts, descending order (does not show nocs with zero medals)
SELECT COUNT(event_results.medal), nocs.name
FROM nocs, event_results
WHERE nocs.id = event_results.noc_id
AND event_results.medal = 'Gold'
GROUP BY nocs.name
ORDER BY COUNT(event_results.medal) DESC;





