courses = [
    "CISC-101", "CISC-102", "CISC-110", "CISC-121", "CISC-124", "CISC-151", "CISC-181", "CISC-203", "CISC-204",
    "CISC-220", "CISC-221", "CISC-223", "CISC-226", "CISC-235", "CISC-251", "CISC-271", "CISC-282", "CISC-320",
    "CISC-322", "CISC-324", "CISC-325", "CISC-326", "CISC-327", "CISC-330", "CISC-332", "CISC-335", "CISC-351",
    "CISC-352", "CISC-360", "CISC-365", "CISC-371", "CISC-422", "CISC-423", "CISC-426", "CISC-432", "CISC-434",
    "CISC-437", "CISC-447", "CISC-448", "CISC-451", "CISC-452", "CISC-453", "CISC-454", "CISC-455", "CISC-457",
    "CISC-458", "CISC-462", "CISC-465", "CISC-466", "CISC-468", "CISC-471", "CISC-472", "CISC-473", "CISC-474",
    "CISC-486", "CISC-490", "CISC-491", "CISC-492", "CISC-495", "CISC-496", "CISC-497", "CISC-498", "CISC-499",
    "CISC-500", "COCA-201", "COGS-100", "COGS-201", "COGS-499"
]

websites = []
course_url_prefix = "https://www.cs.queensu.ca/undergraduate/courses/"
for course in courses:
    websites.append(
        {
            "url": course_url_prefix+course,
            "name":course
        }
    )
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/",
    #     "name": "programs"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/major/",
    #     "name": "computing_major"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/",
    #     "name": "specializations"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/biomedical-computing.php",
    #     "name": "biomedical_computing"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/cognitive-science.php",
    #     "name": "cognitive_science"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-and-the-creative-arts.php",
    #     "name": "computing_creative_arts"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-mathematics-and-analytics.php",
    #     "name": "computing_math_analytics"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/software-design.php",
    #     "name": "software_design"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/options/artificial-intelligence.php",
    #     "name": "ai_option"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/options/biomedical-computation.php",
    #     "name": "biomedical_computation_option"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/options/fundamental-computation.php",
    #     "name": "fundamental_computation_option"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/programs/options/security.php",
    #     "name": "security_option"
    # },
    # {
    #     "url": "https://www.cs.queensu.ca/undergraduate/courses/",
    #     "name": "courses"
    # }



def get_url_from_name(name: str) -> str:
    """
    Takes a program name and returns its corresponding URL from the websites list.
    
    Args:
        name: The name identifier of the program (e.g. 'ai_option', 'computing_major')
        
    Returns:
        The URL string for that program
        
    Raises:
        ValueError: If the name is not found in the websites list
    """
    for website in websites:
        if website["name"] == name:
            return website["url"]
    raise ValueError(f"No URL found for program name: {name}")
