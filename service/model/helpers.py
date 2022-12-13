def find_difference(recs, pop_covered):
    """
    Функция ищет разницу между двумя списками. Таким образом не допускаем повторения в рекомендациях.
    """
    list_difference = [element for element in pop_covered if element not in recs]

    return list_difference


def blending(model_1, model_2, user, N, pop_covered):
    """
    Блендинг двух моделей
    Сделаем простой вариант блендинга. Объединим выдачу обеих моделей,
    отсортируем по убыванию по вторым элементам кортежей и потом возьмём первые 10 элементов.
    """

    recs_1 = model_1.similar_items(user, N + 1)[1:]
    recs_2 = model_2.similar_items(user, N + 1)[1:]
    recs = recs_1 + recs_2

    if len(recs) > 0:
        recs.sort(key=lambda x: x[1], reverse=True)
        recs_sort = [element[0] for element in recs]
        recs_one = []
        my_set = set()

        for element in recs_sort:
            if element not in my_set:
                recs_one.append(element)
                my_set.add(element)

        if len(recs_one) >= N:
            result = recs_one[:10]
        else:
            diff = find_difference(recs_one, pop_covered)
            for i in range(10 - len(recs_one)):

                recs_one.append(diff[i])
            result = recs_one

    else:
        result = list(pop_covered[:10])

    return result
