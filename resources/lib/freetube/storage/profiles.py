# -*- coding: utf-8 -*-
"""
    Profiles Manager - User Profiles
    
    Manage multiple user profiles with separate subscriptions/history
    Based on FreeTube's profile system
    
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


class ProfilesManager:
    """Manage user profiles"""
    
    def __init__(self, database):
        """
        Initialize profiles manager
        
        Args:
            database: Database instance
        """
        self.db = database
    
    def create_profile(self, name, color='#FF0000', is_default=False):
        """
        Create new profile
        
        Args:
            name: Profile name
            color: Profile color (hex)
            is_default: Set as default profile
            
        Returns:
            str: Profile ID or None
        """
        profile_id = str(uuid.uuid4())
        now = int(time.time())
        
        try:
            # If setting as default, unset other defaults
            if is_default:
                self.db.execute('UPDATE profiles SET is_default = 0')
            
            self.db.execute('''
                INSERT INTO profiles (profile_id, name, color, is_default, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (profile_id, name, color, 1 if is_default else 0, now, now))
            
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Profile created: {name} ({profile_id})', xbmc.LOGINFO)
            
            return profile_id
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Profile create error: {str(e)}', xbmc.LOGERROR)
            return None
    
    def update_profile(self, profile_id, name=None, color=None, is_default=None):
        """
        Update profile
        
        Args:
            profile_id: Profile ID
            name: New profile name (optional)
            color: New profile color (optional)
            is_default: Set as default (optional)
            
        Returns:
            bool: True if updated successfully
        """
        now = int(time.time())
        
        try:
            # Build update query dynamically
            updates = []
            params = []
            
            if name is not None:
                updates.append('name = ?')
                params.append(name)
            
            if color is not None:
                updates.append('color = ?')
                params.append(color)
            
            if is_default is not None:
                # Unset other defaults
                if is_default:
                    self.db.execute('UPDATE profiles SET is_default = 0')
                updates.append('is_default = ?')
                params.append(1 if is_default else 0)
            
            updates.append('updated_at = ?')
            params.append(now)
            
            params.append(profile_id)
            
            if updates:
                query = f'UPDATE profiles SET {", ".join(updates)} WHERE profile_id = ?'
                self.db.execute(query, tuple(params))
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Profile update error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def delete_profile(self, profile_id):
        """
        Delete profile (and all associated data)
        
        Args:
            profile_id: Profile ID
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            # Check if this is the only profile
            profiles = self.get_all_profiles()
            if len(profiles) <= 1:
                if KODI_MODE:
                    xbmc.log('[FreeTube] Cannot delete last profile', xbmc.LOGWARNING)
                return False
            
            # Check if this is the default profile
            is_default = self.db.execute('''
                SELECT is_default FROM profiles WHERE profile_id = ?
            ''', (profile_id,))
            
            self.db.execute('DELETE FROM profiles WHERE profile_id = ?', (profile_id,))
            
            # If deleted profile was default, set another as default
            if is_default and is_default[0]['is_default']:
                remaining = self.get_all_profiles()
                if remaining:
                    self.update_profile(remaining[0]['profile_id'], is_default=True)
            
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Profile deleted: {profile_id}', xbmc.LOGINFO)
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Profile delete error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def get_profile(self, profile_id):
        """
        Get profile by ID
        
        Args:
            profile_id: Profile ID
            
        Returns:
            dict: Profile data or None
        """
        result = self.db.execute('''
            SELECT * FROM profiles WHERE profile_id = ?
        ''', (profile_id,))
        
        return dict(result[0]) if result else None
    
    def get_default_profile(self):
        """
        Get default profile
        
        Returns:
            dict: Profile data or None
        """
        result = self.db.execute('''
            SELECT * FROM profiles WHERE is_default = 1
        ''')
        
        if not result:
            # If no default, get first profile
            result = self.db.execute('SELECT * FROM profiles ORDER BY created_at ASC LIMIT 1')
        
        return dict(result[0]) if result else None
    
    def get_all_profiles(self):
        """
        Get all profiles
        
        Returns:
            list: List of profiles
        """
        result = self.db.execute('''
            SELECT * FROM profiles ORDER BY name ASC
        ''')
        
        return [dict(row) for row in result]
    
    def set_default_profile(self, profile_id):
        """
        Set profile as default
        
        Args:
            profile_id: Profile ID
            
        Returns:
            bool: True if set successfully
        """
        return self.update_profile(profile_id, is_default=True)
    
    def get_profile_stats(self, profile_id):
        """
        Get profile statistics
        
        Args:
            profile_id: Profile ID
            
        Returns:
            dict: Profile statistics
        """
        # Subscription count
        sub_count = self.db.execute('''
            SELECT COUNT(*) as count FROM subscriptions WHERE profile_id = ?
        ''', (profile_id,))
        
        # History count
        hist_count = self.db.execute('''
            SELECT COUNT(*) as count FROM history WHERE profile_id = ?
        ''', (profile_id,))
        
        # Playlist count
        pl_count = self.db.execute('''
            SELECT COUNT(*) as count FROM playlists WHERE profile_id = ?
        ''', (profile_id,))
        
        return {
            'subscriptions': sub_count[0]['count'] if sub_count else 0,
            'history': hist_count[0]['count'] if hist_count else 0,
            'playlists': pl_count[0]['count'] if pl_count else 0,
        }

