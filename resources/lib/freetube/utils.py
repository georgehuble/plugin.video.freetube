# -*- coding: utf-8 -*-
"""
    FreeTube Utilities
    
    Helper functions and utilities
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import csv
import json
import xml.etree.ElementTree as ET

try:
    import xbmc
    import xbmcgui
    KODI_MODE = True
except ImportError:
    KODI_MODE = False


class SubscriptionImporter:
    """Import subscriptions from various formats"""
    
    @staticmethod
    def import_from_file(file_path):
        """
        Import subscriptions from file
        
        Args:
            file_path: Path to subscription file
            
        Returns:
            list: List of channel dicts or None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Detect format
            if file_path.endswith('.csv'):
                return SubscriptionImporter.parse_youtube_csv(content)
            elif file_path.endswith('.db'):
                return SubscriptionImporter.parse_freetube_db(content)
            elif file_path.endswith(('.xml', '.opml')):
                return SubscriptionImporter.parse_opml(content)
            elif file_path.endswith('.json'):
                return SubscriptionImporter.parse_json(content)
            else:
                return None
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Import error: {str(e)}', xbmc.LOGERROR)
            return None
    
    @staticmethod
    def parse_youtube_csv(content):
        """Parse YouTube subscription CSV"""
        channels = []
        
        try:
            lines = content.strip().split('\n')
            reader = csv.DictReader(lines)
            
            for row in reader:
                channel_id = row.get('Channel Id') or row.get('Channel ID')
                channel_name = row.get('Channel Title') or row.get('Channel Name')
                
                if channel_id and channel_name:
                    channels.append({
                        'channel_id': channel_id,
                        'channel_name': channel_name,
                        'channel_thumbnail': None
                    })
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] CSV parse error: {str(e)}', xbmc.LOGERROR)
        
        return channels
    
    @staticmethod
    def parse_freetube_db(content):
        """Parse FreeTube .db format (JSON lines)"""
        channels = []
        
        try:
            for line in content.strip().split('\n'):
                if not line:
                    continue
                
                data = json.loads(line)
                
                # Extract channel info
                if 'id' in data:
                    # FreeTube profile format
                    subscriptions = data.get('subscriptions', [])
                    for sub in subscriptions:
                        channels.append({
                            'channel_id': sub.get('id'),
                            'channel_name': sub.get('name'),
                            'channel_thumbnail': sub.get('thumbnail')
                        })
                elif 'channel_id' in data or 'id' in data:
                    # Direct subscription format
                    channels.append({
                        'channel_id': data.get('channel_id') or data.get('id'),
                        'channel_name': data.get('channel_name') or data.get('name'),
                        'channel_thumbnail': data.get('channel_thumbnail') or data.get('thumbnail')
                    })
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] FreeTube DB parse error: {str(e)}', xbmc.LOGERROR)
        
        return channels
    
    @staticmethod
    def parse_opml(content):
        """Parse OPML format"""
        channels = []
        
        try:
            root = ET.fromstring(content)
            
            # Find all outline elements
            for outline in root.findall('.//outline[@xmlUrl]'):
                xml_url = outline.get('xmlUrl', '')
                
                # Extract channel ID from XML URL
                if 'channel_id=' in xml_url:
                    channel_id = xml_url.split('channel_id=')[1].split('&')[0]
                    channel_name = outline.get('title') or outline.get('text')
                    
                    if channel_id and channel_name:
                        channels.append({
                            'channel_id': channel_id,
                            'channel_name': channel_name,
                            'channel_thumbnail': None
                        })
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] OPML parse error: {str(e)}', xbmc.LOGERROR)
        
        return channels
    
    @staticmethod
    def parse_json(content):
        """Parse JSON format (NewPipe or YouTube)"""
        channels = []
        
        try:
            data = json.loads(content)
            
            # NewPipe format
            if 'subscriptions' in data:
                for sub in data['subscriptions']:
                    url = sub.get('url', '')
                    
                    # Extract channel ID from URL
                    channel_id = None
                    if '/channel/' in url:
                        channel_id = url.split('/channel/')[1].split('?')[0].split('/')[0]
                    
                    if channel_id:
                        channels.append({
                            'channel_id': channel_id,
                            'channel_name': sub.get('name', ''),
                            'channel_thumbnail': None
                        })
            
            # YouTube format (list of subscription objects)
            elif isinstance(data, list):
                for item in data:
                    snippet = item.get('snippet', {})
                    resource_id = snippet.get('resourceId', {})
                    channel_id = resource_id.get('channelId')
                    
                    if channel_id:
                        channels.append({
                            'channel_id': channel_id,
                            'channel_name': snippet.get('title', ''),
                            'channel_thumbnail': snippet.get('thumbnails', {}).get('default', {}).get('url')
                        })
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] JSON parse error: {str(e)}', xbmc.LOGERROR)
        
        return channels


def format_duration(seconds):
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration (e.g., "1:23:45")
    """
    if not seconds:
        return "0:00"
    
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def format_number(number):
    """
    Format large numbers with K/M/B suffixes
    
    Args:
        number: Number to format
        
    Returns:
        str: Formatted number
    """
    try:
        number = int(number)
    except (ValueError, TypeError):
        return "0"
    
    if number >= 1000000000:
        return f"{number / 1000000000:.1f}B"
    elif number >= 1000000:
        return f"{number / 1000000:.1f}M"
    elif number >= 1000:
        return f"{number / 1000:.1f}K"
    else:
        return str(number)


def show_notification(title, message, icon=None, time_ms=5000):
    """
    Show Kodi notification
    
    Args:
        title: Notification title
        message: Notification message
        icon: Icon type or path
        time_ms: Display duration in milliseconds
    """
    if not KODI_MODE:
        return
    
    if icon is None:
        icon = xbmcgui.NOTIFICATION_INFO
    
    xbmcgui.Dialog().notification(title, message, icon, time_ms)


def show_text_input(heading, default=''):
    """
    Show text input dialog
    
    Args:
        heading: Dialog heading
        default: Default text
        
    Returns:
        str or None: Input text or None if cancelled
    """
    if not KODI_MODE:
        return None
    
    keyboard = xbmcgui.Dialog().input(heading, default, type=xbmcgui.INPUT_ALPHANUM)
    return keyboard if keyboard else None


def show_select_dialog(heading, items):
    """
    Show selection dialog
    
    Args:
        heading: Dialog heading
        items: List of items (strings)
        
    Returns:
        int: Selected index or -1 if cancelled
    """
    if not KODI_MODE:
        return -1
    
    return xbmcgui.Dialog().select(heading, items)


def show_ok_dialog(heading, message):
    """
    Show OK dialog
    
    Args:
        heading: Dialog heading
        message: Dialog message
    """
    if not KODI_MODE:
        return
    
    xbmcgui.Dialog().ok(heading, message)


def show_yes_no_dialog(heading, message):
    """
    Show Yes/No dialog
    
    Args:
        heading: Dialog heading
        message: Dialog message
        
    Returns:
        bool: True if Yes, False if No
    """
    if not KODI_MODE:
        return False
    
    return xbmcgui.Dialog().yesno(heading, message)

