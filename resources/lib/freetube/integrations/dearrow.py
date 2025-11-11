# -*- coding: utf-8 -*-
"""
    DeArrow Integration
    
    Replace clickbait titles and thumbnails with community submissions
    Based on FreeTube's DeArrow implementation
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

try:
    import xbmc
    KODI_MODE = True
except ImportError:
    KODI_MODE = False


class DeArrowClient:
    """
    DeArrow API client
    Fetch better titles and thumbnails from community
    """
    
    DEFAULT_API_URL = 'https://dearrow-thumb.ajay.app'
    DEFAULT_TITLE_API = 'https://sponsor.ajay.app'
    
    def __init__(self, api_url=None, title_api_url=None):
        """
        Initialize DeArrow client
        
        Args:
            api_url: DeArrow thumbnail API URL (optional)
            title_api_url: DeArrow title API URL (optional)
        """
        self.api_url = (api_url or self.DEFAULT_API_URL).rstrip('/')
        self.title_api_url = (title_api_url or self.DEFAULT_TITLE_API).rstrip('/')
        
        try:
            import requests
            self.session = requests.Session()
        except ImportError:
            raise ImportError('requests module is required')
    
    def get_branding(self, video_id):
        """
        Get DeArrow branding (title and thumbnail) for a video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            dict: Branding data with 'title' and 'thumbnail'
        """
        try:
            # Get title data
            url = f'{self.title_api_url}/api/branding'
            params = {'videoID': video_id}
            
            response = self.session.get(url, params=params, timeout=5)
            
            if response.status_code == 404:
                # No branding found
                return None
            
            response.raise_for_status()
            data = response.json()
            
            result = {}
            
            # Extract title
            titles = data.get('titles', [])
            if titles:
                # Use first title (highest voted)
                title_data = titles[0]
                result['title'] = title_data.get('title')
                result['original_title'] = title_data.get('original', False)
            
            # Extract thumbnail
            thumbnails = data.get('thumbnails', [])
            if thumbnails:
                # Use first thumbnail (highest voted)
                thumb_data = thumbnails[0]
                if thumb_data.get('timestamp') is not None:
                    # Generate thumbnail URL from timestamp
                    timestamp = thumb_data['timestamp']
                    result['thumbnail'] = f'{self.api_url}/api/v1/getThumbnail?videoID={video_id}&time={timestamp}'
                elif thumb_data.get('original'):
                    # Use original thumbnail
                    result['thumbnail'] = None
            
            return result if result else None
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube DeArrow] Error: {str(e)}', xbmc.LOGERROR)
            return None
    
    def get_thumbnail_url(self, video_id, timestamp=None):
        """
        Get DeArrow thumbnail URL
        
        Args:
            video_id: YouTube video ID
            timestamp: Thumbnail timestamp (optional, will fetch best)
            
        Returns:
            str: Thumbnail URL or None
        """
        if timestamp is not None:
            return f'{self.api_url}/api/v1/getThumbnail?videoID={video_id}&time={timestamp}'
        
        # Fetch best thumbnail
        branding = self.get_branding(video_id)
        return branding.get('thumbnail') if branding else None
    
    def submit_title(self, video_id, title, user_id):
        """
        Submit a new title
        
        Args:
            video_id: YouTube video ID
            title: New title
            user_id: DeArrow user ID
            
        Returns:
            bool: True if submitted successfully
        """
        try:
            url = f'{self.title_api_url}/api/branding'
            data = {
                'videoID': video_id,
                'title': title,
                'userID': user_id,
            }
            
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            return True
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube DeArrow] Submit title error: {str(e)}', xbmc.LOGERROR)
            return False
    
    def submit_thumbnail(self, video_id, timestamp, user_id):
        """
        Submit a new thumbnail
        
        Args:
            video_id: YouTube video ID
            timestamp: Thumbnail timestamp in seconds
            user_id: DeArrow user ID
            
        Returns:
            bool: True if submitted successfully
        """
        try:
            url = f'{self.title_api_url}/api/branding/thumbnail'
            data = {
                'videoID': video_id,
                'timestamp': timestamp,
                'userID': user_id,
            }
            
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            return True
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube DeArrow] Submit thumbnail error: {str(e)}', xbmc.LOGERROR)
            return False

