query_countries_info = """
query CountriesInfo {
  countries(filter: { continent: { eq: "SA" } }) {
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