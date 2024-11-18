import joblib
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sklearn.metrics import pairwise_distances_argmin_min
import pandas as pd
model = joblib.load(r'models\DBSCAN2.joblib')
scaler = joblib.load(r'models\scaler2.joblib')
df = pd.read_csv(r"data\final_dataset.csv")
class InputFeatures(BaseModel):
    publication_date: int
    num_pages: int
    price: int
    mng_cate: int
    poet_cate: int
    hist_cate: int
    tr_cate: int
    tec_cate:int
    fan_cate:int
    pol_cate:int
    math_cate:int
    law_cate:int
    story_cate:int
    midec_cate:int
    dev_cate:int
    islam_cate:int
    IsNew:int
    hard_cvr:int
    art_cvr:int
    ppr_cvr:int
    e_cvr:int
    e:int
    ar:int

def preprocessing(input_features: InputFeatures):
    dict_f = {
        'publication_date': input_features.publication_date,
        'num_pages': input_features.num_pages,
        'price': input_features.price,
        'mng_cate': input_features.mng_cate,
        'poet_cate': input_features.poet_cate,
        'hist_cate': input_features.hist_cate,
        'tr_cate': input_features.tr_cate,
        'tec_cate': input_features.tec_cate,
        'fan_cate': input_features.fan_cate,
        'pol_cate': input_features.pol_cate,
        'math_cate': input_features.math_cate,
        'law_cate': input_features.law_cate,
        'story_cate': input_features.story_cate,
        'midec_cate': input_features.midec_cate,
        'dev_cate': input_features.dev_cate,
        'islam_cate': input_features.islam_cate,
        'IsNew': input_features.IsNew,
        'hard_cvr': input_features.hard_cvr,
        'art_cvr': input_features.art_cvr,
        'ppr_cvr': input_features.ppr_cvr,
        'e_cvr': input_features.e_cvr,
        'e': input_features.e,
        'ar': input_features.ar
        }
    # Convert dictionary values to a list in the correct order
    features_list = [dict_f[key] for key in sorted(dict_f)]
    # Scale the input features
    scaled_features = scaler.transform([list(dict_f.values())])

    return scaled_features


app = FastAPI()

# GET request
@app.get("/")
def read_root():
    return {"message": "Welcome to Tuwaiq Academy"}

# get request
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

@app.post("/predict")
async def predict(input_features: InputFeatures):
    try:
        data = preprocessing(input_features)
        # Find the closest cluster core sample for the new data
        core_samples = model.components_
        cluster_labels, _ = pairwise_distances_argmin_min(data, core_samples)
        cluster_label = model.labels_[model.core_sample_indices_[cluster_labels[0]]]
        
        # Filter the DataFrame for the cluster and return 3 samples
        cluster_df = df[df['Cluster'] == cluster_label]
        if not cluster_df.empty:
            samples = cluster_df.sample(3).to_dict(orient="records")
            titles = [sample["title"] for sample in samples]
            img_urls = [sample["image_urls"] for sample in samples]
            return {"pred": int(cluster_label), "titles": titles, "img_urls": img_urls}
        else:
            return {"pred": int(cluster_label), "message": "No samples available for this cluster"}
    except Exception as e:
        return {"error": str(e)}


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )