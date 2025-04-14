from flask import Flask, request, render_template
import math

app = Flask(__name__)

def calculate_expected_matches(current_point, win_count, lose_count):
    target_point = 1450
    total_games = win_count + lose_count

    if total_games == 0:
        return None, "승리&패배 판수를 하나 이상 입력해주세요.", 0.0

    win_rate = win_count / total_games
    diff = target_point - current_point
    expected_point_per_game = 10 * win_rate - 7 * (1 - win_rate)

    if expected_point_per_game <= 0:
        return None, "마스터볼 도달이 불가능한 승률입니다.", win_rate * 100

    expected_matches = math.ceil(diff / expected_point_per_game)
    return expected_matches, None, win_rate * 100

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    rate = None
    current = win = lose = 0

    if request.method == "POST":
        try:
            current = int(request.form.get("current", 0))
            win = int(request.form.get("win", 0))
            lose = int(request.form.get("lose", 0))
            adjust = request.form.get("adjust")

            if adjust:
                if adjust == "current+1":
                    current += 1
                elif adjust == "current-1":
                    current = max(0, current - 1)
                elif adjust == "win+1":
                    win += 1
                elif adjust == "win-1":
                    win = max(0, win - 1)
                elif adjust == "lose+1":
                    lose += 1
                elif adjust == "lose-1":
                    lose = max(0, lose - 1)
                elif adjust == "win-btn":
                    win += 1
                    current += 10
                elif adjust == "lose-btn":
                    lose += 1
                    current = max(0, current - 7)

            result, error, rate = calculate_expected_matches(current, win, lose)
        except:
            error = "숫자만 입력해주세요"

    return render_template("index.html", result=result, error=error, rate=rate, current=current, win=win, lose=lose)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)