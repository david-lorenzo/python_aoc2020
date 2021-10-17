from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

class Parse(Enum):
    FIELD_RULES = auto()
    YOUR_TICKET = auto()
    OTHER_TICKETS = auto()


@dataclass
class Rule:
    low: int
    high: int


@dataclass
class Field:
    name: str
    first: Rule
    second: Rule
    def check(self, v):
        return (self.first.low <= v <= self.first.high) or \
               (self.second.low <= v <= self.second.high)


def parse_rule(line):
    name, rest = line.split(":")
    r1, r2 = rest.split(" or ")
    r1 = r1.split("-")
    r2 = r2.split("-")
    R1 = Rule(low=int(r1[0]), high=int(r1[1]))
    R2 = Rule(low=int(r2[0]), high=int(r2[1]))
    return Field(name=name, first=R1, second=R2)


def parse_ticket(line):
    return [int(n) for n in line.split(",")]


data = Path("input16.txt").read_text().split("\n")

state = Parse.FIELD_RULES
fields = []
yours = None
nearby = []
for line in data:
    if line == "":
        continue
    elif state == Parse.FIELD_RULES:
        if line == "your ticket:":
            state = Parse.YOUR_TICKET
            continue
        fields.append(parse_rule(line))
    elif state == Parse.YOUR_TICKET:
        if line == "nearby tickets:":
            state = Parse.OTHER_TICKETS
            continue
        yours = parse_ticket(line)
    elif state == Parse.OTHER_TICKETS:
        nearby.append(parse_ticket(line))


def field_validator(fields):
    def _invalid_field(v):
        return not any((f.first.low <= v <= f.first.high) or \
                (f.second.low <= v <= f.second.high) for f in fields)
    return _invalid_field
def field_validator(fields):
    def _invalid_field(v):
        return not any(f.check(v) for f in fields)
    return _invalid_field


invalid_field = field_validator(fields)


def ticket_error_rate(ticket):
    return sum(n for n in ticket if invalid_field(n))


total_error_rate = sum(ticket_error_rate(t) for t in nearby)

