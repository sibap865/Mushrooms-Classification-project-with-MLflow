import os
from pathlib import Path
from MushroomProject import logger
from sklearn.metrics import accuracy_score,confusion_matrix
from urllib.parse import urlparse 
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import joblib
from MushroomProject.entity.config_entity    import ModelEvaluationConfig
from MushroomProject.utils.common import save_json
class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    
    def eval_metrics(self,actual, pred):
        acc = accuracy_score(actual,pred)
        logger.info("model accuracy_score is :",acc)
        mat = confusion_matrix(actual,pred)
        logger.info("model confusion matrix is :",mat)
        return acc
    


    def log_into_mlflow(self):
        logger.info("logging data to dagshub")
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]


        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme


        with mlflow.start_run():

            predicted_qualities = model.predict(test_x)

            acc = self.eval_metrics(test_y, predicted_qualities)
            
            # Saving metrics as local
            scores = {"accuracy": acc}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("accuracy", acc)


            # Model registry does not work with file store
            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.sklearn.log_model(model, "model", registered_model_name="RandomForestModel1")
            else:
                mlflow.sklearn.log_model(model, "model")