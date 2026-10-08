import os
import tempfile

import streamlit as st

from config import CONF_THRESHOLD, IOU_TRACK_THRESHOLD, MIN_HITS_TO_SHOW
from detection import load_model, process_video
from ui import (
    CSS,
    clean_html,
    confidence_card,
    details_card,
    empty_confidence_card,
    empty_details_card,
    empty_summary_card,
    esc,
    summary_card,
    timeline_card,
)
from utils import create_summary_csv


st.set_page_config(
    page_title="Vehicle Detection & Analysis System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CSS, unsafe_allow_html=True)

for key, default in {
    "summary": None,
    "video_bytes": None,
    "csv_bytes": None,
    "snapshots": None,
    "detection_df": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default



st.markdown(
    '<div class="hero-wrap"><div class="hero-left"><div class="hero-icon">🚨</div><div><div class="hero-title">Vehicle Detection & Analysis System</div></div></div><div class="top-pills"><div class="top-pill active">▶ Video Analysis</div><div class="top-pill">Project Info</div><div class="top-pill">Model Details</div></div></div>',
    unsafe_allow_html=True
)


left, center, right = st.columns([0.95, 2.45, 1.25], gap="large")

with left:
    st.markdown('<div class="section-title"><span class="title-icon">☁️</span> Upload Video</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload video",
        type=["mp4"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
        st.markdown(
            f'<div class="file-meta"><b>{esc(uploaded_file.name)}</b><br><span class="small-muted">{size_mb:.1f} MB · MP4 video</span></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="file-meta"><b>No video selected</b><br><span class="small-muted">Choose an MP4 file to start.</span></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="title-icon">⚙️</span> Analysis Controls</div>', unsafe_allow_html=True)

    conf_threshold = st.slider(
        "Detection confidence",
        min_value=0.30,
        max_value=0.90,
        value=CONF_THRESHOLD,
        step=0.05,
        help="Minimum confidence required for a YOLO detection."
    )

    min_hits_to_show = st.slider(
        "Detection stability",
        min_value=1,
        max_value=8,
        value=MIN_HITS_TO_SHOW,
        step=1,
        help="Number of confirmations required before the object is shown and counted."
    )

    min_object_size_pct = st.slider(
        "Minimum object size",
        min_value=0.5,
        max_value=5.0,
        value=1.5,
        step=0.5,
        format="%.1f%%",
        help="Filters out very small detections."
    )

    tracking_iou = st.slider(
        "Tracking sensitivity (IoU)",
        min_value=0.05,
        max_value=0.40,
        value=IOU_TRACK_THRESHOLD,
        step=0.05,
        help="Minimum overlap required to treat detections as the same tracked vehicle."
    )

    analyze = st.button("▶ Run analysis", use_container_width=True)

with center:
    status = '<span class="badge green">● Analysis complete</span>' if st.session_state.summary is not None else '<span class="badge">Ready</span>'
    st.markdown(
        f"""
        <div class="video-head">
          <div class="section-title" style="margin:0">▣ Video Preview with Detections</div>
          <div class="badges">{status}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    video_area = st.empty()
    progress_text_area = st.empty()
    progress_bar_area = st.empty()

    if st.session_state.video_bytes is not None:
        video_area.video(st.session_state.video_bytes)
    else:
        video_area.markdown(
            """
            <div class="placeholder">
              <div>
                <div style="font-size:31px;margin-bottom:8px">🎬</div>
                Upload a video and run the analysis.<br>
                Processed detections will appear here.
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.summary is not None:
        st.markdown(
            timeline_card(st.session_state.summary),
            unsafe_allow_html=True
        )

        if st.session_state.snapshots:
            available = [
                st.session_state.snapshots.get("first"),
                st.session_state.snapshots.get("best"),
                st.session_state.snapshots.get("last"),
            ]

            if any(item is not None for item in available):
                st.markdown(
                    '<div class="snapshot-head"><span class="snapshot-icon">▣</span>'
                    '<div><b>Detection Snapshots</b>'
                    '<span>Real frames captured during analysis</span></div></div>',
                    unsafe_allow_html=True
                )

                snap_cols = st.columns(3, gap="medium")
                snap_defs = [
                    ("FIRST DETECTION", st.session_state.snapshots.get("first")),
                    ("BEST DETECTION", st.session_state.snapshots.get("best")),
                    ("LAST DETECTION", st.session_state.snapshots.get("last")),
                ]

                for col, (label, snap) in zip(snap_cols, snap_defs):
                    with col:
                        if snap is not None:
                            st.markdown(
                                f'<div class="snapshot-label">{label}'
                                f'<span>{snap["time"]} · {snap["confidence"]:.2f}</span></div>',
                                unsafe_allow_html=True
                            )
                            st.image(snap["bytes"], use_container_width=True)

with right:
    summary_slot = st.empty()
    confidence_slot = st.empty()
    details_slot = st.empty()

    if st.session_state.summary is not None:
        summary_slot.markdown(clean_html(summary_card(st.session_state.summary)), unsafe_allow_html=True)
        confidence_slot.markdown(clean_html(confidence_card(st.session_state.summary, st.session_state.detection_df)), unsafe_allow_html=True)
        details_slot.markdown(details_card(st.session_state.summary), unsafe_allow_html=True)
    else:
        summary_slot.markdown(clean_html(empty_summary_card()), unsafe_allow_html=True)
        confidence_slot.markdown(clean_html(empty_confidence_card()), unsafe_allow_html=True)
        details_slot.markdown(empty_details_card(), unsafe_allow_html=True)

    if st.session_state.summary is not None:
        d1, d2 = st.columns(2, gap="small")

        with d1:
            st.download_button(
                "📄  Export CSV",
                data=st.session_state.csv_bytes,
                file_name="detection_report.csv",
                mime="text/csv",
                use_container_width=True
            )

        with d2:
            st.download_button(
                "🎞️  Export Video",
                data=st.session_state.video_bytes,
                file_name="video_with_detections.mp4",
                mime="video/mp4",
                use_container_width=True
            )


if analyze:
    if uploaded_file is None:
        st.warning("Choose an MP4 file first.")
    else:
        model = load_model()

        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_input.write(uploaded_file.read())
        temp_input.close()

        output_path = os.path.join(tempfile.gettempdir(), "video_with_detections.mp4")

        progress_text_area.info("Analyzing video…")
        progress = progress_bar_area.progress(0)

        try:
            summary, df, snapshots = process_video(
                temp_input.name,
                output_path,
                model,
                progress,
                conf_threshold,
                min_hits_to_show,
                min_object_size_pct / 100.0,
                tracking_iou
            )

            with open(output_path, "rb") as f:
                video_bytes = f.read()

            csv_bytes = create_summary_csv(summary)

            st.session_state.summary = summary
            st.session_state.video_bytes = video_bytes
            st.session_state.csv_bytes = csv_bytes
            st.session_state.detection_df = df
            st.session_state.snapshots = snapshots

            progress_text_area.empty()
            progress_bar_area.empty()
            st.rerun()

        except Exception as e:
            progress_text_area.empty()
            progress_bar_area.empty()
            st.error(f"Analysis error: {e}")

