
import cv2
import mediapipe as mp
import numpy as np
import socket
import json
import time

# =========================
# 設定
# =========================

CAMERA_ID = 0
UDP_IP = "127.0.0.1"
UDP_PORT = 5000

MODEL_PATH = "face_landmarker.task"

# =========================
# UDP
# =========================

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_ADDRESS = ("127.0.0.1", 5000)


def rotation_matrix_to_quaternion(R):
    trace = np.trace(R)

    if trace > 0:
        s = np.sqrt(trace + 1.0) * 2
        w = 0.25 * s
        x = (R[2, 1] - R[1, 2]) / s
        y = (R[0, 2] - R[2, 0]) / s
        z = (R[1, 0] - R[0, 1]) / s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s
    else:
        s = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s

    return [float(x), float(y), float(z), float(w)]


def send_face_data(position, rotation_matrix):
    qx, qy, qz, qw = rotation_matrix_to_quaternion(rotation_matrix)

    data = {
        "position": {
            "x": float(position[0]),
            "y": float(position[1]),
            "z": float(position[2])
        },
        "rotation": {
            "x": qx,
            "y": qy,
            "z": qz,
            "w": qw
        }
    }

    sock.sendto(
        json.dumps(data).encode("utf-8"),
        UDP_ADDRESS
    )

# =========================
# MediaPipe
# =========================

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1,
    output_facial_transformation_matrixes=True
)

# =========================
# カメラ
# =========================

cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)

if not cap.isOpened():
    raise RuntimeError("カメラを開けませんでした")

timestamp_ms = 0

# =========================
# メインループ
# =========================

try:
    with FaceLandmarker.create_from_options(options) as landmarker:

        while True:
            ret, frame = cap.read()

            if not ret:
                print("カメラ画像を取得できません")
                break

            # 鏡のように表示したい場合は有効化
            # frame = cv2.flip(frame, 1)

            height, width = frame.shape[:2]

            # BGR -> RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            timestamp_ms += 1

            result = landmarker.detect_for_video(
                mp_image,
                timestamp_ms
            )

            # =========================
            # 顔を検出した場合
            # =========================

            if (
                result.face_landmarks
                and result.facial_transformation_matrixes
            ):
                landmarks = result.face_landmarks[0]

                # -------------------------
                # 1. 顔の中心（画像上）
                # -------------------------

                center_x = sum(p.x for p in landmarks) / len(landmarks)
                center_y = sum(p.y for p in landmarks) / len(landmarks)
                center_z = sum(p.z for p in landmarks) / len(landmarks)

                # 正規化座標をピクセル座標へ
                screen_x = int(center_x * width)
                screen_y = int(center_y * height)

                # -------------------------
                # 2. 顔の変換行列
                # -------------------------

                matrix = np.asarray(
                    result.facial_transformation_matrixes[0],
                    dtype=np.float64
                )

                # 4x4行列であることを確認
                if matrix.shape != (4, 4):
                    print("想定外の行列サイズ:", matrix.shape)
                    continue

                # 平行移動成分
                # 顔の3Dモデルの座標系に基づく推定位置
                position = matrix[:3, 3]

                # 回転成分（3x3）
                rotation = matrix[:3, :3]

                # -------------------------
                # 3. UDP送信
                # -------------------------

                send_face_data(position, rotation)

                # -------------------------
                # 4. デバッグ表示
                # -------------------------

                cv2.circle(
                    frame,
                    (screen_x, screen_y),
                    5,
                    (255, 255, 255),
                    -1
                )

                # ランドマーク描画
                for point in landmarks:
                    x = int(point.x * width)
                    y = int(point.y * height)

                    if 0 <= x < width and 0 <= y < height:
                        cv2.circle(
                            frame,
                            (x, y),
                            1,
                            (0, 255, 255),
                            -1
                        )

                cv2.putText(
                    frame,
                    f"Screen: {center_x:.3f}, {center_y:.3f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Landmark Z: {center_z:.4f}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Position: {position[0]:.2f}, "
                    f"{position[1]:.2f}, {position[2]:.2f}",
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 200, 0),
                    2
                )

            cv2.imshow("Face Tracking + UDP", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

finally:
    cap.release()
    cv2.destroyAllWindows()
    sock.close()
