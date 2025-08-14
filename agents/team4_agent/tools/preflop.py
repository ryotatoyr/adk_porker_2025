RANK_ORDER = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
from .starting_hand_dataset import STARTING_HAND_DATASET


def preflop(your_cards: list[str], players: list[dict]) -> float:
    """
    Placeholder function for preflop tool.
    Given the player's hole cards, this function will check the winning probability of the starting hand from starting_hand_dataset.
    引数を整形してSTARTING_HAND_DATASETからスターティングハンドの勝率を取得します。
    Args:
        your_cards: The player's hole cards.
        example: ["A♥", "K♠"]
        players: The list of players at the table.
    Returns:
        The winning probability of the starting hand.
    """
    # 2枚のカードのランクとスートを分解
    rank1, suit1 = your_cards[0][:-1], your_cards[0][-1]
    rank2, suit2 = your_cards[1][:-1], your_cards[1][-1]
    print(rank1, suit1, rank2, suit2)
    num_players = len(players)

    # ペアの場合
    if rank1 == rank2:
        return STARTING_HAND_DATASET[(rank1, rank2, "pair", num_players)]

    # ポーカーの強さ順で並べる
    if RANK_ORDER.index(rank1) < RANK_ORDER.index(rank2):
        ranks = (rank1, rank2)
    else:
        ranks = (rank2, rank1)

    # スーテッド or オフスート or combined/any
    suit_type = "suited" if suit1 == suit2 else "offsuit"
    for key_type in [suit_type, "combined", "any"]:
        key = (ranks[0], ranks[1], key_type, num_players)
        if key in STARTING_HAND_DATASET:
            return STARTING_HAND_DATASET[key]
    # 万一該当がなければKeyErrorを投げる
    raise KeyError(
        f"No winrate found for {ranks[0]}, {ranks[1]}, {suit_type}, {num_players}"
    )
