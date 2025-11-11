# -*- coding: utf-8 -*-
"""
    SponsorBlock Integration
    
    Skip sponsors, intros, outros, and other video segments
    Based on FreeTube's SponsorBlock implementation
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import hashlib

try:
    import xbmc
    KODI_MODE = True
except ImportError:
    KODI_MODE = False


class SponsorBlockClient:
    """
    SponsorBlock API client
    Fetch and manage skip segments for videos
    """
    
    DEFAULT_API_URL = 'https://sponsor.ajay.app'
    
    # Segment categories
    CATEGORIES = {
        'sponsor': 'Sponsor',
        'intro': 'Intermission/Intro Animation',
        'outro': 'Endcards/Credits',
        'selfpromo': 'Self Promotion',
        'interaction': 'Interaction Reminder',
        'preview': 'Preview/Recap',
        'music_offtopic': 'Non-Music Section',
        'filler': 'Filler Tangent',
    }
    
    def __init__(self, api_url=None):
        """
        Initialize SponsorBlock client
        
        Args:
            api_url: SponsorBlock API URL (optional)
        """
        self.api_url = (api_url or self.DEFAULT_API_URL).rstrip('/')
        
        try:
            import requests
            self.session = requests.Session()
        except ImportError:
            raise ImportError('requests module is required')
    
    def get_segments(self, video_id, categories=None):
        """
        Get skip segments for a video
        
        Args:
            video_id: YouTube video ID
            categories: List of categories to fetch (None = all)
            
        Returns:
            list: List of segments
        """
        try:
            # Build category filter
            if categories:
                category_param = '["' + '","'.join(categories) + '"]'
            else:
                category_param = '["sponsor","intro","outro","selfpromo","interaction","preview"]'
            
            # Make API request
            url = f'{self.api_url}/api/skipSegments'
            params = {
                'videoID': video_id,
                'categories': category_param,
            }
            
            response = self.session.get(url, params=params, timeout=5)
            
            if response.status_code == 404:
                # No segments found
                return []
            
            response.raise_for_status()
            data = response.json()
            
            # Parse segments
            segments = []
            for item in data:
                segment = item.get('segment', [])
                if len(segment) == 2:
                    segments.append({
                        'start': segment[0],
                        'end': segment[1],
                        'category': item.get('category'),
                        'action_type': item.get('actionType', 'skip'),
                        'uuid': item.get('UUID'),
                    })
            
            return segments
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube SponsorBlock] Error: {str(e)}', xbmc.LOGERROR)
            return []
    
    def should_skip_segment(self, current_time, segments):
        """
        Check if current time is in a skip segment
        
        Args:
            current_time: Current playback time in seconds
            segments: List of segments
            
        Returns:
            dict or None: Segment to skip or None
        """
        for segment in segments:
            if segment['start'] <= current_time < segment['end']:
                return segment
        return None
    
    def submit_segment(self, video_id, start_time, end_time, category, user_id=None):
        """
        Submit a new segment (requires user ID)
        
        Args:
            video_id: YouTube video ID
            start_time: Segment start time
            end_time: Segment end time
            category: Segment category
            user_id: SponsorBlock user ID
            
        Returns:
            bool: True if submitted successfully
        """
        if not user_id:
            return False
        
        try:
            url = f'{self.api_url}/api/skipSegments'
            data = {
                'videoID': video_id,
                'startTime': start_time,
                'endTime': end_time,
                'category': category,
                'userID': user_id,
            }
            
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            return True
        
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube SponsorBlock] Submit error: {str(e)}', xbmc.LOGERROR)
            return False
    
    @staticmethod
    def generate_user_id():
        """
        Generate random user ID for SponsorBlock submissions
        
        Returns:
            str: User ID
        """
        import uuid
        import hashlib
        
        # Generate UUID and hash it
        user_uuid = str(uuid.uuid4())
        user_id = hashlib.sha256(user_uuid.encode()).hexdigest()
        
        return user_id

