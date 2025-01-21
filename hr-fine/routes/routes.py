from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from utils.jwt_bearer import JWTBearer
from database.db import get_session
from schemas.auth_schema import UserLogin, UserRegister, ChangePassword
from services import auth_service

from typing import List
from schemas.user_schema import EditUserInfoData,EditPaymentinfo,EditHiringInfo
from schemas.user_schema import CreateUserInfoData, CreatePaymentinfo, CreateHiringInfo, SubmitInfoForm
from schemas.optional_schema import AddCompany, AddContractType, AddDepartment, AddEmployeeType, AddPosition, AddProjectType, AddWorkingStatus, EditPosition, FetchCompany, FetchContractType, FetchDepartment, FetchEmployeeType, FetchPosition, FetchWorkingStatus, ResProjectType
from schemas.client_schema import ClientRes, CreateClient, EditClient
from schemas.project_schema import GenerateProjectCode, GenerateProjectCodeRes

from services.user_service import create_user_payment_info, edit_hiring_info, edit_user_info    
from services.user_service import get_hiring_info, get_user_info, fetch_company, fetch_contract, fetch_department, fetch_emp_type, fetch_working_status, fetch_positions
from services.user_service import create_hiring_info, create_user_info, submit_all_user_info
from services.optional_service import add_company, add_contract_type, add_department, add_employee_type, add_position, create_project_type, edit_position, add_working_status, response_project_type
from services.client_service import create_client_info, get_client_info, edit_client_info
from services.project_service import generate_project_code

router = APIRouter(
    prefix="/hr-fine",
)


#### Auth SERVICE
@router.post("/auth/addUser", dependencies=[Depends(JWTBearer())], tags=["Auth"])
def register_user_endpoint(user: UserRegister, session: Session=Depends(get_session)):
    return auth_service.register_user(user, session)

@router.post("/auth/login", tags=["Auth"])
def login_user_endpoint(request: UserLogin, session: Session=Depends(get_session)):
    return auth_service.login_user(request, session)

@router.post("/auth/logout", tags=["Auth"])
def logout_user_endpoint(dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    return auth_service.logout_user(dependencies, session)

@router.post("/auth/change-password", dependencies=[Depends(JWTBearer())], tags=["Auth"])
def change_password_endpoint(request: ChangePassword, session: Session=Depends(get_session), current_user: dict = Depends(JWTBearer)):
    user_id = current_user["sub"]
    return auth_service.change_password(user_id,request, session)

@router.post("/auth/change-temp-password", dependencies=[Depends(JWTBearer())], tags=["Auth"])
def change_temp_password_endpoint(emp_id: str, new_password: str, session: Session = Depends(get_session)):
    return auth_service.change_temporary_password(emp_id, new_password, session)

@router.post("/auth/refresh-token", tags=["Auth"])
def refresh_token_endpoint(refresh_token: str, session: Session= Depends(get_session)):
    return auth_service.access_refresh_token(refresh_token, session)

####User SERVICE
@router.post("/user/add-user-info", dependencies=[Depends(JWTBearer())], tags=["User Info"])
def create_user_info_endpoint(request: CreateUserInfoData, db: Session = Depends(get_session)):
    return create_user_info(request, db)

@router.post("/user/add-hiring-info", dependencies=[Depends(JWTBearer())], tags=["Hiring Info"])
def create_hiring_info_endpoint(request: CreateHiringInfo, db: Session = Depends(get_session)):
    return create_hiring_info(request, db)

@router.post("/user/add-payment-info", dependencies=[Depends(JWTBearer())], tags=["Payment Info"])
def create_payment_info_endpoint(request: CreatePaymentinfo, db: Session= Depends(get_session)):
    return create_user_payment_info(request, db)

@router.get("/user/user-info", dependencies=[Depends(JWTBearer())], tags=["User Info"])
def get_user_info_endpoint(emp_id: str, db: Session = Depends(get_session)):
    return get_user_info(emp_id, db)

@router.get("/user/hiring-info", dependencies=[Depends(JWTBearer())], tags=["Hiring Info"])
def get_hiring_info_endpoint(emp_id: str, db: Session =Depends(get_session)):
    return get_hiring_info(emp_id, db)

@router.get("/user/payment-info", dependencies=[Depends(JWTBearer())], tags=["Payment Info"])
def get_payment_info_endpoint(emp_id: str, db: Session = Depends(get_session)):
    return get_payment_info(emp_id, db)

@router.put("/user/edit-user-info", dependencies=[Depends(JWTBearer())], tags=["User Info"])
def edit_user_info_endpoint(request: EditUserInfoData, db: Session = Depends(get_session)):
    return edit_user_info(request, db)

@router.put("/user/edit-hiring-info", dependencies=[Depends(JWTBearer())], tags=["Hiring Info"])
def edit_hiring_info_endpoint(request: EditHiringInfo, db: Session = Depends(get_session)):
    return edit_hiring_info(request, db)

@router.put("/user/edit-payment-info", dependencies=[Depends(JWTBearer())], tags=["Payment Info"])
def edit_payment_info_endpoint(request: EditPaymentinfo, db: Session= Depends(get_session)):
    return edit_payment_info(request,db)

@router.post("/user/submit-all-user-info", dependencies=[Depends(JWTBearer())], tags=["Submit Info"])
def submit_all_user_info_endpoint(request: SubmitInfoForm, db: Session = Depends(get_session)):
    return submit_all_user_info(request, db)

###Optional Data
@router.post("/optional/add-company", dependencies=[Depends(JWTBearer())], tags=["Optional Data"])
def add_company_endpoint(request: AddCompany, db: Session = Depends(get_session)):
    return add_company(request, db)

@router.post("/optional/add-employee-type", dependencies=[Depends(JWTBearer())], tags=["Optional Data"])
def add_employee_type_endpoint(request: AddEmployeeType, db: Session= Depends(get_session)):
    return add_employee_type(request, db)   

@router.post("/optional/add-contract-type", dependencies=[Depends(JWTBearer())], tags=["Optional Data"])
def add_contract_type_endpoint(request: AddContractType, db: Session= Depends(get_session)):
    return add_contract_type(request, db)   

@router.post("/optional/add-department", dependencies=[Depends(JWTBearer())], tags=["Optional Data"])
def add_department_endpoint(request: AddDepartment, db: Session= Depends(get_session)):
    return add_department(request, db)   

@router.post("/optional/add-position", dependencies=[Depends(JWTBearer())], tags=["Optional Data"])
def add_position_endpoint(request: AddPosition, db: Session= Depends(get_session)):
    return add_position(request, db)

@router.post("/optional/add-working-status", dependencies=[Depends(JWTBearer())], tags=["Optional Data"])
def add_working_status_endpoint(request: AddWorkingStatus, db: Session= Depends(get_session)):
    return add_working_status(request, db)

@router.post("/optional/add-project-types", dependencies=[Depends(JWTBearer())], tags=["Optional Data"])
def add_project_types(request: AddProjectType, db: Session= Depends(get_session)):
    return create_project_type(request, db)

@router.put("/optional/edit_position", dependencies=[Depends(JWTBearer())], response_model=dict, tags=["Optional Data"])
def edit_position_endpoint(request: EditPosition, db: Session = Depends(get_session)):
    return edit_position(request, db)

@router.get("/optional/companies", dependencies=[Depends(JWTBearer())], response_model=List[FetchCompany], tags=["Optional Data"])
def fetch_company_endpoint(db: Session =Depends(get_session)):
    return fetch_company(db)

@router.get("/optional/employee-types", dependencies=[Depends(JWTBearer())], response_model=List[FetchEmployeeType], tags=["Optional Data"])
def fetch_employee_type_endpoint(db: Session =Depends(get_session)):
    return fetch_emp_type(db)

@router.get("/optional/contract-types", dependencies=[Depends(JWTBearer())], response_model=List[FetchContractType], tags=["Optional Data"])
def fetch_contract_type_endpoint(db: Session =Depends(get_session)):
    return fetch_contract(db)

@router.get("/optional/departments", dependencies=[Depends(JWTBearer())], response_model=List[FetchDepartment], tags=["Optional Data"])
def fetch_department_endpoint(db: Session =Depends(get_session)):
    return fetch_department(db)

@router.get("/optional/working-status", dependencies=[Depends(JWTBearer())], response_model=List[FetchWorkingStatus], tags=["Optional Data"])
def fetch_working_status_endpoint(db: Session =Depends(get_session)):
    return fetch_working_status(db)

@router.get("/optional/positions", dependencies=[Depends(JWTBearer())], response_model=List[FetchPosition], tags=["Optional Data"])
def fetch_position_endpoint(db: Session= Depends(get_session)):
    return fetch_positions(db)

@router.get("/optional/project-types", dependencies=[Depends(JWTBearer())], response_model=List[ResProjectType], tags=["Optional Data"])
def response_project_types(db: Session = Depends(get_session)):
    return response_project_type(db)

### Client
@router.post("/client/add-client", dependencies=[Depends(JWTBearer())], tags=["Client"])
def add_client_endpoint(client: CreateClient, session: Session=Depends(get_session)):
    return create_client_info(client, session)

@router.put("/client/edit-client", dependencies=[Depends(JWTBearer())], tags=["Client"])
def edit_client_endpoint(request: EditClient, db: Session=Depends(get_session)):
    return edit_client_info(request, db)

@router.get("/client/fetch-client", dependencies=[Depends(JWTBearer())], tags=["Client"])
def fetch_client_endpoint(client_id:int, db: Session= Depends(get_session)):
    return get_client_info(client_id, db)

###Project
@router.post("/project/generate_projecet_code", dependencies=[Depends(JWTBearer())], tags=["Project"])
def res_generate_project_code(request:GenerateProjectCode, db: Session = Depends(get_session)):
    return generate_project_code(request, db)