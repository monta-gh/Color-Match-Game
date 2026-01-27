"""
カラーマッチングゲーム
ランダムに生成された目標の色を、RGBスライダーを操作して再現するゲーム
"""

import streamlit as st
import random
import math


def generate_random_color():
    """ランダムなRGB色を生成"""
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def calculate_similarity(target, player):
    """
    2つのRGB色間の類似度を％で計算
    
    Args:
        target: 目標色 (r, g, b)
        player: プレイヤーの色 (r, g, b)
    
    Returns:
        類似度（0〜100%）
    """
    # ユークリッド距離を計算
    distance = math.sqrt(
        (target[0] - player[0]) ** 2 +
        (target[1] - player[1]) ** 2 +
        (target[2] - player[2]) ** 2
    )
    
    # 最大距離（白と黒の距離）
    max_distance = math.sqrt(255**2 * 3)  # ≈ 441.67
    
    # 類似度を％で計算（距離が0なら100%、最大なら0%）
    similarity = 100 - (distance / max_distance * 100)
    
    return round(similarity, 1)


def rgb_to_hex(r, g, b):
    """RGB値を16進数カラーコードに変換"""
    return f"#{r:02x}{g:02x}{b:02x}"


def init_session_state():
    """セッション状態を初期化"""
    if "target_color" not in st.session_state:
        st.session_state.target_color = generate_random_color()
    if "score_history" not in st.session_state:
        st.session_state.score_history = []
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "current_score" not in st.session_state:
        st.session_state.current_score = None


def reset_game():
    """新しいゲームを開始"""
    st.session_state.target_color = generate_random_color()
    st.session_state.submitted = False
    st.session_state.current_score = None


def submit_answer(player_color):
    """回答を送信"""
    score = calculate_similarity(st.session_state.target_color, player_color)
    st.session_state.current_score = score
    st.session_state.submitted = True
    
    # スコア履歴に追加（直近5回分のみ保持）
    st.session_state.score_history.insert(0, score)
    if len(st.session_state.score_history) > 5:
        st.session_state.score_history.pop()


def display_color_box(color, label):
    """色のボックスを表示"""
    hex_color = rgb_to_hex(*color)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <p style="font-weight: bold; font-size: 1.2em; margin-bottom: 10px;">{label}</p>
            <div style="
                width: 150px;
                height: 150px;
                background-color: {hex_color};
                border: 3px solid #444;
                border-radius: 15px;
                margin: auto;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            "></div>
            <p style="margin-top: 10px; font-family: monospace;">RGB: {color}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    # ページ設定
    st.set_page_config(
        page_title="カラーマッチングゲーム",
        page_icon="🎨",
        layout="centered"
    )

    # セッション状態を初期化
    init_session_state()

    # タイトル
    st.title("🎨 カラーマッチングゲーム")
    st.markdown("目標の色をRGBスライダーで再現しよう！")
    st.markdown("---")

    # 色の比較表示
    col1, col2 = st.columns(2)
    
    with col1:
        display_color_box(st.session_state.target_color, "🎯 目標の色")
    
    # RGBスライダー
    st.markdown("---")
    st.subheader("🎛️ 色を調整")
    
    player_r = st.slider("R（赤）", 0, 255, 128, key="slider_r")
    player_g = st.slider("G（緑）", 0, 255, 128, key="slider_g")
    player_b = st.slider("B（青）", 0, 255, 128, key="slider_b")
    
    player_color = (player_r, player_g, player_b)
    
    # プレイヤーの色を表示
    with col2:
        display_color_box(player_color, "🖌️ あなたの色")

    st.markdown("---")

    # ボタン
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("✅ 決定", use_container_width=True, type="primary"):
            submit_answer(player_color)
    
    with btn_col2:
        if st.button("🔄 新しいゲーム", use_container_width=True):
            reset_game()
            st.rerun()

    # 結果表示
    if st.session_state.submitted and st.session_state.current_score is not None:
        score = st.session_state.current_score
        
        st.markdown("---")
        
        # スコアに応じてメッセージを変更
        if score >= 95:
            st.success(f"🎉 素晴らしい！ 近似度: **{score}%**")
        elif score >= 80:
            st.info(f"👍 いい感じ！ 近似度: **{score}%**")
        elif score >= 60:
            st.warning(f"🤔 もう少し！ 近似度: **{score}%**")
        else:
            st.error(f"💪 頑張って！ 近似度: **{score}%**")

    # スコア履歴
    if st.session_state.score_history:
        st.markdown("---")
        st.subheader("📊 スコア履歴（直近5回）")
        
        history_cols = st.columns(len(st.session_state.score_history))
        for i, score in enumerate(st.session_state.score_history):
            with history_cols[i]:
                st.metric(label=f"#{i+1}", value=f"{score}%")


if __name__ == "__main__":
    main()
