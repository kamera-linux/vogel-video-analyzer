"""
Internationalization (i18n) module for vogel-video-analyzer
Provides translations for command-line output
"""

import os
import locale


# Available translations
TRANSLATIONS = {
    'en': {
        # Report headers
        'report_title': '🎬 Video Analysis Report',
        'file': 'File',
        'total_frames': 'Total Frames',
        'analyzed': 'analyzed',
        'duration': 'Duration',
        'bird_frames': 'Bird Frames',
        'bird_segments': 'Bird Segments',
        'detected_segments': 'Detected Segments',
        'segment': 'Segment',
        'bird_frames_lower': 'bird frames',
        'status': 'Status',
        'status_significant': 'Significant bird activity detected',
        'status_minimal': 'Minimal bird activity detected',
        'status_none': 'No bird activity detected',
        
        # Summary
        'summary': 'SUMMARY',
        'videos': 'Videos',
        'total_duration': 'Total Duration',
        'total_frames_analyzed': 'Total Frames Analyzed',
        'total_frames_with_birds': 'Total Frames with Birds',
        'average_bird_content': 'Average Bird Content',
        'video_overview': 'Video Overview',
        'nr': 'Nr.',
        'directory': 'Directory',
        'bird': 'Bird',
        'bird_pct': 'Bird%',
        'frames': 'Frames',
        
        # Deletion
        'deleting_files': '🗑️  DELETING VIDEO FILES WITH 0% BIRD CONTENT',
        'deleting_folders': '🗑️  DELETING FOLDERS WITH 0% BIRD CONTENT',
        'files': 'files',
        'deleting': 'Deleting',
        'deleting_folder': 'Deleting folder',
        'successfully_deleted': 'Successfully deleted',
        'error_deleting': 'Error deleting',
        'deleted_files': 'Deleted files',
        'deleted_folders': 'Deleted folders',
        'remaining_videos': 'Remaining videos',
        'no_files_found': 'No video files with 0% bird content found',
        'no_folders_found': 'No folders with 0% bird content found',
        
        # Log messages
        'log_file': 'Log file',
        'warning': 'WARNING',
        'no_write_permissions': 'No write permissions for',
        'run_with_sudo': 'Run with sudo or change permissions',
        'analysis_interrupted': 'Analysis interrupted',
        'error': 'Error',
        'error_analyzing': 'Error analyzing',
        
        # Deprecation
        'deprecation_warning': 'WARNING: --delete is deprecated. Use --delete-file or --delete-folder instead.',
        'defaulting_to': 'Defaulting to --delete-folder behavior for backward compatibility.',
        
        # Report saving
        'report_saved': 'Report saved',
    },
    'de': {
        # Report headers
        'report_title': '🎬 Video-Analyse-Bericht',
        'file': 'Datei',
        'total_frames': 'Gesamt-Frames',
        'analyzed': 'analysiert',
        'duration': 'Dauer',
        'bird_frames': 'Vogel-Frames',
        'bird_segments': 'Vogel-Segmente',
        'detected_segments': 'Erkannte Segmente',
        'segment': 'Segment',
        'bird_frames_lower': 'Vogel-Frames',
        'status': 'Status',
        'status_significant': 'Signifikante Vogelaktivität erkannt',
        'status_minimal': 'Minimale Vogelaktivität erkannt',
        'status_none': 'Keine Vogelaktivität erkannt',
        
        # Summary
        'summary': 'ZUSAMMENFASSUNG',
        'videos': 'Videos',
        'total_duration': 'Gesamtdauer',
        'total_frames_analyzed': 'Gesamt analysierte Frames',
        'total_frames_with_birds': 'Gesamt Frames mit Vögeln',
        'average_bird_content': 'Durchschnittlicher Vogelinhalt',
        'video_overview': 'Video-Übersicht',
        'nr': 'Nr.',
        'directory': 'Verzeichnis',
        'bird': 'Vogel',
        'bird_pct': 'Vogel%',
        'frames': 'Frames',
        
        # Deletion
        'deleting_files': '🗑️  LÖSCHE VIDEODATEIEN MIT 0% VOGELINHALT',
        'deleting_folders': '🗑️  LÖSCHE ORDNER MIT 0% VOGELINHALT',
        'files': 'Dateien',
        'deleting': 'Lösche',
        'deleting_folder': 'Lösche Ordner',
        'successfully_deleted': 'Erfolgreich gelöscht',
        'error_deleting': 'Fehler beim Löschen',
        'deleted_files': 'Gelöschte Dateien',
        'deleted_folders': 'Gelöschte Ordner',
        'remaining_videos': 'Verbleibende Videos',
        'no_files_found': 'Keine Videodateien mit 0% Vogelinhalt gefunden',
        'no_folders_found': 'Keine Ordner mit 0% Vogelinhalt gefunden',
        
        # Log messages
        'log_file': 'Log-Datei',
        'warning': 'WARNUNG',
        'no_write_permissions': 'Keine Schreibrechte für',
        'run_with_sudo': 'Mit sudo ausführen oder Berechtigungen ändern',
        'analysis_interrupted': 'Analyse unterbrochen',
        'error': 'Fehler',
        'error_analyzing': 'Fehler beim Analysieren',
        
        # Deprecation
        'deprecation_warning': 'WARNUNG: --delete ist veraltet. Verwenden Sie --delete-file oder --delete-folder.',
        'defaulting_to': 'Standardmäßig wird --delete-folder Verhalten für Rückwärtskompatibilität verwendet.',
        
        # Report saving
        'report_saved': 'Bericht gespeichert',
    }
}


class I18n:
    """Internationalization handler"""
    
    def __init__(self, language=None):
        """
        Initialize i18n handler
        
        Args:
            language: Language code ('en', 'de', etc.) or None for auto-detection
        """
        if language:
            self.language = language
        else:
            self.language = self._detect_language()
        
        # Fallback to English if language not supported
        if self.language not in TRANSLATIONS:
            self.language = 'en'
    
    def _detect_language(self):
        """Auto-detect system language"""
        # Try VOGEL_LANG environment variable first
        vogel_lang = os.getenv('VOGEL_LANG')
        if vogel_lang:
            return vogel_lang.split('_')[0].lower()
        
        # Try LANG environment variable
        lang_env = os.getenv('LANG', '')
        if lang_env:
            return lang_env.split('_')[0].lower()
        
        # Try locale
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                return system_locale.split('_')[0].lower()
        except:
            pass
        
        # Default to English
        return 'en'
    
    def t(self, key):
        """
        Translate a key
        
        Args:
            key: Translation key
            
        Returns:
            Translated string
        """
        return TRANSLATIONS[self.language].get(key, TRANSLATIONS['en'].get(key, key))
    
    def get_language(self):
        """Get current language code"""
        return self.language


# Global instance (will be initialized in CLI)
_i18n_instance = None


def init_i18n(language=None):
    """Initialize global i18n instance"""
    global _i18n_instance
    _i18n_instance = I18n(language)
    return _i18n_instance


def get_i18n():
    """Get global i18n instance"""
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18n()
    return _i18n_instance


def t(key):
    """Convenience function for translation"""
    return get_i18n().t(key)
