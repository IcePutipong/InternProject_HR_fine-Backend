from fastapi import APIRouter, Depends,HTTPException, Path
from sqlalchemy.orm import Session

from utils.jwt_bearer import JWTBearer
from database.db import get_session
from schemas.auth_schema import UserLogin, UserRegister, ChangePassword
from services import auth_service

from models.user_model import AddressInfo, DeductionInfo, HiringInfo, PaymentInfo,  PersonalInfo, RegistrationAddress

from typing import List
from schemas.user_schema import EmployeeDashboardInfo, EmployeeDetails, SubmitAllInfoData, SubmitHiringInfo, SubmitPaymentInfo, SubmitUserInfo, UpdateAddressInfo, UpdateContactInfo, UpdateDeductionInfo, UpdateHiringInfo, UpdatePaymentInfo, UpdatePersonalInfo, UpdateRegistrationAddress
from schemas.optional_schema import AddCompany, AddContractType, AddDepartment, AddEmployeeType, AddPosition, AddProjectType, AddWorkingStatus, EditPosition, FetchCompany, FetchContractType, FetchDepartment, FetchEmployeeType, FetchPosition, FetchWorkingStatus, ResProjectType
from schemas.client_schema import ClientDashboardInfo, CreateClient, EditClient, GenerateClientCode
from schemas.project_schema import  GenerateProjectCode,  ProjectAllDetails, SubmitallProjectData, ProjectDashboardinfo

from services.user_service import get_all_employees_dashboard, get_employee_details_by_id, submit_all_user_data, update_contact_info, update_or_create_employee_info
from services.optional_service import add_company, add_contract_type, add_department, add_employee_type, add_position, create_project_type, edit_position, add_working_status, response_project_type, fetch_company, fetch_contract, fetch_department, fetch_emp_type, fetch_working_status, fetch_positions
from services.client_service import create_client_info, get_client_dashboard, edit_client_info
from services.project_service import generate_project_code, get_project_dashboard, get_project_details_by_id, submit_all_project_data

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
@router.post("/employee/submit-all-info", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def submit_all_info(data: SubmitAllInfoData, db: Session = Depends(get_session)):
    return submit_all_user_data(db, data)

@router.get("/employees", response_model=List[EmployeeDashboardInfo], dependencies=[Depends(JWTBearer())], tags=["Employee"])
def fetch_employee_dashboard_info(db: Session = Depends(get_session)):
    return get_all_employees_dashboard(db)

@router.get("/employee/{emp_id}", response_model=EmployeeDetails, dependencies=[Depends(JWTBearer())], tags=["Employee"])
def fetch_employee_details(emp_id: str, db: Session = Depends(get_session)):
    return get_employee_details_by_id(db, emp_id)

@router.put("/personal-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_personal_info(emp_id: str, data: UpdatePersonalInfo, db: Session = Depends(get_session)):
    return update_or_create_employee_info(db, emp_id, PersonalInfo, data.model_dump(exclude_unset=True))

@router.put("/address-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_address_info(emp_id: str, data: UpdateAddressInfo, db: Session = Depends(get_session)):
    return update_or_create_employee_info(db, emp_id, AddressInfo, data.model_dump(exclude_unset=True))

@router.put("/registration-address/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_registration_address(emp_id: str, data: UpdateRegistrationAddress, db: Session = Depends(get_session)):
    return update_or_create_employee_info(db, emp_id, RegistrationAddress, data.model_dump(exclude_unset=True))

@router.put("/contact-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_contact_info(emp_id: str, data: UpdateContactInfo, db: Session = Depends(get_session)):
    return update_contact_info(db, emp_id, data.model_dump(exclude_unset=True))

@router.put("/hiring-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_hiring_info(emp_id: str, data: UpdateHiringInfo, db: Session = Depends(get_session)):
    return update_or_create_employee_info(db, emp_id, HiringInfo, data.model_dump(exclude_unset=True))

@router.put("/payment-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_payment_info(emp_id: str, data: UpdatePaymentInfo, db: Session = Depends(get_session)):
    return update_or_create_employee_info(db, emp_id, PaymentInfo, data.model_dump(exclude_unset=True))

@router.put("/deduction-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_deduction_info(emp_id: str, data: UpdateDeductionInfo, db: Session = Depends(get_session)):
    return update_or_create_employee_info(db, emp_id, DeductionInfo, data.model_dump(exclude_unset=True))


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
@router.get("/clients", response_model=List[ClientDashboardInfo], dependencies=[Depends(JWTBearer())], tags=["Client"])
def fetch_clients_dashboard_info(db: Session = Depends(get_session)):
    return get_client_dashboard(db)

@router.put("/client/edit-client", dependencies=[Depends(JWTBearer())], tags=["Client"])
def edit_client_endpoint(request: EditClient, db: Session=Depends(get_session)):
    return edit_client_info(request, db)

@router.post("/client/add-client", dependencies=[Depends(JWTBearer())], tags=["Client"])
def add_client_endpoint(client: CreateClient, session: Session = Depends(get_session)):
    try:
        return create_client_info(client, session)
    except HTTPException as http_err:
        raise http_err  
    except Exception as e:
        import traceback
        print("❌ Error occurred:", e)
        print(traceback.format_exc())
        session.rollback()  
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



###Project
@router.post("/project/generate-project-code", dependencies=[Depends(JWTBearer())], tags=["Project"])
def res_generate_project_code(request:GenerateProjectCode, db: Session = Depends(get_session)):
    return generate_project_code(request, db)

@router.post("/project/submit-projects-info", dependencies=[Depends(JWTBearer())], tags=["Project"])
def res_submit_all_project_data(request: SubmitallProjectData, db: Session = Depends(get_session)):
    return submit_all_project_data(db, request)

@router.get("/projects", response_model=List[ProjectDashboardinfo], dependencies=[Depends(JWTBearer())], tags=["Project"])
def fetch_project_dashboard_info(db: Session = Depends(get_session)):
    return get_project_dashboard(db)

@router.get("/projects/{project_id}", response_model=ProjectAllDetails, dependencies=[Depends(JWTBearer())], tags=["Project"])
def fetch_project_details(project_id: int, db: Session = Depends(get_session)):
    print(f"Fetching project details for project_id: {project_id}")
    return get_project_details_by_id(db, project_id)