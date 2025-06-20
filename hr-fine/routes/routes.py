from datetime import date
from fastapi import APIRouter, Depends,HTTPException, Path
from sqlalchemy.orm import Session

from utils.jwt_bearer import JWTBearer, decode_jwt
from database.db import get_session
from schemas.auth_schema import ChangeTempPassRequest, ResetPasswordRequest, UserLogin, UserRegister, ChangePassword
from services import auth_service

from models.user_model import AddressInfo, DeductionInfo, HiringInfo, PaymentInfo,  PersonalInfo, RegistrationAddress

from typing import List, Optional
from schemas.user_schema import EmployeeDashboardInfo, EmployeeDetails, SubmitAllInfoData, SubmitHiringInfo, SubmitPaymentInfo, SubmitUserInfo, UpdateAddressInfo, UpdateContactInfo, UpdateDeductionInfo, UpdateHiringInfo, UpdatePaymentInfo, UpdatePersonalInfo, UpdateRegistrationAddress
from schemas.optional_schema import AddCompany, AddContractType, AddDepartment, AddEmployeeType, AddPosition, AddProjectType, AddWorkingStatus, EditPosition, FetchCompany, FetchContractType, FetchDepartment, FetchEmployeeType, FetchPosition, FetchWorkingStatus, ResProjectType
from schemas.client_schema import ClientDashboardInfo, CreateClient, EditClient, GenerateClientCode
from schemas.project_schema import  GenerateProjectCode, PlanEdit,  ProjectAllDetails, ProjectAssigned, ProjectDetailEdit, ProjectDurationEdit, ProjectMemberBase, ProjectMemberEdit, SubmitallProjectData, ProjectDashboardinfo
from schemas.timesheet_schemas import CalculateTotalTime, TimeStampBase, TimeStampResponseSchema

from services.user_service import get_all_employees_dashboard, get_employee_details_by_id, submit_all_user_data, update_address_info, update_contact_info, update_deduction_info, update_hiring_info, update_or_create_employee_info, update_payment_info, update_personal_info, update_registration_address
from services.optional_service import add_company, add_contract_type, add_department, add_employee_type, add_position, create_project_type, edit_position, add_working_status, response_project_type, fetch_company, fetch_contract, fetch_department, fetch_emp_type, fetch_working_status, fetch_positions
from services.client_service import create_client_info, get_client_dashboard, edit_client_info
from services.project_service import create_project_member, delete_project_member, fetch_managers, generate_project_code, get_project_assigned, get_project_dashboard, get_project_details_by_id, submit_all_project_data, update_member, update_plan, update_project_details, update_project_durations
from services.timesheet_service import calculate_total_time, delete_time_stamp, edit_time_stamp, fetch_time_stamps, stamp_timesheet



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
def change_temp_password_endpoint(request: ChangeTempPassRequest, session: Session = Depends(get_session)):
    return auth_service.change_temporary_password(request, session)

@router.post("/auth/reset-password", tags=["Auth"])
def reset_password_endpoint(request: ResetPasswordRequest, db: Session = Depends(get_session)):
    return auth_service.reset_password(request, db)

@router.post("/auth/refresh-token", tags=["Auth"])
def refresh_token_endpoint(refresh_token: str, session: Session= Depends(get_session)):
    return auth_service.access_refresh_token(refresh_token, session)

@router.post("/auth/reset-token", tags=["Auth"])
def reset_password_endpoint(request: ResetPasswordRequest, db: Session = Depends(get_session)):
    return auth_service.reset_password(request, db)

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
    return update_personal_info(db, emp_id, data.model_dump(exclude_unset=True))

@router.put("/address-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_address_info(emp_id: str, data: UpdateAddressInfo, db: Session = Depends(get_session)):
    return update_address_info(db, emp_id, data.model_dump(exclude_unset=True))

@router.put("/registration-address/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_registration_address(emp_id: str, data: UpdateRegistrationAddress, db: Session = Depends(get_session)):
    return update_registration_address(db, emp_id, data.model_dump(exclude_unset=True))

@router.put("/contact-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_contact_info(emp_id: str, data: UpdateContactInfo, db: Session = Depends(get_session)):
    return update_contact_info(db, emp_id, data.model_dump(exclude_unset=True))

@router.put("/hiring-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_hiring_info(emp_id: str, data: UpdateHiringInfo, db: Session = Depends(get_session)):
    return update_hiring_info(db, emp_id, data.model_dump(exclude_unset=True))

@router.put("/payment-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_payment_info(emp_id: str, data: UpdatePaymentInfo, db: Session = Depends(get_session)):
    return update_payment_info(db, emp_id, data.model_dump(exclude_unset=True))

@router.put("/deduction-info/{emp_id}", dependencies=[Depends(JWTBearer())], tags=["Employee"])
def edit_deduction_info(emp_id: str, data: UpdateDeductionInfo, db: Session = Depends(get_session)):
    return update_deduction_info(db, emp_id, data.model_dump(exclude_unset=True))

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

@router.post("project/add-project-member/{project_id}", dependencies=[Depends(JWTBearer())], tags=["Project"])
def add_project_member(
    project_id: int, 
    member_data: ProjectMemberBase, 
    db: Session = Depends(get_session)
):
    try:
        added_member = create_project_member(db, project_id, member_data.model_dump())
        return {
            "status": "success",
            "message": "Project member added successfully",
            "data": added_member.__dict__
        }
    except HTTPException as e:
        return {"status": "error", "message": str(e.detail)}

@router.get("/projects", response_model=List[ProjectDashboardinfo], dependencies=[Depends(JWTBearer())], tags=["Project"])
def fetch_project_dashboard_info(db: Session = Depends(get_session)):
    return get_project_dashboard(db)

@router.get("/projects/{project_id}", response_model=ProjectAllDetails, dependencies=[Depends(JWTBearer())], tags=["Project"])
def fetch_project_details(project_id: int, db: Session = Depends(get_session)):
    print(f"Fetching project details for project_id: {project_id}")
    return get_project_details_by_id(db, project_id)

@router.get("/managers", dependencies=[Depends(JWTBearer())], tags=["Project"])
def get_managers(db: Session = Depends(get_session)):
    return fetch_managers(db)

@router.get("/timesheet/projects", response_model=List[ProjectAssigned], tags=["Project"])
def get_assigned_projects(
    db: Session = Depends(get_session),
    auth: str = Depends(JWTBearer())
):
    try:
        return get_project_assigned(db, auth)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/edit-project-details/{project_id}", dependencies=[Depends(JWTBearer())], tags=["Project"])
def edit_project_details(
    request: ProjectDetailEdit,
    project_id: int,
    db: Session = Depends(get_session),
):
    return update_project_details(project_id,request, db)

@router.put("/edit-project-durations/{project_id}", dependencies=[Depends(JWTBearer())], tags=["Project"])
def edit_project_durations(
    request: ProjectDurationEdit,
    project_id: int,
    db: Session = Depends(get_session),
):
    return update_project_durations(project_id,request, db)

@router.put("/edit_plan/{project_id}", dependencies=[Depends(JWTBearer())], tags=["Project"])
def edit_plan(
    request: PlanEdit,
    project_id: int,
    db: Session = Depends(get_session)
): 
    return update_plan(project_id,request, db)


@router.put("/edit-member/{project_member_id}", dependencies=[Depends(JWTBearer())], tags=["Project"])
def edit_member(
    request: ProjectMemberEdit,
    project_member_id: int,
    db: Session = Depends(get_session)
):
    return update_member(project_member_id, request, db)

@router.delete("/delete_member/{project_id}/{project_member_id}", dependencies=[Depends(JWTBearer())], tags=["Project"])
def delete_member(
    project_id: int,
    project_member_id: int,
    db:Session = Depends(get_session)
):
    return delete_project_member(project_id, project_member_id, db)



##Time Stamp
@router.post("/time-stamp/submit-time-stamp", dependencies=[Depends(JWTBearer())], tags=["TimeStamp"])
def submit_time_stamp(request: TimeStampBase, db: Session = Depends(get_session), token: str = Depends(JWTBearer())):
    """Extracts emp_id from the decoded JWT token and submits a time stamp."""

    decoded_token = decode_jwt(token)  

    emp_id = decoded_token.get("emp_id") 
    if not emp_id:
        raise HTTPException(status_code=400, detail="Invalid token: Missing emp_id")

    return stamp_timesheet(request, emp_id, db)  

@router.put("/time-stamp/edit-time-stamp/{stamp_id}", tags=["TimeStamp"])
def edit_time_stamp_endpoint(stamp_id: int, stamp_data: TimeStampBase, db: Session = Depends(get_session), auth: str = Depends(JWTBearer())):
    return edit_time_stamp(stamp_id, stamp_data, db, auth)

@router.delete("/time-stamp/delete-time-stamp/{stamp_id}", tags=["TimeStamp"])
def delete_time_stamp_endpoint(stamp_id: int, db: Session = Depends(get_session), auth: str = Depends(JWTBearer())):
    return delete_time_stamp(stamp_id, db, auth)

@router.get("/time-stamp/fetch-time-stamps", tags=["TimeStamp"])
def fetch_time_stamps_endpoint(
    db: Session = Depends(get_session),
    auth: str = Depends(JWTBearer()),
    target_date: Optional[date] = None,
):
    return fetch_time_stamps( db, auth, target_date)

@router.post("/time-stamp/calculate-total-time", tags=["TimeStamp"])
def calculate_total_time_endpoint(
    request: CalculateTotalTime,
    db: Session = Depends(get_session)
):
    return calculate_total_time(request, db)