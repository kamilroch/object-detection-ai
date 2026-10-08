import cv2
import pandas as pd
import streamlit as st
from ultralytics import YOLO

from config import (
    FIRE_CLASS_NAME,
    MAX_MISSED_FRAMES,
    MODEL_PATH,
    OTHER_CLASS_NAME,
    OTHER_VEHICLE_THRESHOLD,
)
from tracking import iou, smooth_box
from utils import time_format


def load_model():
    return YOLO(str(MODEL_PATH))

def draw_detection(frame, xyxy, class_name, conf, track_id):
    x1, y1, x2, y2 = map(int, xyxy)

    if class_name == FIRE_CLASS_NAME:
        color = (0, 0, 255)
    else:
        color = (255, 120, 0)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    label = f"{class_name} {conf:.2f}"

    cv2.rectangle(
        frame,
        (x1, max(y1 - 30, 0)),
        (x1 + 260, y1),
        color,
        -1
    )

    cv2.putText(
        frame,
        label,
        (x1 + 5, max(y1 - 8, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    return frame

def process_video(
    input_path,
    output_path,
    model,
    progress_bar,
    conf_threshold,
    min_hits_to_show,
    min_box_area_ratio,
    iou_track_threshold
):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise RuntimeError("Nie udało się otworzyć filmu.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not writer.isOpened():
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Lista aktualnie śledzonych obiektów
    tracks = []
    next_track_id = 1

    # Zbiory ID, żeby ten sam pojazd nie był liczony wiele razy
    counted_fire_ids = set()
    counted_other_ids = set()

    detections_log = []
    confidences = []

    first_fire_time = None
    last_fire_time = None

    snapshots = {
        "first": None,
        "best": None,
        "last": None
    }
    best_snapshot_conf = -1.0

    frame_id = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        current_time = frame_id / fps

        for track in tracks:
            track["missed"] += 1

        # YOLO analizuje aktualną klatkę filmu
        results = model(frame, conf=conf_threshold, verbose=False)

        current_detections = []

        for result in results:
            for box in result.boxes:

                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id]

                if class_name not in [FIRE_CLASS_NAME, OTHER_CLASS_NAME]:
                    continue

                xyxy = box.xyxy[0].tolist()
                xyxy = [int(v) for v in xyxy]

                x1, y1, x2, y2 = xyxy

                box_w = x2 - x1
                box_h = y2 - y1
                box_area = box_w * box_h
                frame_area = width * height

                center_y = (y1 + y2) / 2

                EDGE_MARGIN = 130

                # Filtr usuwa obiekty znajdujące się blisko krawędzi obrazu
                if x1 < EDGE_MARGIN or x2 > width - EDGE_MARGIN:
                    continue

                # Filtr usuwa bardzo małe wykrycia
                if box_area / frame_area < min_box_area_ratio:
                    continue

                # Filtr usuwa obiekty znajdujące się wysoko w kadrze
                if center_y < height * 0.28:
                    continue

                # Dla innych pojazdów wymagany jest wyższy confidence
                if class_name == OTHER_CLASS_NAME and conf < OTHER_VEHICLE_THRESHOLD:
                    continue

                current_detections.append({
                    "class_name": class_name,
                    "conf": conf,
                    "box": xyxy
                })

        used_tracks = set()

        # Przypisanie nowych detekcji do istniejących obiektów
        for det in current_detections:

            best_iou = 0
            best_track_index = None

            for idx, track in enumerate(tracks):

                if idx in used_tracks:
                    continue

                if track["class_name"] != det["class_name"]:
                    continue

                score = iou(track["box"], det["box"])

                if score > best_iou:
                    best_iou = score
                    best_track_index = idx

            if best_track_index is not None and best_iou >= iou_track_threshold:

                track = tracks[best_track_index]

                track["box"] = smooth_box(track["box"], det["box"])
                track["conf"] = det["conf"]
                track["missed"] = 0
                track["hits"] += 1

                track_id = track["id"]

                used_tracks.add(best_track_index)

            else:

                track_id = next_track_id
                next_track_id += 1

                tracks.append({
                    "id": track_id,
                    "class_name": det["class_name"],
                    "box": det["box"],
                    "conf": det["conf"],
                    "missed": 0,
                    "hits": 1
                })

            confidences.append(det["conf"])

            if det["class_name"] == FIRE_CLASS_NAME:

                if first_fire_time is None:
                    first_fire_time = current_time

                last_fire_time = current_time

            # Zapis pojedynczej detekcji do logu CSV
            detections_log.append({
                "czas": time_format(current_time),
                "id_obiektu": track_id,
                "klasa": det["class_name"],
                "confidence": round(det["conf"], 3)
            })

        confirmed_fire_confidences = []

        for track in tracks:

            if track["hits"] >= min_hits_to_show and track["missed"] == 0:

                # Liczenie unikalnych pojazdów straży
                if track["class_name"] == FIRE_CLASS_NAME:
                    counted_fire_ids.add(track["id"])
                    confirmed_fire_confidences.append(track["conf"])

                # Liczenie unikalnych innych pojazdów
                if track["class_name"] == OTHER_CLASS_NAME:
                    counted_other_ids.add(track["id"])

                frame = draw_detection(
                    frame,
                    track["box"],
                    track["class_name"],
                    track["conf"],
                    track["id"]
                )

        # Zapis rzeczywistych klatek z potwierdzoną detekcją wozu strażackiego.
        if confirmed_fire_confidences:
            frame_best_conf = max(confirmed_fire_confidences)
            ok, encoded = cv2.imencode(
                ".jpg",
                frame,
                [int(cv2.IMWRITE_JPEG_QUALITY), 88]
            )

            if ok:
                snapshot = {
                    "bytes": encoded.tobytes(),
                    "confidence": frame_best_conf,
                    "time": time_format(current_time)
                }

                if snapshots["first"] is None:
                    snapshots["first"] = snapshot

                snapshots["last"] = snapshot

                if frame_best_conf > best_snapshot_conf:
                    best_snapshot_conf = frame_best_conf
                    snapshots["best"] = snapshot

        # Usunięcie obiektów, które zniknęły z kadru na zbyt długo
        tracks = [
            track for track in tracks
            if track["missed"] <= MAX_MISSED_FRAMES
        ]

        writer.write(frame)

        frame_id += 1

        if total_frames > 0:
            progress_bar.progress(min(frame_id / total_frames, 1.0))

    cap.release()
    writer.release()

    # Podsumowanie wyników analizy filmu
    summary = {
        "fire_count": len(counted_fire_ids),
        "other_count": len(counted_other_ids),
        "total_count": len(counted_fire_ids) + len(counted_other_ids),
        "avg_conf": sum(confidences) / len(confidences) if confidences else 0,
        "max_conf": max(confidences) if confidences else 0,
        "first_fire_time": time_format(first_fire_time),
        "last_fire_time": time_format(last_fire_time)
    }

    return summary, pd.DataFrame(detections_log), snapshots
