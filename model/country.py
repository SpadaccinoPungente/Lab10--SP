from dataclasses import dataclass

@dataclass(frozen=True)
class Country:
    CCode: int # Primary key
    StateAbb: str
    StateNme: str

    def __str__(self):
        return self.StateNme