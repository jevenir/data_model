select
  reviewee_id,
  count(distinct review_id) cnt_review,
  avg(cast (score as numeric)) avg_score
from manual_reviews_test
where score <> 'score'
group by reviewee_id
having count(review_id) > 1
order by reviewee_id