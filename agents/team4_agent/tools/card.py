from poker.game_models import Card

RANK = {name: rank for rank, name in Card.RANK_NAMES.items()}
SUIT = {symbol: suit for suit, symbol in Card.SUIT_SYMBOLS.items()}


def parse_card(card: str) -> Card:
    rank = RANK[card[:-1]]
    suit = SUIT[card[-1]]
    return Card(rank, suit)


def parse_cards(cards: list[str]) -> list[Card]:
    return [parse_card(card) for card in cards]
