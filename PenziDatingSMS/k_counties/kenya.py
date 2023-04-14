from k_counties.read import ReadKenyanCounties

def get_counties():
    """This functions return all kenya counties in list"""
    counties = ReadKenyanCounties('k_counties/kenya_counties.txt') \
        .read_all_counties()
    return counties

def get_county_number():
    """Return number of counties in kenya"""
    return len(get_counties())

print(get_county_number())

