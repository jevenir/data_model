select 
  external_ticket_id,
  avg(score) as avg_score
from autoqa_ratings_test
group by external_ticket_id
order by external_ticket_id