from fastapi import FastAPI,Path,HTTPException,Query
#with help of Path parameter we can add more validation and make it more readable
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated,Literal,Optional


class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID OF THE PATIENT',json_schema_extra={'example':'P001'})]
    name:Annotated[Optional[str],Field(...,description='A NAME OF THE PATEINT')]
    city:Annotated[Optional[str],Field(...,description='NAME OF THE CITY PATIENT BELONG')]
    age:Annotated[Optional[int],Field(...,gt=0 ,lt=120,description='A AGE OF THE PATIENT')]
    gender:Annotated[Optional[Literal['male',"female","other"]],Field(...,description='PATIENT GENDER')]
    height:Annotated[Optional[float],Field(...,description="HEIGTH OF THE PATIENT IN METERS")]
    weight:Annotated[Optional[float],Field(...,description='WEIGHT OF THE PATIENT IN KGS')]

    @computed_field
    def bmi(self) -> Optional[float]:
        if self.height is None or self.weight is None:
            return None
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    def verdict(self) -> Optional[str]:
        if self.bmi is None:
            return None
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(gt=0 ,lt=120,default=None)]
    gender:Annotated[Optional[Literal['male',"female","other"]],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]


def load_data():
    
    with open('patient_clone.json',"r") as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patient_clone.json','w') as f:
        json.dump(data,f)


app = FastAPI()
@app.get('/')
def hello():
    return {"message": "PATIENTS MANAGEMENT SYSTEM"}
    
@app.get('/view')
def view_data():
    data=load_data()
    return data

@app.get('/about')
def about():
    return {"message": "This is a simple FastAPI application."}

#path parameter example-->
@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,title  ="Patient ID",description="The ID of the patient to retrieve",examples=["P001"])):

    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")
@app.get('/sort')
def sort_patients(sort_by: str = Query(...,description='The field is to sort["height","weight","bmi"] '),
                order: str =Query("asc",description="The order of sort asc or desc")):
    data=load_data()
    if sort_by not in ["height","weight","bmi"]:
        raise HTTPException(status_code=400,detail=f"Invalid sort field: {sort_by}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail=f"Invalid order value: {order}")
    order_by=False if order=="asc" else True
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=order_by)   
    return sorted_data   

@app.post('/create')
def create_patient(patient:Patient):


    #load data for compare
    data=load_data()

    #check if the patient is already exiting
    
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient is already exits')
    # new patient  add to the database
    data[patient.id]=patient.model_dump(exclude=['id'])

    # save to json file 
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created sucessfully'})


#update
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='PATIENT IS NOT IN DATABASE')

    exiting_patient_info=data[patient_id]
    update_patient_info=patient_update.model_dump(exclude_unset=True)
    for key,value in update_patient_info.items():
        exiting_patient_info[key]=value

    # Remove computed fields to avoid validation error when creating Patient object
    for field in ['bmi', 'verdict']:
        exiting_patient_info.pop(field, None)

    # exiting_patient_info --> pydantic obj --->update bmi + verdict --> pydantic obj --->dict
    exiting_patient_info['id']=patient_id
    pydantic_patient_obj=Patient(**exiting_patient_info)
    exiting_patient_info=pydantic_patient_obj.model_dump(exclude=['id'])
    data[patient_id]=exiting_patient_info

    #to save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'UPDATED SUCESSFULLY'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail='PATIENT NOT FOUND')
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted sucessfully '})    



