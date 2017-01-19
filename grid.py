from zone import Zone

class Grid():
    x1 = -180
    x2 = 180
    y1 = -90
    y2 = 90

    def create_zones(self):
        zones = []
        g_longitudes = list(range(self.x1, self.x2))
        g_latitudes = list(range(self.y1, self.y2))

        for x_i, x in enumerate(g_longitudes):
            # Create a tuple with the actual longitude and the next one
            if x_i < len(g_longitudes) - 1:
                longitudes = (x, g_longitudes[x_i + 1])

                for y_i, y in enumerate(g_latitudes):
                    if y_i < len(g_latitudes) - 1:
                        latitudes = (y, g_latitudes[y_i + 1])
                        zone = Zone(longitudes[0], longitudes[1], latitudes[0], latitudes[1])
                        zones.append(zone)
        return zones

# DEBUG #
#grid = Grid()
#zones = grid.create_zones()
#print(zones[1].longitude, zones[-1].longitude)
