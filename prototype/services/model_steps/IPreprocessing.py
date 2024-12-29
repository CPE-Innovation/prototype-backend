from abc import abstractmethod

class IPreprocessing:
    @abstractmethod
    def preprocess(api_url, params):
        pass
