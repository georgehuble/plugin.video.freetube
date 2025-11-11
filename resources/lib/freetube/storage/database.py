# -*- coding: utf-8 -*-
"""
    Database Manager - Local SQLite Storage
    
    Manages all local data storage for FreeTube Kodi plugin
    Based on FreeTube's NeDB storage structure
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import os
import sqlite3
import json
from contextlib import contextmanager

try:
    import xbmc
    import xbmcaddon
    import xbmcvfs
    KODI_MODE = True
    addon = xbmcaddon.Addon()
    ADDON_ID = addon.getAddonInfo('id')
    ADDON_DATA_PATH = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
except ImportError:
    KODI_MODE = False
    ADDON_ID = 'plugin.video.freetube'
    ADDON_DATA_PATH = os.path.expanduser('~/.kodi/userdata/addon_data/' + ADDON_ID)


class Database:
    """
    Local SQLite database for FreeTube data
    Stores: subscriptions, history, profiles, playlists
    """
    
    DB_VERSION = 1
    DB_NAME = 'freetube.db'
    
    def __init__(self, db_path=None):
        """
        Initialize database
        
        Args:
            db_path: Custom database path (optional)
        """
        if db_path:
            self.db_path = db_path
        else:
            # Create addon data directory if it doesn't exist
            if not os.path.exists(ADDON_DATA_PATH):
                os.makedirs(ADDON_DATA_PATH)
            self.db_path = os.path.join(ADDON_DATA_PATH, self.DB_NAME)
        
        self._initialize_database()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Database error: {str(e)}', xbmc.LOGERROR)
            raise
        finally:
            conn.close()
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    color TEXT DEFAULT '#FF0000',
                    is_default INTEGER DEFAULT 0,
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL
                )
            ''')
            
            # Subscriptions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    channel_name TEXT NOT NULL,
                    channel_thumbnail TEXT,
                    subscribed_at INTEGER NOT NULL,
                    UNIQUE(profile_id, channel_id),
                    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id) ON DELETE CASCADE
                )
            ''')
            
            # Watch history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT NOT NULL,
                    video_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT,
                    channel_id TEXT,
                    length_seconds INTEGER,
                    thumbnail TEXT,
                    watched_at INTEGER NOT NULL,
                    watch_progress REAL DEFAULT 0,
                    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id) ON DELETE CASCADE
                )
            ''')
            
            # Playlists table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT NOT NULL,
                    playlist_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL,
                    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id) ON DELETE CASCADE
                )
            ''')
            
            # Playlist videos table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS playlist_videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    playlist_id TEXT NOT NULL,
                    video_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT,
                    channel_id TEXT,
                    length_seconds INTEGER,
                    thumbnail TEXT,
                    position INTEGER NOT NULL,
                    added_at INTEGER NOT NULL,
                    UNIQUE(playlist_id, video_id),
                    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) ON DELETE CASCADE
                )
            ''')
            
            # Search history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT NOT NULL,
                    query TEXT NOT NULL,
                    searched_at INTEGER NOT NULL,
                    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id) ON DELETE CASCADE
                )
            ''')
            
            # Settings table (for storing plugin configuration)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at INTEGER NOT NULL
                )
            ''')
            
            # Create indices for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_subscriptions_profile ON subscriptions(profile_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_subscriptions_channel ON subscriptions(channel_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_profile ON history(profile_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_video ON history(video_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_watched_at ON history(watched_at DESC)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_playlists_profile ON playlists(profile_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_playlist_videos_playlist ON playlist_videos(playlist_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_history_profile ON search_history(profile_id)')
            
            # Check if we need to create default profile
            cursor.execute('SELECT COUNT(*) FROM profiles')
            if cursor.fetchone()[0] == 0:
                self._create_default_profile(cursor)
            
            conn.commit()
    
    def _create_default_profile(self, cursor):
        """Create default profile on first run"""
        import time
        import uuid
        
        profile_id = str(uuid.uuid4())
        now = int(time.time())
        
        cursor.execute('''
            INSERT INTO profiles (profile_id, name, color, is_default, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (profile_id, 'Default Profile', '#FF0000', 1, now, now))
        
        if KODI_MODE:
            xbmc.log('[FreeTube] Created default profile', xbmc.LOGINFO)
    
    def execute(self, query, params=None):
        """
        Execute SQL query
        
        Args:
            query: SQL query string
            params: Query parameters tuple
            
        Returns:
            list: Query results
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    def execute_many(self, query, params_list):
        """
        Execute multiple SQL queries with different parameters
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
    
    def get_setting(self, key, default=None):
        """
        Get setting value
        
        Args:
            key: Setting key
            default: Default value if setting doesn't exist
            
        Returns:
            Setting value or default
        """
        result = self.execute('SELECT value FROM settings WHERE key = ?', (key,))
        if result:
            try:
                return json.loads(result[0]['value'])
            except (json.JSONDecodeError, KeyError):
                return result[0]['value']
        return default
    
    def set_setting(self, key, value):
        """
        Set setting value
        
        Args:
            key: Setting key
            value: Setting value (will be JSON encoded)
        """
        import time
        
        value_str = json.dumps(value) if not isinstance(value, str) else value
        now = int(time.time())
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, ?)
            ''', (key, value_str, now))
    
    def clear_all_data(self):
        """Clear all data from database (except settings)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM playlist_videos')
            cursor.execute('DELETE FROM playlists')
            cursor.execute('DELETE FROM history')
            cursor.execute('DELETE FROM search_history')
            cursor.execute('DELETE FROM subscriptions')
            cursor.execute('DELETE FROM profiles')
            
            # Recreate default profile
            self._create_default_profile(cursor)
        
        if KODI_MODE:
            xbmc.log('[FreeTube] All data cleared', xbmc.LOGINFO)
    
    def export_data(self):
        """
        Export all data for backup
        
        Returns:
            dict: All database data
        """
        data = {}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Export profiles
            cursor.execute('SELECT * FROM profiles')
            data['profiles'] = [dict(row) for row in cursor.fetchall()]
            
            # Export subscriptions
            cursor.execute('SELECT * FROM subscriptions')
            data['subscriptions'] = [dict(row) for row in cursor.fetchall()]
            
            # Export history
            cursor.execute('SELECT * FROM history')
            data['history'] = [dict(row) for row in cursor.fetchall()]
            
            # Export playlists
            cursor.execute('SELECT * FROM playlists')
            data['playlists'] = [dict(row) for row in cursor.fetchall()]
            
            # Export playlist videos
            cursor.execute('SELECT * FROM playlist_videos')
            data['playlist_videos'] = [dict(row) for row in cursor.fetchall()]
            
            # Export search history
            cursor.execute('SELECT * FROM search_history')
            data['search_history'] = [dict(row) for row in cursor.fetchall()]
        
        return data
    
    def import_data(self, data):
        """
        Import data from backup
        
        Args:
            data: Data dictionary from export_data()
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Clear existing data
            cursor.execute('DELETE FROM playlist_videos')
            cursor.execute('DELETE FROM playlists')
            cursor.execute('DELETE FROM history')
            cursor.execute('DELETE FROM search_history')
            cursor.execute('DELETE FROM subscriptions')
            cursor.execute('DELETE FROM profiles')
            
            # Import profiles
            for profile in data.get('profiles', []):
                cursor.execute('''
                    INSERT INTO profiles (profile_id, name, color, is_default, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    profile['profile_id'],
                    profile['name'],
                    profile['color'],
                    profile['is_default'],
                    profile['created_at'],
                    profile['updated_at']
                ))
            
            # Import subscriptions
            for sub in data.get('subscriptions', []):
                cursor.execute('''
                    INSERT INTO subscriptions 
                    (profile_id, channel_id, channel_name, channel_thumbnail, subscribed_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    sub['profile_id'],
                    sub['channel_id'],
                    sub['channel_name'],
                    sub.get('channel_thumbnail'),
                    sub['subscribed_at']
                ))
            
            # Import history
            for item in data.get('history', []):
                cursor.execute('''
                    INSERT INTO history 
                    (profile_id, video_id, title, author, channel_id, length_seconds, 
                     thumbnail, watched_at, watch_progress)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['profile_id'],
                    item['video_id'],
                    item['title'],
                    item.get('author'),
                    item.get('channel_id'),
                    item.get('length_seconds'),
                    item.get('thumbnail'),
                    item['watched_at'],
                    item.get('watch_progress', 0)
                ))
            
            # Import playlists
            for playlist in data.get('playlists', []):
                cursor.execute('''
                    INSERT INTO playlists 
                    (profile_id, playlist_id, name, description, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    playlist['profile_id'],
                    playlist['playlist_id'],
                    playlist['name'],
                    playlist.get('description'),
                    playlist['created_at'],
                    playlist['updated_at']
                ))
            
            # Import playlist videos
            for video in data.get('playlist_videos', []):
                cursor.execute('''
                    INSERT INTO playlist_videos 
                    (playlist_id, video_id, title, author, channel_id, length_seconds, 
                     thumbnail, position, added_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    video['playlist_id'],
                    video['video_id'],
                    video['title'],
                    video.get('author'),
                    video.get('channel_id'),
                    video.get('length_seconds'),
                    video.get('thumbnail'),
                    video['position'],
                    video['added_at']
                ))
            
            # Import search history
            for search in data.get('search_history', []):
                cursor.execute('''
                    INSERT INTO search_history (profile_id, query, searched_at)
                    VALUES (?, ?, ?)
                ''', (search['profile_id'], search['query'], search['searched_at']))
        
        if KODI_MODE:
            xbmc.log('[FreeTube] Data imported successfully', xbmc.LOGINFO)

