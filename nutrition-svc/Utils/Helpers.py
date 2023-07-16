import json

from Common.Exceptions import MissingBodyParameter, InvalidBodyParameter


def flatten_json(json_objects) -> json:
    if len(json_objects) < 1:
        return json_objects

    if len(json_objects) == 1:
        return json_objects[0]

    for jsn in json_objects[1:]:
        for key in json_objects[0]:
            if not isinstance(jsn[key], str):
                json_objects[0][key] += jsn[key]

    fjson = json_objects[0]
    return fjson


def arg_parser(parser, argument_list: dict[str, type]) -> dict[str, str | int]:
    """
    can raise TypeError or
    :param parser:
    :param argument_list:
    :return:
    """
    for arg, details in argument_list.items():
        parser.add_argument(arg)
    args = parser.parse_args()

    for arg_name, arg_value in args.items():
        if arg_value is None:
            raise MissingBodyParameter()

        try:
            expected_type = argument_list[arg_name]
            if expected_type is int:
                args[arg_name] = int(arg_value)

        except ValueError:
            raise InvalidBodyParameter()

    return args


def calc_round_sum(parameter: str, dishes_data: list) -> float:
    epsilon = 0.01
    value = sum([round(dish[parameter], 3) for dish in dishes_data])

    if value <= epsilon:
        return int(0)

    return value
