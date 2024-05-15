import uvicorn
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from model import HookArgs, TemplateDynamicBody
from service import get_data_from_session

# example db to hold user data
DB = {}

# defined props in engine templates
USER_PROPS_KEY = "kProps"
ERP_PROP_KEY = "erp"
BOOKING_DATE_PROP_KEY = "bookingDate"

router = APIRouter(prefix='/chatbot')

app = FastAPI(
    title="JAWCE Chatbot",
    description="A sample chatbot connecting Python chatbot to JAWCE engine separately",
    contact={
        "name": "DonnC",
        "url": "https://docs.page/donnc/jawce",
        "email": "donnclab@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/DonnC/jawce",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.post("/get-username", response_model=HookArgs)
def tpl_get_user_name(args: HookArgs):
    print(">>> GU-Received args: ", args)

    DB['username'] = args.channelUser.name

    template = TemplateDynamicBody()
    template.renderPayload = {"user": args.channelUser.name}
    args.templateDynamicBody = template

    return args


@router.post("/confirm-booking")
def tpl_confirm_booking(args: HookArgs):
    # print(">>> Received args: {}".format(args))

    session_data = get_data_from_session(
        user=args.channelUser.waId,
        data_key=USER_PROPS_KEY
    )

    system_ = session_data.get(ERP_PROP_KEY)
    date_, time_ = session_data.get(BOOKING_DATE_PROP_KEY).split(" ")

    confirmation_text = f"You are about to book a System demo with us. " \
                        f"\\n\\nSystem: {system_}\\nDate: {date_}\\nTime: {time_}"

    template = TemplateDynamicBody()
    template.renderPayload = {"confirmation": confirmation_text}
    args.templateDynamicBody = template

    return args


@router.post("/save-booking")
def save(args: HookArgs):
    # print(">>> SB, Received args: {}".format(args))

    session_data = get_data_from_session(
        user=args.channelUser.waId,
        data_key=USER_PROPS_KEY
    )

    # add to DB
    DB.update(session_data)

    print('>>> current DB: ', DB)

    return args


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True, use_colors=True)
