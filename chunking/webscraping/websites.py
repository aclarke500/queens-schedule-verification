# this will be a dictionary of all the websites we want to scrape, and the site name we want the next to have
'''
https://www.cs.queensu.ca/undergraduate/programs/specializations/
https://www.cs.queensu.ca/undergraduate/programs/specializations/biomedical-computing.php
https://www.cs.queensu.ca/undergraduate/programs/specializations/cognitive-science.php
https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-and-the-creative-arts.php
https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-mathematics-and-analytics.php
https://www.cs.queensu.ca/undergraduate/programs/specializations/software-design.php
https://www.cs.queensu.ca/undergraduate/programs/options/artificial-intelligence.php
https://www.cs.queensu.ca/undergraduate/programs/options/biomedical-computation.php
https://www.cs.queensu.ca/undergraduate/programs/options/fundamental-computation.php
https://www.cs.queensu.ca/undergraduate/programs/options/security.php
https://www.cs.queensu.ca/undergraduate/courses/
'''
websites = [
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/",
        "name": "programs"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/major/",
        "name": "computing_major"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/",
        "name": "specializations"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/biomedical-computing.php",
        "name": "biomedical_computing"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/cognitive-science.php",
        "name": "cognitive_science"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-and-the-creative-arts.php",
        "name": "computing_creative_arts"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-mathematics-and-analytics.php",
        "name": "computing_math_analytics"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/software-design.php",
        "name": "software_design"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/options/artificial-intelligence.php",
        "name": "ai_option"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/options/biomedical-computation.php",
        "name": "biomedical_computation_option"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/options/fundamental-computation.php",
        "name": "fundamental_computation_option"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/options/security.php",
        "name": "security_option"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/courses/",
        "name": "courses"
    }
]


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
