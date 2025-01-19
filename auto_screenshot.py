# /Users/i_kawano/Documents/Auto-YT-screenshot-new/auto_screenshot.py
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import base64
from io import BytesIO


# Chromeのオプションを設定
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# --- ここがポイント ---
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-background-timer-throttle")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-renderer-backgrounding")
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
chrome_options.add_argument("--mute-audio")
# すでに入っているオプションに加えて、下記2つを追加
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-file-access-from-files")
# -----------------------


# ChromeDriverのパスを指定
# service = Service('/Users/i_kawano/Documents/Auto-YT-screenshot-new/chromedriver-mac-arm64/chromedriver')  # 確認したChromeDriverのパスに変更
service = Service('./chromedriver-mac-arm64/chromedriver')

options = Options()

# ドライバーを初期化
# driver = webdriver.Chrome(service=service, options=chrome_options)
# 重複したoptionsの定義を削除
driver = webdriver.Chrome(service=service, options=chrome_options)


# ローカルの動画ファイルのURLを指定
video_path = os.path.abspath("videos/【9分で分かる】ロジスティック回帰分析を分かりやすく解説！.mp4")  # ${num}は都度変更する
url = f"file://{video_path}"
driver.get(url)

# 動画を全画面にするために待機
time.sleep(5)

# ビデオ要素を見つけるための待機
time.sleep(5)  # ページが完全に読み込まれるまで待機

# ビデオ要素を見つける
try:
    video_element = driver.find_element(By.TAG_NAME, 'video')
except:
    print("ビデオ要素が見つかりませんでした。")
    driver.quit()
    exit()

# # 動画を再生
# driver.execute_script("arguments[0].play();", video_element)
driver.execute_script("""
    var video = arguments[0];
    video.setAttribute('crossOrigin', 'anonymous');
""", video_element)


# 動画の総再生時間（秒）を取得
video_duration = driver.execute_script("return arguments[0].duration;", video_element)

# スクリーンショットを一定時間ごとに撮る間隔を設定
interval = 2  # スクリーンショットの間隔（秒）
num_screenshots = int(video_duration // interval)  # 動画全体に対してスクリーンショットの回数を計算

# 保存先フォルダ
output_folder = "screenshots"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


get_screenshot_script = """
var video = arguments[0];
var canvas = document.createElement('canvas');
canvas.width = video.videoWidth;
canvas.height = video.videoHeight;
var ctx = canvas.getContext('2d', {willReadFrequently: true});
ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
return canvas.toDataURL('image/png').substring(22);
"""


for i in range(num_screenshots):
    # JavaScriptでスクリーンショットを取得
    screenshot_base64 = driver.execute_script(get_screenshot_script, video_element)
    
    # Base64からバイナリデータに変換して画像を保存
    screenshot_data = base64.b64decode(screenshot_base64)
    image = Image.open(BytesIO(screenshot_data))
    image.save(os.path.join(output_folder, f"screenshot_{i+1}.png"))
    
    # 次のスクリーンショットまで待機
    time.sleep(interval)

# ドライバーを終了
driver.quit()
