import random

from pydantic import BaseModel, Field


class President(BaseModel):
    start: int = Field(description="Year the president started their term")
    end: int = Field(description="Year the president ended their term")
    name: str = Field(description="Name of the president")
    ordinal_number: int = Field(description="Order when they were president")

    @property
    def ordinal(self) -> str:
        """Combine the ordinal number with the suffix"""
        ordinal_str = str(self.ordinal_number)
        # 11, 12, and 13 have the suffix th:
        if self.ordinal_number in (11, 12, 13):
            return ordinal_str + "th"

        suffix = ""
        match ordinal_str[-1]:
            # Numbers that end with 1 have the suffix st
            case "1":
                suffix = "st"

            # Numbers that end with 2 have the suffix nd
            case "2":
                suffix = "nd"

            # Numbers that end with 3 have the suffix rd
            case "3":
                suffix = "rd"

            # All other numbers end with th:
            case _:
                suffix = "th"

        return ordinal_str + suffix

    def within_term(self, year: int) -> bool:
        """Check if the year is within the presidential term"""
        return self.start <= year <= self.end

    def generate_random_year(self) -> int:
        """Generate a random year that is around the presidential term"""
        return random.randint(self.start - 25, self.end + 25)

    def generate_choices(self) -> list[int]:
        """Generate four random number. Three that are not within the
        presidential term and one within"""
        choices = []
        while True:
            year = self.generate_random_year()
            # Don't duplicate years
            if year in choices:
                continue

            # Handle year within term later
            if self.within_term(year):
                continue

            # Only want 3 choices that are not within term
            choices.append(year)
            if 3 == len(choices):
                break

        # Add year that is within term
        year = random.randint(self.start, self.end)
        choices.append(year)

        # Shuffle the list of choices
        random.shuffle(choices)

        return choices

    def get_correct_year(self, curr_choices) -> int:
        """Given the random generated choices, find the one within the
        presidential term"""
        return next(year for year in curr_choices if self.within_term(year))


ALL_PRESIDENTS = [
    President(name="George Washington", start=1789, end=1797, ordinal_number=1),
    President(name="John Adams", start=1797, end=1801, ordinal_number=2),
    President(name="Thomas Jefferson", start=1801, end=1809, ordinal_number=3),
    President(name="James Madison", start=1809, end=1817, ordinal_number=4),
    President(name="James Monroe", start=1817, end=1825, ordinal_number=5),
    President(name="John Quincy Adams", start=1825, end=1829, ordinal_number=6),
    President(name="Andrew Jackson", start=1829, end=1837, ordinal_number=7),
    President(name="Martin Van Buren", start=1837, end=1841, ordinal_number=8),
    President(name="William Henry Harrison", start=1841, end=1841, ordinal_number=9),
    President(name="John Tyler", start=1841, end=1845, ordinal_number=10),
    President(name="James K. Polk", start=1845, end=1849, ordinal_number=11),
    President(name="Zachary Taylor", start=1849, end=1850, ordinal_number=12),
    President(name="Millard Fillmore", start=1850, end=1853, ordinal_number=13),
    President(name="Franklin Pierce", start=1853, end=1857, ordinal_number=14),
    President(name="James Buchanan", start=1857, end=1861, ordinal_number=15),
    President(name="Abraham Lincoln", start=1861, end=1865, ordinal_number=16),
    President(name="Andrew Johnson", start=1865, end=1869, ordinal_number=17),
    President(name="Ulysses S. Grant", start=1869, end=1877, ordinal_number=18),
    President(name="Rutherford B. Hayes", start=1877, end=1881, ordinal_number=19),
    President(name="James Garfield", start=1881, end=1881, ordinal_number=20),
    President(name="Chester Arthur", start=1881, end=1885, ordinal_number=21),
    President(name="Grover Cleveland", start=1885, end=1889, ordinal_number=22),
    President(name="Benjamin Harrison", start=1889, end=1893, ordinal_number=23),
    President(name="Grover Cleveland", start=1893, end=1897, ordinal_number=24),
    President(name="William McKinley", start=1897, end=1901, ordinal_number=25),
    President(name="Theodore Roosevelt", start=1901, end=1909, ordinal_number=26),
    President(name="William Howard Taft", start=1909, end=1913, ordinal_number=27),
    President(name="Woodrow Wilson", start=1913, end=1921, ordinal_number=28),
    President(name="Warren G. Harding", start=1921, end=1923, ordinal_number=29),
    President(name="Calvin Coolidge", start=1923, end=1929, ordinal_number=30),
    President(name="Herbert Hoover", start=1929, end=1933, ordinal_number=31),
    President(name="Franklin D. Roosevelt", start=1933, end=1945, ordinal_number=32),
    President(name="Harry S. Truman", start=1945, end=1953, ordinal_number=33),
    President(name="Dwight Eisenhower", start=1953, end=1961, ordinal_number=34),
    President(name="John F. Kennedy", start=1961, end=1963, ordinal_number=35),
    President(name="Lyndon B. Johnson", start=1963, end=1969, ordinal_number=36),
    President(name="Richard Nixon", start=1969, end=1974, ordinal_number=37),
    President(name="Gerald Ford", start=1974, end=1977, ordinal_number=38),
    President(name="Jimmy Carter", start=1977, end=1981, ordinal_number=39),
    President(name="Ronald Reagan", start=1981, end=1989, ordinal_number=40),
    President(name="George Bush", start=1989, end=1993, ordinal_number=41),
    President(name="Bill Clinton", start=1993, end=2001, ordinal_number=42),
    President(name="George W. Bush", start=2001, end=2009, ordinal_number=43),
    President(name="Barack Obama", start=2009, end=2017, ordinal_number=44),
    President(name="Donald Trump", start=2017, end=2021, ordinal_number=45),
    President(name="Joe Biden", start=2021, end=2025, ordinal_number=44),
    President(name="Donald Trump", start=2025, end=2029, ordinal_number=47),
]

if __name__ == "__main__":
    first_pres = ALL_PRESIDENTS[0]
    assert first_pres.within_term(1791)
    assert not first_pres.within_term(1788)

    random_year = first_pres.generate_random_year()
    print(
        f"{random_year} within {first_pres.start} and {first_pres.end}: {first_pres.within_term(random_year)}"
    )

    choices = first_pres.generate_choices()
    print(choices)

    within_term_count = 0
    outside_term_count = 0
    for year in choices:
        if first_pres.within_term(year):
            within_term_count += 1
            print(f"{year} within {first_pres.name} term")
        else:
            outside_term_count += 1
            print(f"{year} outside {first_pres.name} term")

    assert 1 == within_term_count
    assert 3 == outside_term_count
