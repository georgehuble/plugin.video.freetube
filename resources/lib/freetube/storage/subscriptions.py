# -*- coding: utf-8 -*-
"""
    Subscriptions Manager - Local Channel Subscriptions
    
    Manage channel subscriptions without YouTube account
    Based on FreeTube's subscription system
    
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


class SubscriptionsManager:
    """Manage local channel subscriptions"""
    
    def __init__(self, database):
        """
        Initialize subscriptions manager
        
        Args:
            database: Database instance
        """
        self.db = database
    
    def subscribe(self, profile_id, channel_id, channel_name, channel_thumbnail=None):
        """
        Subscribe to a channel
        
        Args:
            profile_id: Profile ID
            channel_id: YouTube channel ID
            channel_name: Channel name
            channel_thumbnail: Channel thumbnail URL (optional)
            
        Returns:
            bool: True if subscribed successfully
        """
        now = int(time.time())
        
        try:
            self.db.execute('''
                INSERT OR IGNORE INTO subscriptions 
                (profile_id, channel_id, channel_name, channel_thumbnail, subscribed_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (profile_id, channel_id, channel_name, channel_thumbnail, now))
            
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Subscribed to channel: {channel_name} ({channel_id})', xbmc.LOGINFO)
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Subscribe error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def unsubscribe(self, profile_id, channel_id):
        """
        Unsubscribe from a channel
        
        Args:
            profile_id: Profile ID
            channel_id: YouTube channel ID
            
        Returns:
            bool: True if unsubscribed successfully
        """
        try:
            self.db.execute('''
                DELETE FROM subscriptions 
                WHERE profile_id = ? AND channel_id = ?
            ''', (profile_id, channel_id))
            
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Unsubscribed from channel: {channel_id}', xbmc.LOGINFO)
            
            return True
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Unsubscribe error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def is_subscribed(self, profile_id, channel_id):
        """
        Check if subscribed to a channel
        
        Args:
            profile_id: Profile ID
            channel_id: YouTube channel ID
            
        Returns:
            bool: True if subscribed
        """
        result = self.db.execute('''
            SELECT COUNT(*) as count FROM subscriptions 
            WHERE profile_id = ? AND channel_id = ?
        ''', (profile_id, channel_id))
        
        return result[0]['count'] > 0 if result else False
    
    def get_subscriptions(self, profile_id, sort_by='name'):
        """
        Get all subscriptions for a profile
        
        Args:
            profile_id: Profile ID
            sort_by: 'name' or 'date' (subscription date)
            
        Returns:
            list: List of subscriptions
        """
        order_clause = 'channel_name ASC' if sort_by == 'name' else 'subscribed_at DESC'
        
        result = self.db.execute(f'''
            SELECT * FROM subscriptions 
            WHERE profile_id = ?
            ORDER BY {order_clause}
        ''', (profile_id,))
        
        return [dict(row) for row in result]
    
    def get_subscription_count(self, profile_id):
        """
        Get subscription count for a profile
        
        Args:
            profile_id: Profile ID
            
        Returns:
            int: Number of subscriptions
        """
        result = self.db.execute('''
            SELECT COUNT(*) as count FROM subscriptions 
            WHERE profile_id = ?
        ''', (profile_id,))
        
        return result[0]['count'] if result else 0
    
    def search_subscriptions(self, profile_id, query):
        """
        Search subscriptions by channel name
        
        Args:
            profile_id: Profile ID
            query: Search query
            
        Returns:
            list: Matching subscriptions
        """
        result = self.db.execute('''
            SELECT * FROM subscriptions 
            WHERE profile_id = ? AND channel_name LIKE ?
            ORDER BY channel_name ASC
        ''', (profile_id, f'%{query}%'))
        
        return [dict(row) for row in result]
    
    def import_subscriptions(self, profile_id, channels, clear_existing=False):
        """
        Import multiple subscriptions
        
        Args:
            profile_id: Profile ID
            channels: List of channel dicts with keys: channel_id, channel_name, channel_thumbnail
            clear_existing: Clear existing subscriptions before import
            
        Returns:
            int: Number of imported subscriptions
        """
        if clear_existing:
            self.db.execute('DELETE FROM subscriptions WHERE profile_id = ?', (profile_id,))
        
        now = int(time.time())
        imported = 0
        
        for channel in channels:
            try:
                self.db.execute('''
                    INSERT OR IGNORE INTO subscriptions 
                    (profile_id, channel_id, channel_name, channel_thumbnail, subscribed_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    profile_id,
                    channel['channel_id'],
                    channel['channel_name'],
                    channel.get('channel_thumbnail'),
                    now
                ))
                imported += 1
            except Exception:
                continue
        
        if KODI_MODE:
            xbmc.log(f'[FreeTube] Imported {imported} subscriptions', xbmc.LOGINFO)
        
        return imported
    
    def export_subscriptions(self, profile_id, format='freetube'):
        """
        Export subscriptions in various formats
        
        Args:
            profile_id: Profile ID
            format: 'freetube', 'youtube', 'opml', 'newpipe'
            
        Returns:
            str or dict: Exported data
        """
        subscriptions = self.get_subscriptions(profile_id)
        
        if format == 'freetube':
            # FreeTube .db format (JSON lines)
            return '\n'.join([
                f'{{"channel_id": "{sub["channel_id"]}", "channel_name": "{sub["channel_name"]}", "channel_thumbnail": "{sub.get("channel_thumbnail", "")}"}}' 
                for sub in subscriptions
            ])
        
        elif format == 'youtube':
            # YouTube CSV format
            csv_lines = ['Channel Id,Channel Url,Channel Title']
            for sub in subscriptions:
                csv_lines.append(f'{sub["channel_id"]},https://www.youtube.com/channel/{sub["channel_id"]},{sub["channel_name"]}')
            return '\n'.join(csv_lines)
        
        elif format == 'opml':
            # OPML format
            opml = ['<?xml version="1.0" encoding="UTF-8"?>', '<opml version="1.1">', '<body>', '<outline text="YouTube Subscriptions" title="YouTube Subscriptions">']
            for sub in subscriptions:
                opml.append(f'<outline text="{sub["channel_name"]}" title="{sub["channel_name"]}" type="rss" xmlUrl="https://www.youtube.com/feeds/videos.xml?channel_id={sub["channel_id"]}" />')
            opml.extend(['</outline>', '</body>', '</opml>'])
            return '\n'.join(opml)
        
        elif format == 'newpipe':
            # NewPipe JSON format
            import json
            newpipe_data = {
                'app_version': '0.19.8',
                'app_version_int': 953,
                'subscriptions': []
            }
            for sub in subscriptions:
                newpipe_data['subscriptions'].append({
                    'service_id': 0,
                    'url': f'https://www.youtube.com/channel/{sub["channel_id"]}',
                    'name': sub["channel_name"]
                })
            return json.dumps(newpipe_data, indent=2)
        
        return subscriptions

