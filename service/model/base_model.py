from typing import List

import dill
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

with open("data/cosine_itemknn.dill", "rb") as f:
    homework_3_model_1 = dill.load(f)

with open("data/tfidf_itemknn.dill", "rb") as f:
    homework_3_model_2 = dill.load(f)


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


def find_difference(list_1, list_2):
    difference_1 = np.setdiff1d(np.array(list_1), np.array(list_2))
    difference_2 = np.setdiff1d(array_2, array_1)
    list_difference = list(np.concatenate((difference_1, difference_2)))

    return list_difference


@app.get("/reco/{model_name}/{user_id}", response_model=RecoResponse)
async def get_reco(model_name: str, user_id: int):
    N = 10

    pop_covered = [
        10440,
        15297,
        9728,
        13865,
        2657,
        4151,
        3734,
        6809,
        4740,
        4880,
        7571,
        11237,
        8636,
        14741,
        1844,
        142,
        14431,
        7793,
        12173,
        9996,
        12192,
        11863,
        16166,
        849,
        4436,
        12360,
        13018,
        4685,
        101,
        4495,
        4457,
        341,
        14317,
        1819,
        7107,
        3182,
        16228,
        1916,
        7626,
        14703,
        7829,
        16361,
        7102,
        3076,
        6192,
        13935,
        15078,
        512,
        14470,
        11310,
        1465,
        12501,
        12995,
        8314,
        24,
        15464,
        7417,
        5411,
        9169,
        6006,
        1554,
        2720,
        1978,
        3784,
        14359,
        5658,
        10942,
        6166,
        10821,
        4718,
        12463,
        5693,
        4382,
        5732,
        741,
        5434,
        10772,
        10464,
        14526,
        11756,
        15399,
        14488,
        3935,
        1399,
        14,
        1449,
        12228,
        2722,
        3402,
        12356,
        496,
        14899,
        13159,
        14461,
        1132,
        8618,
        5023,
        11754,
        14901,
        12974,
        14245,
        16270,
        7854,
        8270,
        1287,
        4475,
        15199,
        6402,
        14120,
        657,
        1290,
        12623,
        931,
        10732,
        16509,
        12981,
        5471,
        10761,
        3804,
        13915,
        1445,
        1053,
        11312,
        12743,
        10077,
        13262,
        10073,
        7476,
        5250,
        5543,
        9070,
        10755,
        7582,
        12537,
        15997,
        15531,
        16201,
        1204,
        6162,
        12133,
        1626,
        8447,
        3095,
        11778,
        2956,
        13861,
        12770,
        4689,
        2858,
        15266,
        1131,
        1173,
        2301,
        6646,
        8373,
        4400,
        5424,
        13849,
        9342,
        6939,
        9986,
        9164,
        11640,
        13955,
        8663,
        13411,
        10281,
        9194,
        12225,
        10878,
        4946,
        3071,
        12396,
        12841,
        15915,
        4260,
        12324,
        15706,
        10436,
        11697,
        15942,
        11769,
        4702,
        16291,
        15679,
        11654,
        9811,
        7210,
        2220,
        4912,
        16447,
        7310,
        11322,
        12132,
        2358,
        12149,
        9937,
        14266,
        598,
        7662,
        7713,
        6968,
        10353,
        8580,
        11118,
        13243,
        10240,
        12820,
        5398,
        9612,
        12965,
        13653,
        5669,
        6086,
        1562,
        7825,
        6050,
        6443,
        5791,
        4716,
        10824,
        11749,
        11047,
        12275,
        6382,
        4218,
        10219,
        10680,
    ]

    if model_name == "mmm":
        rec = list(range(10))

    elif model_name == "homework_3_model_1":
        rec = homework_3_model_1.similar_items(user_id, N=N + 1)[1:]
        rec = [element[0] for element in rec]
        if len(rec) < 10:
            diff = find_difference(rec, pop_covered)
            for i in range(10 - len(rec)):
                rec.append(diff[i])

    elif model_name == "homework_3_model_2":

        rec = homework_3_model_2.similar_items(user_id, N=N + 1)[1:]
        rec = [element[0] for element in rec]
        if len(rec) < 10:
            diff = find_difference(rec, pop_covered)
            for i in range(10 - len(rec)):
                rec.append(diff[i])
    else:
        rec = list(range(10))[::-1]

    reco = RecoResponse(user_id=user_id, items=rec)

    return reco
