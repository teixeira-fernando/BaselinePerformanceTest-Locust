query_country_info = """
query CountryInfo {
  country(code: "BR") {
    code
    name
    capital
    continent {
      code
      name
    }
    languages {
      code
      name
    }
  }
}
"""
