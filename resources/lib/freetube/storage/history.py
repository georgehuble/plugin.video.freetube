# -*- coding: utf-8 -*-
"""
    History Manager - Watch History Tracking
    
    Track watched videos locally without YouTube account
    Based on FreeTube's history system
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import time

try:
    import xbmc
    KODI_MODE = True
except ImportError:
    KODI_MODE = False


class HistoryManager:
    """Manage local watch history"""
    
    def __init__(self, database):
        """
        Initialize history manager
        
        Args:
            database: Database instance
        """
        self.db = database
    
    def add_to_history(self, profile_id, video_id, title, author=None, channel_id=None,
                       length_seconds=None, thumbnail=None, watch_progress=0):
        """
        Add video to watch history
        
        Args:
            profile_id: Profile ID
            video_id: YouTube video ID
            title: Video title
            author: Video author/channel name
            channel_id: Channel ID
            length_seconds: Video duration
            thumbnail: Video thumbnail URL
            watch_progress: Watch progress (0-1)
            
        Returns:
            bool: True if added successfully
        """
        now = int(time.time())
        
        try:
            # Check if video already in history
            existing = self.db.execute('''
                SELECT id FROM history 
                WHERE profile_id = ? AND video_id = ?
            ''', (profile_id, video_id))
            
            if existing:
                # Update existing entry
                self.db.execute('''
                    UPDATE history 
                    SET title = ?, author = ?, channel_id = ?, length_seconds = ?, 
                        thumbnail = ?, watched_at = ?, watch_progress = ?
                    WHERE profile_id = ? AND video_id = ?
                ''', (title, author, channel_id, length_seconds, thumbnail, now, 
                     watch_progress, profile_id, video_id))
            else:
                # Insert new entry
                self.db.execute('''
                    INSERT INTO history 
                    (profile_id, video_id, title, author, channel_id, length_seconds, 
                     thumbnail, watched_at, watch_progress)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (profile_id, video_id, title, author, channel_id, length_seconds, 
                     thumbnail, now, watch_progress))
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] History add error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def remove_from_history(self, profile_id, video_id):
        """
        Remove video from history
        
        Args:
            profile_id: Profile ID
            video_id: YouTube video ID
            
        Returns:
            bool: True if removed successfully
        """
        try:
            self.db.execute('''
                DELETE FROM history 
                WHERE profile_id = ? AND video_id = ?
            ''', (profile_id, video_id))
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] History remove error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def clear_history(self, profile_id):
        """
        Clear all history for a profile
        
        Args:
            profile_id: Profile ID
            
        Returns:
            bool: True if cleared successfully
        """
        try:
            self.db.execute('DELETE FROM history WHERE profile_id = ?', (profile_id,))
            if KODI_MODE:
                xbmc.log('[FreeTube] History cleared', xbmc.LOGINFO)
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] History clear error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def get_history(self, profile_id, limit=100, offset=0):
        """
        Get watch history
        
        Args:
            profile_id: Profile ID
            limit: Maximum number of items
            offset: Offset for pagination
            
        Returns:
            list: History items
        """
        result = self.db.execute('''
            SELECT * FROM history 
            WHERE profile_id = ?
            ORDER BY watched_at DESC
            LIMIT ? OFFSET ?
        ''', (profile_id, limit, offset))
        
        return [dict(row) for row in result]
    
    def get_history_count(self, profile_id):
        """
        Get history count
        
        Args:
            profile_id: Profile ID
            
        Returns:
            int: Number of history items
        """
        result = self.db.execute('''
            SELECT COUNT(*) as count FROM history 
            WHERE profile_id = ?
        ''', (profile_id,))
        
        return result[0]['count'] if result else 0
    
    def search_history(self, profile_id, query):
        """
        Search history by title
        
        Args:
            profile_id: Profile ID
            query: Search query
            
        Returns:
            list: Matching history items
        """
        result = self.db.execute('''
            SELECT * FROM history 
            WHERE profile_id = ? AND title LIKE ?
            ORDER BY watched_at DESC
        ''', (profile_id, f'%{query}%'))
        
        return [dict(row) for row in result]
    
    def is_in_history(self, profile_id, video_id):
        """
        Check if video is in history
        
        Args:
            profile_id: Profile ID
            video_id: YouTube video ID
            
        Returns:
            bool: True if in history
        """
        result = self.db.execute('''
            SELECT COUNT(*) as count FROM history 
            WHERE profile_id = ? AND video_id = ?
        ''', (profile_id, video_id))
        
        return result[0]['count'] > 0 if result else False
    
    def get_watch_progress(self, profile_id, video_id):
        """
        Get watch progress for a video
        
        Args:
            profile_id: Profile ID
            video_id: YouTube video ID
            
        Returns:
            float: Watch progress (0-1) or None
        """
        result = self.db.execute('''
            SELECT watch_progress FROM history 
            WHERE profile_id = ? AND video_id = ?
        ''', (profile_id, video_id))
        
        return result[0]['watch_progress'] if result else None
    
    def export_history(self, profile_id):
        """
        Export watch history
        
        Args:
            profile_id: Profile ID
            
        Returns:
            str: JSON lines format (FreeTube compatible)
        """
        history = self.get_history(profile_id, limit=999999)
        
        lines = []
        for item in history:
            import json
            lines.append(json.dumps({
                'video_id': item['video_id'],
                'title': item['title'],
                'author': item['author'],
                'channel_id': item['channel_id'],
                'length_seconds': item['length_seconds'],
                'thumbnail': item['thumbnail'],
                'watched_at': item['watched_at'],
                'watch_progress': item['watch_progress']
            }))
        
        return '\n'.join(lines) + '\n'
    
    def import_history(self, profile_id, history_data, clear_existing=False):
        """
        Import watch history
        
        Args:
            profile_id: Profile ID
            history_data: JSON lines string or list of dicts
            clear_existing: Clear existing history before import
            
        Returns:
            int: Number of imported items
        """
        if clear_existing:
            self.clear_history(profile_id)
        
        # Parse history data
        if isinstance(history_data, str):
            import json
            items = []
            for line in history_data.strip().split('\n'):
                if line:
                    try:
                        items.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        else:
            items = history_data
        
        imported = 0
        for item in items:
            try:
                self.add_to_history(
                    profile_id,
                    item['video_id'],
                    item['title'],
                    item.get('author'),
                    item.get('channel_id'),
                    item.get('length_seconds'),
                    item.get('thumbnail'),
                    item.get('watch_progress', 0)
                )
                imported += 1
            except Exception:
                continue
        
        if KODI_MODE:
            xbmc.log(f'[FreeTube] Imported {imported} history items', xbmc.LOGINFO)
        
        return imported

