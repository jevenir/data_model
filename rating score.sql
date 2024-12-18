select 
  category_name,
  calc_rating,
  min_rating,
  max_rating,
  round(rating_score) as rating_score
from (
select 
   category_name,
   sum(ifnull(rating, 0) * weight) / sum(nullif(weight, 0)) calc_rating,
   min(ifnull(rating, 0)) as min_rating,
   max(ifnull(rating, 0)) as max_rating,
   case 
     when max(ifnull(rating, 0)) <> min(ifnull(rating, 0)) and (max(ifnull(rating, 0)) - min(ifnull(rating, 0))) = 0 then -1
     when max(ifnull(rating, 0)) <> min(ifnull(rating, 0)) and (max(ifnull(rating, 0)) - min(ifnull(rating, 0))) <> 0 then (sum(ifnull(rating, 0) * weight) / sum(nullif(weight, 0)) - min(ifnull(rating, 0))) *100 / (max(ifnull(rating, 0)) - min(ifnull(rating, 0)))
     when max(ifnull(rating, 0)) = min(ifnull(rating, 0)) and (max(ifnull(rating, 0)) - min(ifnull(rating, 0))) = 0 then (sum(ifnull(rating, 0) * weight) / sum(nullif(weight, 0))) *100 / (max(rating))
     else -2
   end as rating_score
from manual_rating_test
group by category_name
) sub
order by category_name
