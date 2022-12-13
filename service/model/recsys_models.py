import dill
import pandas as pd


class BaseRecSysModel:
    def __init__(self, path, name_for_bot):
        self.name_for_bot = name_for_bot
        with open(path, "rb") as f:
            self.model = dill.load(f)

    def get_rec(self, user_id):
        pass


class LightFM(BaseRecSysModel):
    def __init__(self, path, name_for_bot):
        super().__init__(path, name_for_bot)
        with open("all_dataset.dill", "rb") as f:
            self.dataset = dill.load(f)

    def get_rec(self, user_id):
        return self.model.recommend(
            pd.DataFrame([user_id])[0], self.dataset, k=10, filter_viewed=True
        )
