def create_path(path:str): 
    """
    :param path:path is the relative path from the pixel images folder
    :return: return the relative path from roots of project
    """
    return current_path + path
#a function name is before the parameters and after the def 
#function parameters: the values that the function knows, inside the parantheses
#function typehinting: tells the code that it should be a string...
#docstrings: tells what the function does, what parameters are, what it returns