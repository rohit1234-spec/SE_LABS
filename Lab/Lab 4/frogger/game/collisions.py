"""
Collision detection for Frogger.
"""


def check_collision(frog, vehicles, cell_size=50):
    """Return True when the frog rectangle actually overlaps a vehicle rectangle."""
    frog_rect = frog.get_rect(cell_size)
    for vehicle in vehicles:
        if frog_rect.colliderect(vehicle.get_rect(cell_size)):
            return True
    return False
