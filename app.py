from flask import Flask, request, render_template
import math

app = Flask(__name__)

def calculate_expected_matches(current_point, win_count, lose_count):
    target_point = 1450
    total_games = win_count + lose_count

    if total_games == 0:
        return "승리&패배 판수를 하나 이상 입력해주세요."
    
    win_rate = win_count / total_games
    diff = target_point - current_point
    expected_point_per_game = 10 * win_rate - 7 * (1 - win_rate)

    if expected_point_per_game <= 0:
        return "마스터볼 도달이 불가능한 승률입니다."
    
    expected_matches = diff / expected_point_per_game
    return math.ceil(expected_matches)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            current = int(request.form["current"])
            win = int(request.form["win"])
            lose = int(request.form["lose"])
            result = calculate_expected_matches(current, win, lose)
        except:
            result = "숫자만 입력해주세요"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)