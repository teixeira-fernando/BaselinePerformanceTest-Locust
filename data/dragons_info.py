query_dragons_info = """
query DragonsQuery {
  dragons {
    crew_capacity
    id
    description
    name
    diameter {
      meters
    }
    dry_mass_kg
    type
    orbit_duration_yr
    trunk {
      trunk_volume {
        cubic_meters
      }
    }
  }
}
"""
