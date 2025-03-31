import pandas as pd
import joblib
import numpy as np
import os
import warnings 

warnings.filterwarnings("ignore")

# 실습3. 현재 학습된 모델인 model.pkl을 ml_model.py의 load_model() 함수에서 사용
def load_model():
    model_path = 'ml_model/model.pkl'
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    else:
        raise FileNotFoundError(f"Model file not found at {model_path}")


# 예측 결과 출력
def predict(input_values, model):
    return model.predict(np.array(input_values))