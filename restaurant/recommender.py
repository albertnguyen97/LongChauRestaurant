import redis
from django.conf import settings
from warehouse.models import Dish

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


class Recommender:
    def get_dish_key(self, id):
        return f'dish:{id}:purchased_with'

    def dishes_bought(self, dishes):
        dishe_ids = [p.id for p in dishes]
        for dish_id in dishe_ids:
            for with_id in dishe_ids:
                # get the other products bought with each product
                if dish_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(
                        self.get_dish_key(dish_id), 1, with_id
                    )

    def clear_purchases(self):
        for id in Dish.objects.values_list('id', flat=True):
            r.delete(self.get_dish_key(id))

    def suggest_dishes_for(self, dishes, max_results=6):
        dish_ids = [p.id for p in dishes]
        if len(dishes) == 1:
            # only 1 product
            suggestions = r.zrange(
                self.get_dish_key(dish_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in dish_ids])
            tmp_key = f'tmp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_dish_key(id) for id in dish_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *dish_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(
                tmp_key, 0, -1, desc=True
            )[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_dish_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_dishes = list(
            Dish.objects.filter(id__in=suggested_dish_ids)
        )
        suggested_dishes.sort(
            key=lambda x: suggested_dish_ids.index(x.id)
        )
        return suggested_dishes
