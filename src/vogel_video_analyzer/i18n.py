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
        'video_info': 'Video info:',
        'frames': 'frames',
        'analyzing_every_nth': 'Analyzing every {n}. frame...',
        'analysis_complete': 'Analysis complete!',
        'analysis_interrupted': 'Analysis interrupted',
        
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
    },
    'de': {
        # Loading and initialization
        'loading_model': 'Lade YOLO-Modell:',
        'model_not_found': "Modell '{model_name}' lokal nicht gefunden, wird automatisch heruntergeladen...",
        
        # Video analysis
        'analyzing': 'Analysiere:',
        'video_not_found': 'Video nicht gefunden: {path}',
        'cannot_open_video': 'Kann Video nicht öffnen: {path}',
        'video_info': 'Video-Info:',
        'frames': 'Frames',
        'analyzing_every_nth': 'Analysiere jeden {n}. Frame...',
        'analysis_complete': 'Analyse abgeschlossen!',
        'analysis_interrupted': 'Analyse unterbrochen',
        
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
