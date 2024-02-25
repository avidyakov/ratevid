class Repository:
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def update_multi(self, *args, **kwargs):
        raise NotImplementedError

    def get_last_update(self, *args, **kwargs):
        raise NotImplementedError
