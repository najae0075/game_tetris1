import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

APP_DIR = Path(__file__).resolve().parent
USER_DATA_FILE = APP_DIR / "users.json"
GAME_HTML = (APP_DIR / "game.html").read_text(encoding="utf-8")


def load_users():
    if not USER_DATA_FILE.exists():
        return []
    try:
        data = json.loads(USER_DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def save_users(users):
    USER_DATA_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")


def add_user(name):
    cleaned = (name or "").strip()
    if not cleaned:
        return False, "이름을 입력하세요."

    users = load_users()
    if any(user.get("name", "").lower() == cleaned.lower() for user in users):
        return False, "이미 존재하는 사용자입니다."

    next_id = max((int(user.get("id", 0)) for user in users), default=0) + 1
    users.append({
        "id": next_id,
        "name": cleaned,
        "score": 0,
        "best_score": 0,
        "games_played": 0,
        "history": [],
    })
    save_users(users)
    return True, "사용자가 추가되었습니다."


def update_user(user_id, new_name):
    cleaned = (new_name or "").strip()
    if not cleaned:
        return False, "변경할 이름을 입력하세요."

    users = load_users()
    for user in users:
        if int(user.get("id", 0)) == int(user_id):
            if any(
                item.get("name", "").lower() == cleaned.lower()
                and int(item.get("id", 0)) != int(user_id)
                for item in users
            ):
                return False, "이미 사용 중인 이름입니다."
            user["name"] = cleaned
            save_users(users)
            return True, "사용자 정보가 수정되었습니다."
    return False, "수정할 사용자를 찾지 못했습니다."


def delete_user(user_id):
    users = load_users()
    before = len(users)
    users = [user for user in users if int(user.get("id", 0)) != int(user_id)]
    if len(users) == before:
        return False, "삭제할 사용자를 찾지 못했습니다."
    save_users(users)
    return True, "사용자가 삭제되었습니다."


def record_score(user_name, score_value, lines=0, level=1):
    try:
        score_value = int(score_value)
        lines = int(lines)
        level = int(level)
    except (TypeError, ValueError):
        return False, "점수, 줄 수, 레벨은 숫자여야 합니다."

    users = load_users()
    for user in users:
        if user.get("name") == user_name:
            history = user.setdefault("history", [])
            history.append({
                "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": score_value,
                "lines": lines,
                "level": level,
            })
            user["score"] = score_value
            user["best_score"] = max(int(user.get("best_score", 0)), score_value)
            user["games_played"] = len(history)
            save_users(users)
            return True, "점수가 저장되었습니다."
    return False, "사용자를 찾지 못했습니다."


def ranking_rows():
    rows = []
    for user in load_users():
        rows.append({
            "name": user.get("name", "Unknown"),
            "score": int(user.get("score", 0)),
            "best_score": int(user.get("best_score", 0)),
            "games_played": int(user.get("games_played", 0)),
        })

    rows.sort(key=lambda item: (item["best_score"], item["score"], item["games_played"]), reverse=True)
    for idx, row in enumerate(rows, start=1):
        row["rank"] = idx
    return rows


def user_history(name):
    for user in load_users():
        if user.get("name") == name:
            history = user.get("history", [])
            return sorted(history, key=lambda item: item.get("recorded_at", ""), reverse=True)
    return []


st.set_page_config(page_title="Tetris Rank Manager", page_icon="🎮", layout="wide")
st.title("🎮 Tetris 사용자 관리 & 랭킹")
st.caption("사용자를 추가하고, 점수를 저장하며, 사용자별 플레이 기록과 랭킹을 관리합니다.")

page = st.sidebar.radio("메뉴", ["게임 플레이", "사용자 관리", "랭킹", "상세 기록"])

if page == "게임 플레이":
    users = load_users()
    st.subheader("게임 플레이")

    if not users:
        st.warning("먼저 사용자 관리에서 사용자를 추가해주세요.")
    else:
        selected_user = st.selectbox("현재 사용자", [user["name"] for user in users], index=0)
        st.info(f"선택된 사용자: {selected_user}")

        game_html = GAME_HTML + f"""
        <script>
          window.__selectedUser = {json.dumps(selected_user)};
        </script>
        """

        component_value = components.html(game_html, height=820, scrolling=False)

        if isinstance(component_value, dict):
            user_name = str(component_value.get("user") or selected_user)
            score_value = int(component_value.get("score", 0) or 0)
            lines_value = int(component_value.get("lines", 0) or 0)
            level_value = int(component_value.get("level", 1) or 1)
            save_key = f"{user_name}:{score_value}:{lines_value}:{level_value}"
            if score_value >= 0 and st.session_state.get("last_game_save_key") != save_key:
                st.session_state["last_game_save_key"] = save_key
                ok, msg = record_score(user_name, score_value, lines_value, level_value)
                if ok:
                    st.success(f"게임 종료 기록 저장: {msg}")
                else:
                    st.warning(msg)

        st.subheader("수동 점수 저장")
        col1, col2, col3 = st.columns(3)
        with col1:
            score_value = st.number_input("점수", min_value=0, step=1, value=0, key="manual_score")
        with col2:
            lines_value = st.number_input("지운 줄 수", min_value=0, step=1, value=0, key="manual_lines")
        with col3:
            level_value = st.number_input("레벨", min_value=1, step=1, value=1, key="manual_level")

        if st.button("점수 저장"):
            ok, msg = record_score(selected_user, score_value, lines_value, level_value)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

elif page == "사용자 관리":
    st.subheader("사용자 추가")
    with st.form("add_user_form"):
        new_name = st.text_input("새 사용자 이름")
        submitted = st.form_submit_button("추가")
        if submitted:
            ok, msg = add_user(new_name)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    users = load_users()
    if users:
        st.subheader("사용자 수정 / 삭제")
        user_map = {user["name"]: user["id"] for user in users}
        chosen_name = st.selectbox("수정 또는 삭제할 사용자", list(user_map.keys()))
        edited_name = st.text_input("변경할 이름", value=chosen_name)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("사용자 수정"):
                ok, msg = update_user(user_map[chosen_name], edited_name)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        with col2:
            if st.button("사용자 삭제"):
                ok, msg = delete_user(user_map[chosen_name])
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.dataframe(
            pd.DataFrame(users)[["id", "name", "score", "best_score", "games_played"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("아직 등록된 사용자가 없습니다.")

elif page == "랭킹":
    st.subheader("사용자별 랭킹")
    rows = ranking_rows()
    if not rows:
        st.info("기록이 아직 없습니다. 게임을 플레이하고 점수를 저장해 주세요.")
    else:
        rank_table = [{
            "순위": row["rank"],
            "사용자": row["name"],
            "현재 점수": row["score"],
            "최고 점수": row["best_score"],
            "게임 수": row["games_played"],
        } for row in rows]

        st.dataframe(rank_table, use_container_width=True, hide_index=True)
        top5 = {row["name"]: row["best_score"] for row in rows[:5]}
        st.bar_chart(top5)

else:
    users = load_users()
    if not users:
        st.info("먼저 사용자를 추가해 주세요.")
    else:
        selected_user = st.selectbox("상세 기록 보기", [user["name"] for user in users])
        history = user_history(selected_user)
        if not history:
            st.info(f"{selected_user}의 플레이 기록이 아직 없습니다.")
        else:
            st.subheader(f"{selected_user}의 최근 기록")
            hist_df = pd.DataFrame(history)
            hist_df = hist_df[["recorded_at", "score", "lines", "level"]]
            st.dataframe(hist_df, use_container_width=True, hide_index=True)
            st.line_chart(hist_df.set_index("recorded_at")["score"])
