import pandas as pd
from MushroomProject.entity.config_entity import DataValidationConfig
from MushroomProject  import logger

class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    def validate_all_columns(self)-> bool:
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)

            all_schema = self.config.all_schema.keys()

            
            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
            # droping nulll values column and unuseful columns
            logger.info("droping nulll values column and unuseful columns")
            data.drop(columns=["veil-type","stalk-root"],axis=1,inplace=True)
            data.to_csv(self.config.root_dir+"/mushrooms.csv",index=False)

            return validation_status
        
        except Exception as e:
            raise e