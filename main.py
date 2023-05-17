from joblib import load
from fastapi import FastAPI


app = FastAPI()
artists = load("artists.joblib")
venues = load("venues.joblib")
model = load("model.joblib")
csr = load("csr.joblib")


@app.get("/")
def read_root():
    return {"Result": "PA Recommender Engine"}


@app.get("/recommend-venues/{paid}")
def recommend_venues(paid: str):
    try:
        index = list(artists).index(f'{paid}')
        results = model.recommend(index, csr[index], N=10, filter_already_liked_items=True)
        ids = [result for result in results[0]]
        scores = list([result for result in results[1]])
        proposals = [{"venue": venues[ids[i]], "score": float(scores[i])} for i in range(len(ids))]
    except ValueError:
        # recommend top 10 in general
        index = -1
        proposals = [{"venue": venues[i] } for i in range(10)]
    return {"proposals": proposals}

@app.get("/recommend-artists/{paid}")
def recommend_artists(paid: str):
    try:
        index = list(venues).index(f'{paid}')
        results = model.recommend(index, csr[index], N=10, filter_already_liked_items=True)
        ids = [result for result in results[0]]
        scores = list([result for result in results[1]])
        proposals = [{"artist": artists[ids[i]], "score": float(scores[i])} for i in range(len(ids))]
    except ValueError:
        # recommend top 10 in general
        index = -1
        proposals = [{"artist": artists[i] } for i in range(10)]
    return {"proposals": proposals}