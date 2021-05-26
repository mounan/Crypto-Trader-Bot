from datetime import datetime

class NoNewException(Exception):
    """[summary]

    :param Exception: [description]
    :type Exception: [type]
    """    
    def __init__(self):
        self.message = "No new tweets yet, keep tracking... " + \
            datetime.now().strftime("%Y/%m/%d/ %H:%M:%S")
    def __str__(self) -> str:
        return self.message

class RequestException(Exception):
    """[summary]

    :param Exception: [description]
    :type Exception: [type]
    """    
    def __init__(self, func_name):
        self.message = f"Function '{func_name}' requests failed, requesting agian."
    def __str__(self) -> str:
        return self.message

