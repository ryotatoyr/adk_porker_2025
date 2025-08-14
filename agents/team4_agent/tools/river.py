from itertools import combinations

# 役の強さを数値化（大きいほど強い）
HAND_RANKS = {
    "royal_flush": 10,
    "straight_flush": 9,
    "four_of_a_kind": 8,
    "full_house": 7,
    "flush": 6,
    "straight": 5,
    "three_of_a_kind": 4,
    "two_pair": 3,
    "one_pair": 2,
    "high_card": 1,
}


def card_to_tuple(card: str):
    # 例: "A♥" → ("A", "♥")
    return (card[:-1], card[-1])


def rank_to_value(rank: str):
    order = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    return order[rank]


def evaluate_hand(cards):
    # cards: [(rank, suit), ...] 5枚
    ranks = [rank_to_value(r) for r, s in cards]
    suits = [s for r, s in cards]
    rank_counts = {r: ranks.count(r) for r in set(ranks)}
    is_flush = len(set(suits)) == 1
    sorted_ranks = sorted(ranks, reverse=True)
    is_straight = False
    # ストレート判定（A-2-3-4-5も考慮）
    if len(set(ranks)) == 5:
        if max(ranks) - min(ranks) == 4:
            is_straight = True
        elif set(ranks) == {14, 2, 3, 4, 5}:
            is_straight = True
            sorted_ranks = [5, 4, 3, 2, 1]
    # ロイヤルフラッシュ
    if is_flush and set(sorted_ranks) == {14, 13, 12, 11, 10}:
        return (HAND_RANKS["royal_flush"], sorted_ranks)
    # ストレートフラッシュ
    if is_flush and is_straight:
        return (HAND_RANKS["straight_flush"], sorted_ranks)
    # フォーカード
    if 4 in rank_counts.values():
        return (HAND_RANKS["four_of_a_kind"], sorted_ranks)
    # フルハウス
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return (HAND_RANKS["full_house"], sorted_ranks)
    # フラッシュ
    if is_flush:
        return (HAND_RANKS["flush"], sorted_ranks)
    # ストレート
    if is_straight:
        return (HAND_RANKS["straight"], sorted_ranks)
    # スリーカード
    if 3 in rank_counts.values():
        return (HAND_RANKS["three_of_a_kind"], sorted_ranks)
    # ツーペア
    if list(rank_counts.values()).count(2) == 2:
        return (HAND_RANKS["two_pair"], sorted_ranks)
    # ワンペア
    if 2 in rank_counts.values():
        return (HAND_RANKS["one_pair"], sorted_ranks)
    # ハイカード
    return (HAND_RANKS["high_card"], sorted_ranks)


def river(your_cards: list[str], community: list[str]) -> float:
    """
    リバーフェーズで自分の手札2枚とコミュニティカード5枚から作れる全ての5枚役を列挙し、
    その中で自分の役（最強の5枚役）が上位何割に位置するかをfloatで返す関数。

    役の強さはポーカーの一般的な役（ロイヤルフラッシュ＞ストレートフラッシュ＞フォーカード…）で判定。
    返り値は1.0に近いほど強い役、0.0に近いほど弱い役となる。

    Args:
        your_cards (list[str]): 自分の手札2枚（例: ["A♥", "K♠"]）
        community (list[str]): コミュニティカード5枚（例: ["Q♥", "J♦", "10♣", "9♠", "6♦"]）

    Returns:
        float: 7枚から作れる全ての5枚役の中で自分の役が上位何割に入るか（1.0=最強, 0.0=最弱）
    """
    all_cards = your_cards + community
    card_tuples = [card_to_tuple(c) for c in all_cards]
    all_hands = list(combinations(card_tuples, 5))
    hand_scores = [evaluate_hand(hand) for hand in all_hands]
    # 自分の役（自分の2枚＋コミュニティ5枚から最強の5枚）
    my_best = max([evaluate_hand(hand) for hand in combinations(card_tuples, 5)])
    # 全役を強い順にソート
    sorted_scores = sorted(hand_scores, reverse=True)
    # 自分の役が全体の上位何番目か
    my_rank = sorted_scores.index(my_best) + 1
    percentile = 1 - (my_rank - 1) / len(sorted_scores)
    return percentile


"""
riverのinput例
{
  "your_id": 0,
  "phase": "turn",
  "your_cards": ["A♥", "K♠"],
  "community": ["Q♥", "J♦", "10♣", "9♠", "6♦"],
  "your_chips": 950,
  "your_bet_this_round": 0,
  "your_total_bet_this_hand": 50,
  "pot": 200,
  "to_call": 0,
  "dealer_button": 3,
  "current_turn": 0,
  "players": [
    {"id": 1, "chips": 950, "bet": 0, "status": "active"},
    {"id": 2, "chips": 950, "bet": 0, "status": "active"},
    {"id": 3, "chips": 950, "bet": 0, "status": "active"}
  ],
  "actions": ["check", "bet (min 20)", "all-in (950)"],
  "history": [
    "Flop: Player 3 bet 20, all players called",
    "Turn dealt: 9♠"
  ]
}
"""
