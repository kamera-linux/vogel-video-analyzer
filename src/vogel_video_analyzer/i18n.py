"""
Internationalization (i18n) module for vogel-video-analyzer
Provides translations for command-line output
"""

import os
import locale


# Available translations
TRANSLATIONS = {
    'en': {
        # Loading and initialization
        'loading_model': 'Loading YOLO model:',
        'model_not_found': "Model '{model_name}' not found locally, will be auto-downloaded...",
        
        # Video analysis
        'analyzing': 'Analyzing:',
        'video_not_found': 'Video not found: {path}',
        'cannot_open_video': 'Cannot open video: {path}',
        'annotation_complete': '✅ Annotated video created successfully',
        'annotation_skip_multiple': 'Skipping annotation for additional video',
        'annotation_multiple_custom_path': '⚠️  Cannot use custom output path with multiple videos',
        'annotation_using_auto_path': 'Using automatic path generation instead',
        'annotation_creating': 'Creating annotated video:',
        'annotation_flag_directory': '🏴 Flag directory:',
        'annotation_output': '📁 Output:',
        'annotation_video_info': '{width}x{height}, {fps} FPS (output: {output_fps} FPS), {frames} frames',
        'annotation_processing': 'Processing every {n} frame(s)...',
        'annotation_frames_processed': '   Frames processed: {processed}/{total}',
        'annotation_birds_detected': '   Total birds detected: {count}',
        'annotation_merging_audio': '   🎵 Merging audio from original video...',
        'annotation_audio_merged': '   ✅ Audio successfully merged',
        'annotation_audio_failed': '⚠️  Failed to merge audio (video without audio)',
        'video_info': 'Video info:',
        'frames': 'frames',
        'analyzing_every_nth': 'Analyzing every {n}. frame...',
        'analysis_complete': 'Analysis complete!',
        'analysis_interrupted': 'Analysis interrupted',
        
        # Summary video creation (v0.3.1+)
        'summary_analyzing': '🔍 Analyzing video for bird activity:',
        'summary_segments_found': '📊 Bird activity segments identified',
        'summary_creating': '🎬 Creating summary video:',
        'summary_complete': '✅ Summary video created successfully',
        'summary_multiple_custom_path': '⚠️  Cannot use custom output path with multiple videos',
        'summary_using_auto_path': 'Using automatic path generation instead',
        'summary_skip_multiple': 'Skipping summary for additional video',
        
        # Report
        'report_title': 'Video Analysis Report',
        'report_file': 'File:',
        'report_total_frames': 'Total Frames:',
        'report_analyzed': 'analyzed:',
        'report_duration': 'Duration:',
        'report_seconds': 'seconds',
        'report_bird_frames': 'Bird Frames:',
        'report_bird_segments': 'Bird Segments:',
        'report_detected_segments': 'Detected Segments:',
        'report_segment': 'Segment',
        'report_bird_frames_short': 'bird frames',
        'report_status': 'Status:',
        'status_significant': 'Significant bird activity detected',
        'status_limited': 'Limited bird activity detected',
        'status_none': 'No bird content detected',
        
        # Summary
        'summary_title': 'SUMMARY ({count} Videos)',
        'summary_total_duration': 'Total Duration:',
        'summary_total_frames': 'Total Frames Analyzed:',
        'summary_bird_frames': 'Total Frames with Birds:',
        'summary_avg_bird': 'Average Bird Content:',
        'summary_overview': 'Video Overview:',
        'summary_directory': 'Directory',
        'summary_bird': 'Bird',
        'summary_bird_pct': 'Bird%',
        'summary_frames': 'Frames',
        'summary_duration': 'Duration',
        
        # Deletion
        'delete_files_title': 'DELETING VIDEO FILES WITH 0% BIRD CONTENT ({count} files)',
        'delete_folders_title': 'DELETING FOLDERS WITH 0% BIRD CONTENT ({count} videos)',
        'deleting': 'Deleting:',
        'deleting_folder': 'Deleting folder:',
        'delete_success': 'Successfully deleted',
        'delete_error': 'Error deleting:',
        'deleted_files': 'Deleted files:',
        'deleted_folders': 'Deleted folders:',
        'remaining_videos': 'Remaining videos:',
        'no_empty_files': 'No video files with 0% bird content found',
        'no_empty_folders': 'No folders with 0% bird content found',
        'delete_deprecated': 'WARNING: --delete is deprecated. Use --delete-file or --delete-folder instead.',
        'delete_deprecated_hint': 'Defaulting to --delete-folder behavior for backward compatibility.',
        
        # Logging
        'log_file': 'Log file:',
        'log_permission_denied': 'WARNING: No write permissions for /var/log/vogel-kamera-linux/',
        'log_permission_hint': 'Run with sudo or change permissions:',
        
        # Errors
        'error': 'Error',
        'error_analyzing': 'Error analyzing',
        'report_saved': 'Report saved:',
        
        # Species identification
        'species_dependencies_missing': 'Species identification requires additional dependencies.',
        'identifying_species': 'Identifying bird species...',
        'species_title': 'Detected Species:',
        'species_count': '{count} species detected',
        'species_detections': '{detections} detections',
        'species_avg_confidence': 'avg confidence',
        'species_no_detections': 'No species identified',
        'loading_species_model': 'Loading bird species classification model:',
        'model_download_info': 'First run will download ~100-300MB, then cached locally',
        'model_loaded_success': 'Model loaded successfully',
        'model_load_error': 'Error loading model:',
        'fallback_basic_detection': 'Falling back to basic bird detection only',
        
        # HTML Reports (v0.5.0+)
        'html_generating': 'Generating HTML report...',
        'html_success': 'HTML report saved:',
        'html_error': 'Error generating HTML report:',
        'html_single_only': 'HTML reports currently support single videos only.',
        'html_processing_first': 'Processing first video:',
        'html_title': 'Bird Video Analysis',
        'html_video': 'Video:',
        'html_created': 'Created:',
        'html_detections': 'Detections',
        'html_unique_species': 'Unique Species',
        'html_avg_confidence': 'Avg Confidence',
        'html_frames_with_birds': 'Frames with Birds',
        'html_activity_timeline': 'Activity Timeline',
        'html_species_distribution': 'Species Distribution',
        'html_best_shots': 'Best Shots',
        'html_images': 'images',
        'html_no_thumbnails': 'No thumbnails available (species identification required)',
        'html_footer': 'Generated with vogel-video-analyzer',
    },
    'de': {
        # Loading and initialization
        'loading_model': 'Lade YOLO-Modell:',
        'model_not_found': "Modell '{model_name}' lokal nicht gefunden, wird automatisch heruntergeladen...",
        
        # Video analysis
        'analyzing': 'Analysiere:',
        'video_not_found': 'Video nicht gefunden: {path}',
        'cannot_open_video': 'Kann Video nicht öffnen: {path}',
        'annotation_complete': '✅ Annotiertes Video erfolgreich erstellt',
        'annotation_skip_multiple': 'Überspringe Annotation für zusätzliches Video',
        'annotation_multiple_custom_path': '⚠️  Kann keinen benutzerdefinierten Ausgabepfad mit mehreren Videos verwenden',
        'annotation_using_auto_path': 'Verwende stattdessen automatische Pfadgenerierung',
        'annotation_creating': 'Erstelle annotiertes Video:',
        'annotation_flag_directory': '🏴 Flaggen-Verzeichnis:',
        'annotation_output': '📁 Ausgabe:',
        'annotation_video_info': '{width}x{height}, {fps} FPS (Ausgabe: {output_fps} FPS), {frames} Frames',
        'annotation_processing': 'Verarbeite jeden {n}. Frame...',
        'annotation_frames_processed': '   Verarbeitete Frames: {processed}/{total}',
        'annotation_birds_detected': '   Erkannte Vögel gesamt: {count}',
        'annotation_merging_audio': '   🎵 Füge Audio vom Original-Video hinzu...',
        'annotation_audio_merged': '   ✅ Audio erfolgreich hinzugefügt',
        'annotation_audio_failed': '⚠️  Audio-Zusammenführung fehlgeschlagen (Video ohne Audio)',
        'video_info': 'Video-Info:',
        'frames': 'Frames',
        'analyzing_every_nth': 'Analysiere jeden {n}. Frame...',
        'analysis_complete': 'Analyse abgeschlossen!',
        'analysis_interrupted': 'Analyse unterbrochen',
        
        # Summary video creation (v0.3.1+)
        'summary_analyzing': '🔍 Analysiere Video für Vogelaktivität:',
        'summary_segments_found': '📊 Vogelaktivitäts-Segmente identifiziert',
        'summary_creating': '🎬 Erstelle Zusammenfassungs-Video:',
        'summary_complete': '✅ Zusammenfassungs-Video erfolgreich erstellt',
        'summary_multiple_custom_path': '⚠️  Kann keinen benutzerdefinierten Ausgabepfad mit mehreren Videos verwenden',
        'summary_using_auto_path': 'Verwende stattdessen automatische Pfadgenerierung',
        'summary_skip_multiple': 'Überspringe Zusammenfassung für zusätzliches Video',
        
        # Report
        'report_title': 'Videoanalyse-Bericht',
        'report_file': 'Datei:',
        'report_total_frames': 'Gesamt-Frames:',
        'report_analyzed': 'analysiert:',
        'report_duration': 'Dauer:',
        'report_seconds': 'Sekunden',
        'report_bird_frames': 'Vogel-Frames:',
        'report_bird_segments': 'Vogel-Segmente:',
        'report_detected_segments': 'Erkannte Segmente:',
        'report_segment': 'Segment',
        'report_bird_frames_short': 'Vogel-Frames',
        'report_status': 'Status:',
        'status_significant': 'Signifikante Vogelaktivität erkannt',
        'status_limited': 'Eingeschränkte Vogelaktivität erkannt',
        'status_none': 'Kein Vogelinhalt erkannt',
        
        # Summary
        'summary_title': 'ZUSAMMENFASSUNG ({count} Videos)',
        'summary_total_duration': 'Gesamtdauer:',
        'summary_total_frames': 'Gesamt analysierte Frames:',
        'summary_bird_frames': 'Gesamt Frames mit Vögeln:',
        'summary_avg_bird': 'Durchschnittlicher Vogelinhalt:',
        'summary_overview': 'Videoübersicht:',
        'summary_directory': 'Verzeichnis',
        'summary_bird': 'Vogel',
        'summary_bird_pct': 'Vogel%',
        'summary_frames': 'Frames',
        'summary_duration': 'Dauer',
        
        # Deletion
        'delete_files_title': 'LÖSCHE VIDEODATEIEN MIT 0% VOGELINHALT ({count} Dateien)',
        'delete_folders_title': 'LÖSCHE ORDNER MIT 0% VOGELINHALT ({count} Videos)',
        'deleting': 'Lösche:',
        'deleting_folder': 'Lösche Ordner:',
        'delete_success': 'Erfolgreich gelöscht',
        'delete_error': 'Fehler beim Löschen:',
        'deleted_files': 'Gelöschte Dateien:',
        'deleted_folders': 'Gelöschte Ordner:',
        'remaining_videos': 'Verbleibende Videos:',
        'no_empty_files': 'Keine Videodateien mit 0% Vogelinhalt gefunden',
        'no_empty_folders': 'Keine Ordner mit 0% Vogelinhalt gefunden',
        'delete_deprecated': 'WARNUNG: --delete ist veraltet. Verwenden Sie --delete-file oder --delete-folder.',
        'delete_deprecated_hint': 'Verwende --delete-folder-Verhalten für Rückwärtskompatibilität.',
        
        # Logging
        'log_file': 'Log-Datei:',
        'log_permission_denied': 'WARNUNG: Keine Schreibrechte für /var/log/vogel-kamera-linux/',
        'log_permission_hint': 'Mit sudo ausführen oder Berechtigungen ändern:',
        
        # Errors
        'error': 'Fehler',
        'error_analyzing': 'Fehler beim Analysieren',
        'report_saved': 'Bericht gespeichert:',
        
        # Species identification
        'species_dependencies_missing': 'Artenerkennung erfordert zusätzliche Abhängigkeiten.',
        'identifying_species': 'Identifiziere Vogelarten...',
        'species_title': 'Erkannte Arten:',
        'species_count': '{count} Arten erkannt',
        'species_detections': '{detections} Erkennungen',
        'species_avg_confidence': 'Ø Konfidenz',
        'species_no_detections': 'Keine Arten identifiziert',
        'loading_species_model': 'Lade Vogel-Artenerkennung Modell:',
        'model_download_info': 'Beim ersten Mal werden ~100-300MB heruntergeladen, dann lokal gecacht',
        'model_loaded_success': 'Modell erfolgreich geladen',
        'model_load_error': 'Fehler beim Laden des Modells:',
        'fallback_basic_detection': 'Verwende nur grundlegende Vogelerkennung',
        
        # HTML Reports (v0.5.0+)
        'html_generating': 'Erstelle HTML-Bericht...',
        'html_success': 'HTML-Bericht gespeichert:',
        'html_error': 'Fehler beim Erstellen des HTML-Berichts:',
        'html_single_only': 'HTML-Berichte unterstützen derzeit nur einzelne Videos.',
        'html_processing_first': 'Verarbeite erstes Video:',
        'html_title': 'Vogel-Video-Analyse',
        'html_video': 'Video:',
        'html_created': 'Erstellt:',
        'html_detections': 'Erkennungen',
        'html_unique_species': 'Verschiedene Arten',
        'html_avg_confidence': 'Ø Konfidenz',
        'html_frames_with_birds': 'Frames mit Vögeln',
        'html_activity_timeline': 'Aktivitäts-Timeline',
        'html_species_distribution': 'Arten-Verteilung',
        'html_best_shots': 'Beste Aufnahmen',
        'html_images': 'Bilder',
        'html_no_thumbnails': 'Keine Thumbnails verfügbar (Artenerkennung erforderlich)',
        'html_footer': 'Generiert mit vogel-video-analyzer',
    },
    'ja': {
        # Loading and initialization
        'loading_model': 'YOLOモデルを読み込んでいます：',
        'model_not_found': "モデル '{model_name}' がローカルで見つかりません。自動的にダウンロードします...",
        
        # Video analysis
        'analyzing': '分析中：',
        'video_not_found': 'ビデオが見つかりません：{path}',
        'cannot_open_video': 'ビデオを開けません：{path}',
        'annotation_complete': '✅ 注釈付きビデオが正常に作成されました',
        'annotation_skip_multiple': '追加のビデオの注釈をスキップします',
        'annotation_multiple_custom_path': '⚠️  複数のビデオではカスタム出力パスを使用できません',
        'annotation_using_auto_path': '代わりに自動パス生成を使用します',
        'annotation_creating': '注釈付きビデオを作成中：',
        'annotation_flag_directory': '🏴 フラグディレクトリ：',
        'annotation_output': '📁 出力：',
        'annotation_video_info': '{width}x{height}、{fps} FPS（出力：{output_fps} FPS）、{frames}フレーム',
        'annotation_processing': '{n}フレームごとに処理しています...',
        'annotation_frames_processed': '   処理されたフレーム：{processed}/{total}',
        'annotation_birds_detected': '   検出された鳥の合計：{count}',
        'annotation_merging_audio': '   🎵 元のビデオから音声を追加しています...',
        'annotation_audio_merged': '   ✅ 音声が正常に追加されました',
        'annotation_audio_failed': '⚠️  オーディオのマージに失敗しました（オーディオなしのビデオ）',
        'video_info': 'ビデオ情報：',
        'frames': 'フレーム',
        'analyzing_every_nth': '{n}フレームごとに分析しています...',
        'analysis_complete': '分析完了！',
        'analysis_interrupted': '分析が中断されました',
        
        # Summary video creation (v0.3.1+)
        'summary_analyzing': '🔍 鳥の活動についてビデオを分析しています：',
        'summary_segments_found': '📊 鳥の活動セグメントが識別されました',
        'summary_creating': '🎬 要約ビデオを作成中：',
        'summary_complete': '✅ 要約ビデオが正常に作成されました',
        'summary_multiple_custom_path': '⚠️  複数のビデオではカスタム出力パスを使用できません',
        'summary_using_auto_path': '代わりに自動パス生成を使用します',
        'summary_skip_multiple': '追加のビデオの要約をスキップします',
        
        # Report
        'report_title': 'ビデオ分析レポート',
        'report_file': 'ファイル：',
        'report_total_frames': '総フレーム数：',
        'report_analyzed': '分析済み：',
        'report_duration': '再生時間：',
        'report_seconds': '秒',
        'report_bird_frames': '鳥検出フレーム：',
        'report_bird_segments': '鳥検出セグメント：',
        'report_detected_segments': '検出されたセグメント：',
        'report_segment': 'セグメント',
        'report_bird_frames_short': '鳥フレーム',
        'report_status': 'ステータス：',
        'status_significant': '顕著な鳥の活動を検出',
        'status_limited': '限定的な鳥の活動を検出',
        'status_none': '鳥のコンテンツが検出されませんでした',
        
        # Summary
        'summary_title': 'サマリー（{count}本の動画）',
        'summary_total_duration': '総再生時間：',
        'summary_total_frames': '総分析フレーム数：',
        'summary_bird_frames': '鳥検出フレーム総数：',
        'summary_avg_bird': '平均鳥コンテンツ：',
        'summary_overview': 'ビデオ概要：',
        'summary_directory': 'ディレクトリ',
        'summary_bird': '鳥',
        'summary_bird_pct': '鳥%',
        'summary_frames': 'フレーム',
        'summary_duration': '再生時間',
        
        # Deletion
        'delete_files_title': '鳥コンテンツ0%のビデオファイルを削除（{count}ファイル）',
        'delete_folders_title': '鳥コンテンツ0%のフォルダを削除（{count}本の動画）',
        'deleting': '削除中：',
        'deleting_folder': 'フォルダを削除中：',
        'delete_success': '正常に削除されました',
        'delete_error': '削除エラー：',
        'deleted_files': '削除されたファイル：',
        'deleted_folders': '削除されたフォルダ：',
        'remaining_videos': '残りの動画：',
        'no_empty_files': '鳥コンテンツ0%のビデオファイルが見つかりません',
        'no_empty_folders': '鳥コンテンツ0%のフォルダが見つかりません',
        'delete_deprecated': '警告：--deleteは非推奨です。--delete-fileまたは--delete-folderを使用してください。',
        'delete_deprecated_hint': '後方互換性のため、--delete-folderの動作をデフォルトとします。',
        
        # Logging
        'log_file': 'ログファイル：',
        'log_permission_denied': '警告：/var/log/vogel-kamera-linux/ への書き込み権限がありません',
        'log_permission_hint': 'sudoで実行するか、権限を変更してください：',
        
        # Errors
        'error': 'エラー',
        'error_analyzing': '分析中にエラー',
        'report_saved': 'レポートが保存されました：',
        
        # Species identification
        'species_dependencies_missing': '種の識別には追加の依存関係が必要です。',
        'identifying_species': '鳥の種を識別中...',
        'species_title': '検出された種：',
        'species_count': '{count}種を検出',
        'species_detections': '{detections}件の検出',
        'species_avg_confidence': '平均信頼度',
        'species_no_detections': '種が識別されませんでした',
        'loading_species_model': '鳥種分類モデルを読み込んでいます：',
        'model_download_info': '初回実行時は約100-300MBダウンロード、その後ローカルにキャッシュされます',
        'model_loaded_success': 'モデルが正常に読み込まれました',
        'model_load_error': 'モデルの読み込みエラー：',
        'fallback_basic_detection': '基本的な鳥検出のみにフォールバックします',
        
        # HTML Reports (v0.5.0+)
        'html_generating': 'HTMLレポートを生成中...',
        'html_success': 'HTMLレポートが保存されました：',
        'html_error': 'HTMLレポートの生成エラー：',
        'html_single_only': 'HTMLレポートは現在、単一の動画のみをサポートしています。',
        'html_processing_first': '最初の動画を処理中：',
        'html_title': '鳥動画分析',
        'html_video': '動画：',
        'html_created': '作成日時：',
        'html_detections': '検出数',
        'html_unique_species': '固有種数',
        'html_avg_confidence': '平均信頼度',
        'html_frames_with_birds': '鳥検出フレーム',
        'html_activity_timeline': 'アクティビティタイムライン',
        'html_species_distribution': '種の分布',
        'html_best_shots': 'ベストショット',
        'html_images': '枚',
        'html_no_thumbnails': 'サムネイルなし（種の識別が必要）',
        'html_footer': 'vogel-video-analyzerで生成',
    }
}


class I18n:
    """Internationalization handler"""
    
    def __init__(self, language=None):
        """
        Initialize i18n with specified language or auto-detect
        
        Args:
            language: Language code ('en', 'de') or None for auto-detection
        """
        self.language = language or self._detect_language()
        
    def _detect_language(self):
        """
        Auto-detect system language
        
        Priority:
        1. VOGEL_LANG environment variable
        2. LANG environment variable
        3. locale.getdefaultlocale()
        4. Fallback to 'en'
        
        Returns:
            Language code ('en' or 'de')
        """
        # Check VOGEL_LANG first
        vogel_lang = os.environ.get('VOGEL_LANG', '').lower()
        if vogel_lang in TRANSLATIONS:
            return vogel_lang
        
        # Check LANG environment variable
        lang = os.environ.get('LANG', '').lower()
        if 'de' in lang:
            return 'de'
        elif 'en' in lang:
            return 'en'
        
        # Try locale
        try:
            default_locale = locale.getdefaultlocale()[0]
            if default_locale:
                if default_locale.lower().startswith('de'):
                    return 'de'
                elif default_locale.lower().startswith('en'):
                    return 'en'
        except:
            pass
        
        # Fallback to English
        return 'en'
    
    def translate(self, key, **kwargs):
        """
        Get translation for key
        
        Args:
            key: Translation key
            **kwargs: Format parameters for translation string
            
        Returns:
            Translated string
        """
        translation = TRANSLATIONS.get(self.language, {}).get(key, key)
        
        # Apply formatting if kwargs provided
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError:
                pass
        
        return translation


# Global instance
_i18n_instance = None


def init_i18n(language=None):
    """
    Initialize global i18n instance
    
    Args:
        language: Language code or None for auto-detection
    """
    global _i18n_instance
    _i18n_instance = I18n(language)


def get_i18n():
    """
    Get global i18n instance
    
    Returns:
        I18n instance
    """
    global _i18n_instance
    if _i18n_instance is None:
        init_i18n()
    return _i18n_instance


def t(key, **kwargs):
    """
    Convenience function for translation
    
    Args:
        key: Translation key
        **kwargs: Format arguments
        
    Returns:
        Translated string
    """
    return get_i18n().translate(key, **kwargs)


def get_language():
    """
    Get current language code
    
    Returns:
        Language code ('en' or 'de')
    """
    return get_i18n().language
