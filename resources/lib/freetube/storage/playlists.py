# -*- coding: utf-8 -*-
"""
    Playlists Manager - Local Playlists
    
    Manage local video playlists without YouTube account
    Based on FreeTube's playlist system
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import time
import uuid

try:
    import xbmc
    KODI_MODE = True
except ImportError:
    KODI_MODE = False


class PlaylistsManager:
    """Manage local playlists"""
    
    def __init__(self, database):
        """
        Initialize playlists manager
        
        Args:
            database: Database instance
        """
        self.db = database
    
    def create_playlist(self, profile_id, name, description=''):
        """
        Create new playlist
        
        Args:
            profile_id: Profile ID
            name: Playlist name
            description: Playlist description
            
        Returns:
            str: Playlist ID or None
        """
        playlist_id = str(uuid.uuid4())
        now = int(time.time())
        
        try:
            self.db.execute('''
                INSERT INTO playlists (profile_id, playlist_id, name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (profile_id, playlist_id, name, description, now, now))
            
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist created: {name} ({playlist_id})', xbmc.LOGINFO)
            
            return playlist_id
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist create error: {str(e)}', xbmc.LOGERROR)
            return None
    
    def update_playlist(self, playlist_id, name=None, description=None):
        """
        Update playlist
        
        Args:
            playlist_id: Playlist ID
            name: New playlist name (optional)
            description: New description (optional)
            
        Returns:
            bool: True if updated successfully
        """
        now = int(time.time())
        
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append('name = ?')
                params.append(name)
            
            if description is not None:
                updates.append('description = ?')
                params.append(description)
            
            updates.append('updated_at = ?')
            params.append(now)
            
            params.append(playlist_id)
            
            if updates:
                query = f'UPDATE playlists SET {", ".join(updates)} WHERE playlist_id = ?'
                self.db.execute(query, tuple(params))
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist update error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def delete_playlist(self, playlist_id):
        """
        Delete playlist (and all videos in it)
        
        Args:
            playlist_id: Playlist ID
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            self.db.execute('DELETE FROM playlists WHERE playlist_id = ?', (playlist_id,))
            
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist deleted: {playlist_id}', xbmc.LOGINFO)
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist delete error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def get_playlist(self, playlist_id):
        """
        Get playlist info
        
        Args:
            playlist_id: Playlist ID
            
        Returns:
            dict: Playlist data or None
        """
        result = self.db.execute('''
            SELECT * FROM playlists WHERE playlist_id = ?
        ''', (playlist_id,))
        
        return dict(result[0]) if result else None
    
    def get_all_playlists(self, profile_id):
        """
        Get all playlists for a profile
        
        Args:
            profile_id: Profile ID
            
        Returns:
            list: List of playlists
        """
        result = self.db.execute('''
            SELECT p.*, COUNT(pv.id) as video_count
            FROM playlists p
            LEFT JOIN playlist_videos pv ON p.playlist_id = pv.playlist_id
            WHERE p.profile_id = ?
            GROUP BY p.playlist_id
            ORDER BY p.name ASC
        ''', (profile_id,))
        
        return [dict(row) for row in result]
    
    def add_video_to_playlist(self, playlist_id, video_id, title, author=None,
                             channel_id=None, length_seconds=None, thumbnail=None):
        """
        Add video to playlist
        
        Args:
            playlist_id: Playlist ID
            video_id: YouTube video ID
            title: Video title
            author: Video author
            channel_id: Channel ID
            length_seconds: Video duration
            thumbnail: Video thumbnail URL
            
        Returns:
            bool: True if added successfully
        """
        now = int(time.time())
        
        try:
            # Get next position
            result = self.db.execute('''
                SELECT COALESCE(MAX(position), -1) + 1 as next_pos
                FROM playlist_videos
                WHERE playlist_id = ?
            ''', (playlist_id,))
            next_position = result[0]['next_pos'] if result else 0
            
            # Insert video
            self.db.execute('''
                INSERT OR IGNORE INTO playlist_videos
                (playlist_id, video_id, title, author, channel_id, length_seconds, 
                 thumbnail, position, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (playlist_id, video_id, title, author, channel_id, length_seconds,
                 thumbnail, next_position, now))
            
            # Update playlist timestamp
            self.db.execute('''
                UPDATE playlists SET updated_at = ? WHERE playlist_id = ?
            ''', (now, playlist_id))
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist add video error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def remove_video_from_playlist(self, playlist_id, video_id):
        """
        Remove video from playlist
        
        Args:
            playlist_id: Playlist ID
            video_id: YouTube video ID
            
        Returns:
            bool: True if removed successfully
        """
        now = int(time.time())
        
        try:
            self.db.execute('''
                DELETE FROM playlist_videos
                WHERE playlist_id = ? AND video_id = ?
            ''', (playlist_id, video_id))
            
            # Reorder remaining videos
            videos = self.db.execute('''
                SELECT id FROM playlist_videos
                WHERE playlist_id = ?
                ORDER BY position ASC
            ''', (playlist_id,))
            
            for idx, video in enumerate(videos):
                self.db.execute('''
                    UPDATE playlist_videos SET position = ?
                    WHERE id = ?
                ''', (idx, video['id']))
            
            # Update playlist timestamp
            self.db.execute('''
                UPDATE playlists SET updated_at = ? WHERE playlist_id = ?
            ''', (now, playlist_id))
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist remove video error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def get_playlist_videos(self, playlist_id, limit=None, offset=0):
        """
        Get videos in playlist
        
        Args:
            playlist_id: Playlist ID
            limit: Maximum number of videos (optional)
            offset: Offset for pagination
            
        Returns:
            list: List of videos
        """
        query = '''
            SELECT * FROM playlist_videos
            WHERE playlist_id = ?
            ORDER BY position ASC
        '''
        
        params = [playlist_id]
        
        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])
        
        result = self.db.execute(query, tuple(params))
        
        return [dict(row) for row in result]
    
    def get_playlist_video_count(self, playlist_id):
        """
        Get video count in playlist
        
        Args:
            playlist_id: Playlist ID
            
        Returns:
            int: Number of videos
        """
        result = self.db.execute('''
            SELECT COUNT(*) as count FROM playlist_videos
            WHERE playlist_id = ?
        ''', (playlist_id,))
        
        return result[0]['count'] if result else 0
    
    def is_video_in_playlist(self, playlist_id, video_id):
        """
        Check if video is in playlist
        
        Args:
            playlist_id: Playlist ID
            video_id: YouTube video ID
            
        Returns:
            bool: True if video is in playlist
        """
        result = self.db.execute('''
            SELECT COUNT(*) as count FROM playlist_videos
            WHERE playlist_id = ? AND video_id = ?
        ''', (playlist_id, video_id))
        
        return result[0]['count'] > 0 if result else False
    
    def reorder_playlist_videos(self, playlist_id, video_ids_in_order):
        """
        Reorder videos in playlist
        
        Args:
            playlist_id: Playlist ID
            video_ids_in_order: List of video IDs in desired order
            
        Returns:
            bool: True if reordered successfully
        """
        now = int(time.time())
        
        try:
            for idx, video_id in enumerate(video_ids_in_order):
                self.db.execute('''
                    UPDATE playlist_videos
                    SET position = ?
                    WHERE playlist_id = ? AND video_id = ?
                ''', (idx, playlist_id, video_id))
            
            # Update playlist timestamp
            self.db.execute('''
                UPDATE playlists SET updated_at = ? WHERE playlist_id = ?
            ''', (now, playlist_id))
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist reorder error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def clear_playlist(self, playlist_id):
        """
        Clear all videos from playlist
        
        Args:
            playlist_id: Playlist ID
            
        Returns:
            bool: True if cleared successfully
        """
        now = int(time.time())
        
        try:
            self.db.execute('''
                DELETE FROM playlist_videos WHERE playlist_id = ?
            ''', (playlist_id,))
            
            # Update playlist timestamp
            self.db.execute('''
                UPDATE playlists SET updated_at = ? WHERE playlist_id = ?
            ''', (now, playlist_id))
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Playlist clear error: {str(e)}', xbmc.LOGERROR)
            return False

