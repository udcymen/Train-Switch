class Yard:
    def __init__(self, connection):
        self.connection = connection
        self.num_tracks = max([item for t in connection for item in t])

    def __str__(self):
        return "Yard Connections Are " + str(self.connection)


