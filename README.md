# TrackCoreLib

In order to solve this we will use postgress as our main database. 
For each tracking type we will create a table.
This will create smaller data sets. instead of a single large table separated by type.
now will focus on the table `exercise` with the following structure.


! This project you can run. and call the code using the attached postman file.
Please run `pip install -r requirements.txt`
and run the `app_run.py` (can open from py charm and run it)
open postman and send request to the server 

(there is no login in this example. so in the code he always assume the the user_id is 1)



# Exercise Table Definition

The `Exercise` table consists of the following columns:

| Column Name        | Type       | Constraints             | Description                                  |
|--------------------|------------|-------------------------|----------------------------------------------|
| `id`               | `Integer`  | `Primary Key`           | Unique identifier for each exercise record.  |
| `user_id`          | `Integer`  | `Not Null`              | The user this record is belong to.           |
| `type`             | `Integer`  | `Not Null`              | Type of exercise, defined by `ExerciseType`. |
| `duration_minutes` | `Integer`  | `Not Null`              | Duration of the exercise in minutes.         |
| `start_datetime`   | `DateTime` | `Not Null`              | Start date and time of the exercise.         |

### Indexes

- **INDEX_TYPE**: Index on the `type` column to improve query performance.

### ExerciseType Enum

The `ExerciseType` enum defines the following exercise types:

- `WALK` = 1
- `RUN` = 2
- `BICYCLE` = 3
- `YOGA_PILATES` = 4
- `FOOTBALL` = 5
- `BASKET_BALL` = 6
- `SWIMMING` = 7
- `AEROBIC` = 8
- `MEDITATION` = 9
- `OTHER` = 100



```python
import enum

from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import SoftDeleteMixin
from sqlalchemy import Column, Integer, Index, DateTime

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.types.int_enum import IntEnum

class Exercise(Base, SoftDeleteMixin):

    __tablename__ = 'exercise'

    INDEX_TYPE = 'index_type'

    class ExerciseType(enum.Enum):
        WALK = 1
        RUN = 2
        BICYCLE = 3
        YOGA_PILATES = 4
        FOOTBALL = 5
        BASKET_BALL = 6
        SWIMMING = 7
        AEROBIC = 8
        MEDITATION = 9
        OTHER = 100

    id = Column(Integer, primary_key=True)
    type = Column('type', IntEnum(ExerciseType), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    start_datetime = Column(DateTime, nullable=False)

    __table_args__ = (Index(INDEX_TYPE, 'type', unique=False),)
```

#### Columns: 
`id`: auto increment primary key
`type` integer, tells what is the type of the exercise. managed by the app level enum called `ExerciseType`. (Index for fast query)
`duration_minutes` length of the exercise in minutes. 
`start_datetime` date and time when the workout started.


#### API'S

!Please see the file in the project root directory. 
for `swagger` see the file under the `test` filter called `swagger.yaml`
for `postman` see the file under the `test` filter called `TrackCoreLib.postman_collection.json`


1. All. GET request to get all exercise list for a specific user.
2. Update. PUT request to update the track information. 
3. Get. GET request to return a specific item the user is viewing.
4. Create. POST request to create a new track item.


```python
import hydra
from track_core_lib import TrackCoreLib

hydra.core.global_hydra.GlobalHydra.instance().clear()
hydra.initialize(config_path='../../track_core_lib/config')

# Create a new TrackCoreLib using hydra (https://hydra.cc/docs/next/advanced/compose_api/) config
track_core_lib = TrackCoreLib(hydra.compose('track_core_lib.yaml'))
```

## License
Core-Lib in licenced under [MIT](https://github.com/shay-te/core-lib/blob/master/LICENSE)





### **Code Example**



In the example code in the link. There is a small library the implement the solution.

The soution was written with Core-Lib [https://github.com/shay-te/core-lib] an in house library we are using here. 



This library knows how to 

- register new tracking 
- store them yearly 
- search by user id and type 



https://github.com/shay-te/track-core-lib



### **API List**



**GET /api/track/<track_id: ind>**
Return track information by id



**GET /api/track/all/user/<user_id:int>**?type=?
Get all track information for this user, optional paramater the type of the track



**POST /api/track/register**
Register new track information 



### **Diagram**

![PhanoAI](./diagram.png)





