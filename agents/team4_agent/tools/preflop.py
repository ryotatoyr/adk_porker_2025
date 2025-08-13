"""
プレフロップでの勝率計算ツール

このモジュールは、ポーカーのプレフロップ（最初の2枚のカード）での勝率を計算します。
starting_hand_datasetからデータを読み取り、指定されたハンドとプレイヤー数に対する勝率を返します。
"""

import ast
from typing import Any, Dict, Optional, Tuple


def load_starting_hand_dataset() -> Dict[str, float]:
    """
    スターティングハンドデータセットを読み込みます。
    
    Returns:
        Dict[str, float]: ハンド情報をキーとし、勝率を値とする辞書
    """
    try:
        with open('starting_hand_dataset.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # コメントとdocstringを除去
        lines = content.split('\n')
        data_lines = []
        in_data = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('{') and '"first_val"' in line:
                in_data = True
            if in_data:
                if line.startswith('{') or line.startswith('}'):
                    data_lines.append(line)
                elif line and not line.startswith('#'):
                    data_lines.append(line)
            if line.startswith('}') and in_data:
                in_data = False
        
        # データを結合して辞書として解析
        data_str = '\n'.join(data_lines)
        # 複数の辞書を結合
        data_str = data_str.replace('}\n{', ',\n')
        data_str = '{' + data_str.strip('{}') + '}'
        
        # 辞書として解析
        dataset = ast.literal_eval(data_str)
        return dataset
        
    except Exception as e:
        print(f"データセットの読み込みエラー: {e}")
        return {}


def parse_hand_input(hand_input: str) -> Optional[Tuple[str, str, str]]:
    """
    ハンド入力を解析して、first_val, second_val, suit_typeを抽出します。
    
    Args:
        hand_input (str): ハンドの入力文字列（例: "AKs", "QJo", "TT"）
    
    Returns:
        Optional[Tuple[str, str, str]]: (first_val, second_val, suit_type)のタプル、解析できない場合はNone
    
    Examples:
        >>> parse_hand_input("AKs")
        ('A', 'K', 'suited')
        >>> parse_hand_input("QJo")
        ('Q', 'J', 'offsuit')
        >>> parse_hand_input("TT")
        ('T', 'T', 'pair')
    """
    hand_input = hand_input.upper().strip()
    
    if len(hand_input) < 2:
        return None
    
    first_val = hand_input[0]
    second_val = hand_input[1]
    
    # ペアの場合
    if first_val == second_val:
        return (first_val, second_val, 'pair')
    
    # スート指定がある場合
    if len(hand_input) > 2:
        suit_indicator = hand_input[2]
        if suit_indicator == 's':
            return (first_val, second_val, 'suited')
        elif suit_indicator == 'o':
            return (first_val, second_val, 'offsuit')
    
    # デフォルトはoffsuit
    return (first_val, second_val, 'offsuit')


def calculate_win_rate(hand_input: str, num_players: int, dataset: Dict[str, float]) -> Optional[float]:
    """
    指定されたハンドとプレイヤー数での勝率を計算します。
    
    Args:
        hand_input (str): ハンドの入力文字列（例: "AKs", "QJo", "TT"）
        num_players (int): プレイヤー数（2-9）
        dataset (Dict[str, float]): スターティングハンドデータセット
    
    Returns:
        Optional[float]: 勝率（0.0-1.0）、見つからない場合はNone
    """
    # ハンド入力を解析
    parsed = parse_hand_input(hand_input)
    if not parsed:
        return None
    
    first_val, second_val, suit_type = parsed
    
    # データセットから該当するエントリを検索
    for key, value in dataset.items():
        if (key.get('first_val') == first_val and 
            key.get('second_val') == second_val and 
            key.get('suit_type') == suit_type and 
            key.get('num_players') == num_players):
            return value
    
    # 完全一致が見つからない場合、suit_typeを"any"で検索
    if suit_type in ['suited', 'offsuit']:
        for key, value in dataset.items():
            if (key.get('first_val') == first_val and 
                key.get('second_val') == second_val and 
                key.get('suit_type') == 'any' and 
                key.get('num_players') == num_players):
                return value
    
    return None


def get_hand_recommendation(win_rate: float) -> str:
    """
    勝率に基づいてハンドの推奨アクションを返します。
    
    Args:
        win_rate (float): 勝率（0.0-1.0）
    
    Returns:
        str: 推奨アクション
    """
    if win_rate >= 0.7:
        return "強く推奨 (Raise/Reraise)"
    elif win_rate >= 0.6:
        return "推奨 (Raise/Call)"
    elif win_rate >= 0.5:
        return "状況次第 (Call/Fold)"
    elif win_rate >= 0.4:
        return "慎重に (Call/Fold)"
    else:
        return "推奨しない (Fold)"


def main():
    """
    メイン関数：ユーザー入力を受け取り、勝率を計算して表示します。
    """
    print("ポーカープレフロップ勝率計算ツール")
    print("=" * 40)
    
    # データセットを読み込み
    dataset = load_starting_hand_dataset()
    if not dataset:
        print("エラー: データセットの読み込みに失敗しました。")
        return
    
    print(f"データセット読み込み完了: {len(dataset)}件のエントリ")
    print()
    
    while True:
        try:
            # ユーザー入力を受け取り
            hand_input = input("ハンドを入力してください（例: AKs, QJo, TT）: ").strip()
            if hand_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not hand_input:
                continue
            
            num_players_input = input("プレイヤー数を入力してください（2-9）: ").strip()
            if num_players_input.lower() in ['quit', 'exit', 'q']:
                break
            
            try:
                num_players = int(num_players_input)
                if num_players < 2 or num_players > 9:
                    print("プレイヤー数は2-9の範囲で入力してください。")
                    continue
            except ValueError:
                print("プレイヤー数は数値で入力してください。")
                continue
            
            # 勝率を計算
            win_rate = calculate_win_rate(hand_input, num_players, dataset)
            
            if win_rate is not None:
                print(f"\n結果:")
                print(f"ハンド: {hand_input}")
                print(f"プレイヤー数: {num_players}")
                print(f"勝率: {win_rate:.3f} ({win_rate*100:.1f}%)")
                print(f"推奨: {get_hand_recommendation(win_rate)}")
            else:
                print(f"\nエラー: ハンド '{hand_input}' とプレイヤー数 {num_players} の組み合わせが見つかりません。")
                print("有効なハンド例: AKs, QJo, TT, 72o")
            
            print("\n" + "-" * 40)
            
        except KeyboardInterrupt:
            print("\n\nプログラムを終了します。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
