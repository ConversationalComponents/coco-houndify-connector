from enum import Enum
import copy


from config import ACTIONS_MAPPING_CONFIG


# Consts.
DEFAULT_CONFIG_KEY = "default"


COCO_STANDARD_RESPONSE = {
    "action_name": "",
    "component_done": False,  # Bool
    "component_failed": False,  # Bool
    "confidence": 1,
    "out_of_context": False,  # Bool
    "response": "",
    "response_time": 0.0,
    "updated_context": {}
}


class ComponentStatus(Enum):
    DONE = "done"
    FAILED = "failed"
    OUT_OF_CONTEXT = "out_of_context"


class ResponseHandlerException(Exception):
    pass


def calculate_status_flags(json_result):
    """
    Calculate component status flags, depends on the result.

    Arguments:
        json_result: (dict) Raw JSON result.

    Returns:
        Status flags. (dict).
    """
    status = json_result.get("status")

    component_done = False
    component_failed = False
    out_of_context = False

    if status:
        if ComponentStatus(status) == ComponentStatus.DONE:
            component_done = True
        if ComponentStatus(status) == ComponentStatus.FAILED:
            component_done = True
            component_failed = True
        if ComponentStatus(status) == ComponentStatus.OUT_OF_CONTEXT:
            out_of_context = True

    return {
        "component_done": component_done,
        "component_failed": component_failed,
        "out_of_context": out_of_context
    }


# functions
def handle(session_turn, houndify_json_response, last_response, response_time_seconds=0.0):
    coco_standard_response = copy.deepcopy(COCO_STANDARD_RESPONSE)

    results = houndify_json_response.get("AllResults")

    result = results[0]

    if not result.get("Result"):
        intent = "*"
    else:
        intent = result.get("Result").get("action", "*")

    if last_response:
        coco_standard_response["component_done"] = True

    coco_standard_response["action_name"] = intent

    raw_intent_response = session_turn.get('intents').get(intent)
    intent_response = f"{raw_intent_response} ," if raw_intent_response else ""

    coco_standard_response["response"] = f"{intent_response} " \
                                         f"{session_turn.get('push-forward')}."

    coco_standard_response["response_time"] = response_time_seconds

    coco_standard_response["confidence"] = 1.0  # Default.

    return coco_standard_response
