import os
from MushroomProject import logger
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
from MushroomProject.entity.config_entity    import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    
    ## Note: You can add different data transformation techniques such as Scaler, PCA and all
    #You can perform all kinds of EDA in ML cycle here before passing this data to the model

    # I am only adding train_test_spliting cz this data is already cleaned up
    def label_encoding_to_all_feature(self):
        data = pd.read_csv(self.config.data_path)
        
        
        # converting all categorical columns to numerical
        logger.info("converting all categorical columns to numerical using LabelEncoder")

        labelencoder=LabelEncoder()
        for column in data.columns:
            data[column] = labelencoder.fit_transform(data[column])
        logger.info("Columns datatype after converting to numerical")
        logger.info(f"{data.dtypes}")
        data.to_csv(os.path.join(self.config.root_dir, "data.csv"),index=False)




    def train_test_spliting(self):
        data = pd.read_csv(self.config.root_dir+"/data.csv")

        # Split the data into training and test sets. (0.75, 0.25) split.
        train, test = train_test_split(data,random_state=42,test_size=.2)

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"),index = False)

        logger.info("Splited data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)
        