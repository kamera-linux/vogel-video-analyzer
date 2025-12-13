"""
HTML report generation for bird video analysis results.

This module creates interactive HTML reports with:
- Activity timeline charts
- Species distribution visualization
- Thumbnail gallery of detected birds
- Detection statistics and metadata
"""

import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
import urllib.request

from .i18n import t, get_language
from .species_classifier import BirdSpeciesClassifier

# Chart.js library will be embedded inline for HTMLPreview compatibility
CHARTJS_CDN_URL = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"
_CHARTJS_CACHE = None


class HTMLReporter:
    """Generate interactive HTML reports from video analysis results."""
    
    def __init__(self, analysis_data: Dict, video_path: str):
        """
        Initialize the HTML reporter.
        
        Args:
            analysis_data: Analysis results from analyzer.py
            video_path: Path to the analyzed video file
        """
        self.data = analysis_data
        self.video_path = Path(video_path)
        self.video_name = self.video_path.name        
    @staticmethod
    def _get_chartjs() -> str:
        """Get Chart.js library code (download once and cache)."""
        global _CHARTJS_CACHE
        
        if _CHARTJS_CACHE is None:
            try:
                with urllib.request.urlopen(CHARTJS_CDN_URL, timeout=10) as response:
                    _CHARTJS_CACHE = response.read().decode('utf-8')
            except Exception as e:
                print(f"⚠️  Warning: Could not download Chart.js: {e}")
                print(f"   Charts will not be displayed in the HTML report.")
                _CHARTJS_CACHE = "// Chart.js not available"
        
        return _CHARTJS_CACHE        
    def generate_report(self, output_path: str, max_thumbnails: int = 50) -> None:
        """
        Generate and save an HTML report.
        
        Args:
            output_path: Path where the HTML file will be saved
            max_thumbnails: Maximum number of thumbnails to include
        """
        html_content = self._build_html(max_thumbnails)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding='utf-8')
        
    def _build_html(self, max_thumbnails: int) -> str:
        """Build the complete HTML document."""
        stats = self._calculate_statistics()
        timeline_data = self._prepare_timeline_data()
        species_data = self._prepare_species_data()
        thumbnails = self._generate_thumbnails(max_thumbnails)
        chartjs_code = self._get_chartjs()
        
        html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t('html_title')}: {self.video_name}</title>
    <script>
    {chartjs_code}
    </script>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🦅 {t('html_title')}</h1>
            <div class="video-info">
                <p><strong>{t('html_video')}</strong> {self.video_name}</p>
                <p><strong>{t('html_created')}</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
            </div>
        </header>
        
        <section class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_detections']}</div>
                <div class="stat-label">{t('html_detections')}</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['unique_species']}</div>
                <div class="stat-label">{t('html_unique_species')}</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['avg_confidence']:.1f}%</div>
                <div class="stat-label">{t('html_avg_confidence')}</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['frames_with_birds']}</div>
                <div class="stat-label">{t('html_frames_with_birds')}</div>
            </div>
        </section>
        
        <section class="chart-section">
            <h2>📊 {t('html_activity_timeline')}</h2>
            <div class="chart-container">
                <canvas id="timelineChart"></canvas>
            </div>
        </section>
        
        <section class="chart-section">
            <h2>🐦 {t('html_species_distribution')}</h2>
            <div class="chart-container">
                <canvas id="speciesChart"></canvas>
            </div>
        </section>
        
        <section class="gallery-section">
            <h2>📸 {t('html_best_shots')} ({len(thumbnails)} {t('html_images')})</h2>
            <div class="thumbnail-grid">
                {self._render_thumbnails(thumbnails) if thumbnails else '<p style="text-align:center;color:#666;">' + t('html_no_thumbnails') + '</p>'}
            </div>
        </section>
        
        <footer>
            <p>{t('html_footer')} v0.5.0</p>
        </footer>
    </div>
    
    <script>
        {self._get_chart_js(timeline_data, species_data)}
    </script>
</body>
</html>"""
        return html
    
    def _calculate_statistics(self) -> Dict:
        """Calculate summary statistics from analysis data."""
        bird_detections = self.data.get('bird_detections', 0)
        frames_with_birds = self.data.get('frames_with_birds', 0)
        
        # Extract species from species_stats
        species_stats = self.data.get('species_stats', {})
        species_set = set(species_stats.keys()) if species_stats else set()
        
        # Calculate average confidence from species_stats
        confidences = []
        if species_stats:
            for species_data in species_stats.values():
                if 'avg_confidence' in species_data:
                    confidences.append(species_data['avg_confidence'])
        
        return {
            'total_detections': bird_detections,
            'unique_species': len(species_set),
            'avg_confidence': (sum(confidences) / len(confidences) * 100) if confidences else 0,
            'frames_with_birds': frames_with_birds
        }
    
    def _prepare_timeline_data(self) -> Dict:
        """Prepare data for the activity timeline chart."""
        # Use bird_segments data from analyzer
        segments = self.data.get('bird_segments', [])
        
        if not segments:
            return {'labels': ['0s'], 'values': [0]}
        
        # Group detections by time intervals (every 10 seconds)
        fps = self.data.get('fps', 30)
        duration = self.data.get('duration_seconds', 0)
        interval_seconds = 10
        num_intervals = int(duration / interval_seconds) + 1
        
        timeline = [0] * num_intervals
        
        # Count detections per interval based on segments
        for segment in segments:
            start_time = segment.get('start', 0)
            end_time = segment.get('end', 0)
            detections = segment.get('detections', 1)
            
            start_interval = int(start_time / interval_seconds)
            end_interval = int(end_time / interval_seconds)
            
            # Distribute detections across intervals
            for i in range(start_interval, min(end_interval + 1, num_intervals)):
                timeline[i] += 1
        
        labels = [f"{i * interval_seconds}s" for i in range(num_intervals)]
        
        return {'labels': labels, 'values': timeline}
    
    def _prepare_species_data(self) -> Dict:
        """Prepare data for the species distribution chart."""
        species_stats = self.data.get('species_stats', {})
        
        if not species_stats:
            return {'labels': [t('species_no_detections')], 'values': [0]}
        
        # Convert species_stats to list of (name, count)
        # Translate species names to current language
        species_counts = []
        for name, data in species_stats.items():
            # Translate species name
            translated_name = BirdSpeciesClassifier.translate_species_name(name)
            species_counts.append((translated_name, data['count']))
        
        # Sort by count and take top 10
        sorted_species = sorted(species_counts, key=lambda x: x[1], reverse=True)[:10]
        
        labels = [s[0] for s in sorted_species]
        values = [s[1] for s in sorted_species]
        
        return {'labels': labels, 'values': values}
    
    def _generate_thumbnails(self, max_count: int) -> List[Dict]:
        """
        Generate thumbnail images from the video for best detections.
        
        Args:
            max_count: Maximum number of thumbnails to generate
            
        Returns:
            List of thumbnail data with base64 encoded images
        """
        # Get detections from analyzer data
        detections = self.data.get('detections', [])
        
        if not detections:
            return []
        
        thumbnails = []
        cap = cv2.VideoCapture(str(self.video_path))
        fps = self.data.get('fps', 30)
        
        try:
            # Collect all detections with species info
            all_detections = []
            for detection in detections:
                frame_num = detection.get('frame', 0)
                species_list = detection.get('species', [])
                
                # Add each species detection from this frame
                for species_info in species_list:
                    all_detections.append({
                        'frame': frame_num,
                        'species': species_info.get('species', 'Unknown'),
                        'confidence': species_info.get('confidence', 0)
                    })
            
            # Sort by confidence and limit
            all_detections.sort(key=lambda x: x['confidence'], reverse=True)
            all_detections = all_detections[:max_count]
            
            for detection in all_detections:
                frame_num = detection['frame']
                species_name = detection['species']
                confidence = detection['confidence']
                
                # Translate species name to current language
                translated_species = BirdSpeciesClassifier.translate_species_name(species_name)
                
                # Seek to frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Resize for thumbnail (max 300px width)
                h, w = frame.shape[:2]
                if w > 300:
                    scale = 300 / w
                    frame = cv2.resize(frame, (300, int(h * scale)))
                
                # Convert to JPEG and base64
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                img_base64 = base64.b64encode(buffer).decode('utf-8')
                
                thumbnails.append({
                    'image': img_base64,
                    'species': translated_species,
                    'confidence': confidence * 100,
                    'frame': frame_num,
                    'timestamp': self._frame_to_timestamp(frame_num, fps)
                })
        
        finally:
            cap.release()
        
        return thumbnails
    
    def _frame_to_timestamp(self, frame_num: int, fps: float) -> str:
        """Convert frame number to timestamp string."""
        seconds = frame_num / fps
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    
    def _render_thumbnails(self, thumbnails: List[Dict]) -> str:
        """Render HTML for thumbnail gallery."""
        html_parts = []
        
        for thumb in thumbnails:
            html_parts.append(f"""
                <div class="thumbnail-card">
                    <img src="data:image/jpeg;base64,{thumb['image']}" alt="{thumb['species']}">
                    <div class="thumbnail-info">
                        <div class="species-name">{thumb['species']}</div>
                        <div class="thumbnail-meta">
                            <span>🎯 {thumb['confidence']:.1f}%</span>
                            <span>🕐 {thumb['timestamp']}</span>
                        </div>
                    </div>
                </div>
            """)
        
        return '\n'.join(html_parts)
    
    def _get_css(self) -> str:
        """Return CSS stylesheet."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        h2 {
            color: #333;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
        }
        
        .video-info {
            opacity: 0.9;
            margin-top: 1rem;
        }
        
        .video-info p {
            margin: 0.5rem 0;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            background: #f8f9fa;
        }
        
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .chart-section {
            padding: 2rem;
            border-top: 1px solid #e0e0e0;
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            margin-top: 1rem;
        }
        
        .gallery-section {
            padding: 2rem;
            border-top: 1px solid #e0e0e0;
            background: #f8f9fa;
        }
        
        .thumbnail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }
        
        .thumbnail-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        
        .thumbnail-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }
        
        .thumbnail-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
        }
        
        .thumbnail-info {
            padding: 1rem;
        }
        
        .species-name {
            font-weight: bold;
            font-size: 1.1rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .thumbnail-meta {
            display: flex;
            justify-content: space-between;
            color: #666;
            font-size: 0.9rem;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            background: #f8f9fa;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }
        
        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr 1fr;
            }
            
            .thumbnail-grid {
                grid-template-columns: 1fr;
            }
        }
        """
    
    def _get_chart_js(self, timeline_data: Dict, species_data: Dict) -> str:
        """Return JavaScript code for Chart.js visualizations."""
        return f"""
        // Activity Timeline Chart
        const timelineCtx = document.getElementById('timelineChart').getContext('2d');
        new Chart(timelineCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(timeline_data['labels'])},
                datasets: [{{
                    label: 'Erkennungen',
                    data: {json.dumps(timeline_data['values'])},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            precision: 0
                        }}
                    }}
                }}
            }}
        }});
        
        // Species Distribution Chart
        const speciesCtx = document.getElementById('speciesChart').getContext('2d');
        new Chart(speciesCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(species_data['labels'])},
                datasets: [{{
                    label: 'Anzahl',
                    data: {json.dumps(species_data['values'])},
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#4facfe',
                        '#43e97b', '#fa709a', '#fee140', '#30cfd0',
                        '#a8edea', '#fed6e3'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            precision: 0
                        }}
                    }}
                }}
            }}
        }});
        """
