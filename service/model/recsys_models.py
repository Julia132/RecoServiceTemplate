import dill

from service.model.helpers import blending


class BaseRecSysModel:
    def __init__(self, path, name_for_bot):
        self.name_for_bot = name_for_bot
        with open(path, "rb") as f:
            self.model = dill.load(f)

    def get_rec(self, user_id):
        pass


class BlendingModel(BaseRecSysModel):
    N = 10

    def __init__(self, path, name_for_bot):
        super().__init__(path, name_for_bot)
        with open("tfidf_itemknn.dill", "rb") as f:
            self.tfidf_model = dill.load(f)

        with open("pop_covered.dill", "rb") as f:
            self.pop_covered = dill.load(f)

    def get_rec(self, user_id):
        return blending(
            self.model,
            self.tfidf_model,
            user_id,
            BlendingModel.N,
            self.pop_covered,
        )
