import pickle


def dumps(o):
    return pickle.dumps(o, pickle.HIGHEST_PROTOCOL)


def loads(s):
    return pickle.loads(s)
