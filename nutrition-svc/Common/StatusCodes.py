
RESPONSE_CODES = {
    "Content-Type-Exception": (0, 415),
    "Invalid-Body-Parameters": (-1, 422),
    "Resource-Already-Exists": (-2, 422),
    "Void-Query-Results": (-3, 422),
    "Out-Source-Unreachable": (-4, 504),
    "Invalid-Method": ("This method is not allowed for the requested URL", 405),
    "Resource-Does-Not-Exists": (-5, 404),
    "Dish-ID-Does-Not-Exists": (-6, 422),
    "Resource-Created-Successfully": 201,
    "Resource-Modified-Successfully": 200,
    "Resource-Deleted-Successfully": 200,
    "Resource-Get-Successfully": 200
}
