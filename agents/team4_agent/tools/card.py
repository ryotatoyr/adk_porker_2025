from .poker.game_models import Card
from .poker.evaluator import HandEvaluator

RANK = {name: rank for rank, name in Card.RANK_NAMES.items()}
SUIT = {symbol: suit for suit, symbol in Card.SUIT_SYMBOLS.items()}


def parse_card(card: str) -> Card:
    rank = RANK[card[:-1]]
    suit = SUIT[card[-1]]
    return Card(rank, suit)


def parse_cards(cards: list[str]) -> list[Card]:
    return [parse_card(card) for card in cards]


def get_hand_rank(hands: list[str], community: list[str]) -> str:
    """
    現在の状況で完成している手札の役を求める。
    Args:
        hands (list[str]): 自身のカード (2枚)
        community (list[str]): 場のカード (3, 4枚)
    Return:
        現在よりも強い役にそれぞれ対するouts数の辞書
        現在よりも弱い役については記述しない
    """
    print(hands, community)
    hands = parse_cards(hands)
    community = parse_cards(community)
    result = HandEvaluator.evaluate_hand(hands, community)
    return str(result)
