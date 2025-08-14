"""
Side pot distribution tests
"""

from poker.game import PokerGame, GamePhase
from poker.player_models import RandomPlayer, PlayerStatus
from poker.game_models import Card, Suit


def test_side_pot_distribution_basic():
    """All-in creates main and side pots; distribute correctly.

    Scenario:
    - P0 all-in 50
    - P1, P2, P3 each invest 200
    Pot layers:
      main  = 50 * 4 = 200 (eligible: P0,P1,P2,P3)
      side1 = 150 * 3 = 450 (eligible: P1,P2,P3)

    Hands:
      P0: Trips Aces (best overall)
      P1: Trips Kings (best among P1,P2,P3)
      P2: Trips Queens
      P3: Pair Nines

    Expected:
      P0 wins 200 (main pot only)
      P1 wins 450 (side pot)
      P2, P3 win 0
    """

    game = PokerGame()
    # Add 4 players
    p0 = RandomPlayer(0, "P0", 0)
    p1 = RandomPlayer(1, "P1", 0)
    p2 = RandomPlayer(2, "P2", 0)
    p3 = RandomPlayer(3, "P3", 0)
    game.add_player(p0)
    game.add_player(p1)
    game.add_player(p2)
    game.add_player(p3)

    # Assign community cards
    game.community_cards = [
        Card(14, Suit.CLUBS),  # A♣
        Card(13, Suit.DIAMONDS),  # K♦
        Card(12, Suit.HEARTS),  # Q♥
        Card(2, Suit.SPADES),  # 2♠
        Card(3, Suit.SPADES),  # 3♠
    ]

    # Hole cards
    p0.hole_cards = [Card(14, Suit.DIAMONDS), Card(14, Suit.HEARTS)]  # A♦ A♥ (Trips A)
    p1.hole_cards = [Card(13, Suit.CLUBS), Card(13, Suit.SPADES)]  # K♣ K♠ (Trips K)
    p2.hole_cards = [Card(12, Suit.CLUBS), Card(12, Suit.SPADES)]  # Q♣ Q♠ (Trips Q)
    p3.hole_cards = [Card(9, Suit.CLUBS), Card(9, Suit.DIAMONDS)]  # 9♣ 9♦ (Pair 9)

    # Set statuses at showdown
    p0.status = PlayerStatus.ALL_IN
    p1.status = PlayerStatus.ACTIVE
    p2.status = PlayerStatus.ACTIVE
    p3.status = PlayerStatus.ACTIVE

    # Contributed chips this hand
    p0.total_bet_this_hand = 50
    p1.total_bet_this_hand = 200
    p2.total_bet_this_hand = 200
    p3.total_bet_this_hand = 200
    # Ensure current_bet does not interfere
    p0.current_bet = 0
    p1.current_bet = 0
    p2.current_bet = 0
    p3.current_bet = 0

    # Total pot
    game.pot = 50 + 200 + 200 + 200

    # Move to showdown phase
    game.current_phase = GamePhase.SHOWDOWN

    results = game.conduct_showdown()

    # Map winnings
    pid_to_win = {r["player_id"]: r["winnings"] for r in results["results"]}

    assert pid_to_win.get(0, 0) == 200
    assert pid_to_win.get(1, 0) == 450
    assert pid_to_win.get(2, 0) == 0
    assert pid_to_win.get(3, 0) == 0
