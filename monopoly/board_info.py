# Type 0 : Property (0, name, color, cost, rent, rent1H, rent2H, rent3H, rent4H, RentHotel, costBuilding)
# Type 1 : Railroad
# Type 2 : Water Works or Electric Company
# Type 3 : Taxes
# Type 4 : Free Parking, GO
# Type 5 : Go to Jail
# Type 6 : Community Chest
# Type 7 : Chance

BOARD = [
    # [0 - 9]
    (4, "GO", "GO"),
    (0, 60, "Mediteranean Avenue", "Brown", 2, 10, 30, 90, 160, 250, 50),
    (6, "Community Chest", "Community Chest"),
    (0, 60, "Baltic Avenue", "Brown", 4, 20, 60, 180, 320, 450, 50),
    (3, 200, "Income Tax"),
    (1, 200, "Reading Railroad"),
    (0, 100, "Oriental Avenue", "Lt.Blue", 6, 30, 90, 270, 400, 550, 50),
    (7, "Chance", "Chance"),
    (0, 100, "Vermont Avenue", "Lt.Blue", 8, 40, 100, 300, 450, 600, 50),
    (0, 120, "Conneticut Avenue", "Lt.Blue", 6, 30, 90, 270, 400, 550, 50),

    # [10 - 19]
    (4, "Jail", "Jail"),
    (0, 140, "St. Charles Places", "Pink", 10, 50, 150, 450, 625, 750, 100),
    (2, 150, "Electric Company"),
    (0, 140, "States Avenue", "Pink", 10, 50, 150, 450, 625, 750, 100),
    (0, 160, "Virginia Avenue", "Pink", 12, 60, 180, 500, 700, 900, 100),
    (1, 200, "Pennysylvania Railroad"),
    (0, 180, "St. James Place", "Orange", 14, 70, 200, 550, 700, 900, 100),
    (6, "Community Chest", "Community Chest"),
    (0, 180, "Tenessee Avenue", "Orange", 14, 70, 200, 550, 700, 950, 100),
    (0, 200, "New York Avenue", "Orange", 16, 80, 220, 600, 800, 1000, 100),
    
    # [20 - 29]
    (4, "Free Parking", "Free Parking"),
    (0, 220, "Kentucky Avenue", "Red", 18, 90, 250, 700, 875, 1050, 150),
    (7, "Chance", "Chance"),
    (0, 220, "Indiana Avenue", "Red", 18, 90, 250, 700, 875, 1050, 150),
    (0, 240, "Illinois Avenue", "Red", 20, 100, 300, 750, 925, 1100, 150),
    (1, 200, "B. & O. Railroad"),
    (0, 260, "Atlantic Avenue", "Yellow", 22, 110, 330, 800, 975, 1150, 150),
    (0, 260, "Ventnor Avenue",  "Yellow", 22, 110, 330, 800, 975, 1150, 150),
    (2, 150, "Water Works"),
    (0, 280, "Marvin Gardens", "Yellow", 24, 120, 360, 850, 1025, 1200, 150),

    # [30 - 39]
    (5, "Go To Jail", "Go To Jail"),
    (0, 300, "Pacific Avenue", "Green", 26, 130, 390, 900, 1100, 1275, 200),
    (0, 300, "North Carolina Avenue", "Green", 26, 130, 390, 900, 1100, 1275, 200),
    (6, "Community Chest", "Community Chest"),
    (0, 320, "Pennsylvania Avenue", "Green", 28, 150, 450, 1000, 1200, 1400, 200),
    (1, 200, "Short Line"),
    (7, "Chance", "Chance"),
    (0, 350, "Park Place", "Blue", 35, 175, 500, 1100, 1300, 1500, 200),
    (3, 100, "Luxury Tax"),
    (0, 400, "Boardwalk", "Blue", 50, 200, 600, 1400, 1700, 2000, 200),
]