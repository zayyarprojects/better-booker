class BookingSlot:
    def __init__(self, time_str, availability, link):
        self.time_str = time_str
        self.availability = availability
        self.link = link

    def __repr__(self):
        return f"BookingSlot(time='{self.time_str}', availability={self.availability}, link='{self.link}')"
