from ..livecoder import LiveCoder
from ..models import LiveCodeRequest

livecoder = LiveCoder()


def code(request: LiveCodeRequest):

    # message = {
    #     "message": request.message,
    #     "attachments": request.attachments,
    # }
    response = livecoder(request.message, session_id=request.session_id)

    return response
