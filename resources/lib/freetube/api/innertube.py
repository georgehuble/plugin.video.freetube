# -*- coding: utf-8 -*-
"""
    Innertube API Client - No Authentication Required
    
    Based on FreeTube's approach using youtubei.js methodology
    Accesses YouTube's internal InnerTube API without Google account
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import json
import time
import random
import string
from hashlib import sha1

try:
    from urllib.parse import urlencode, parse_qs, urlparse
except ImportError:
    from urllib import urlencode
    from urlparse import parse_qs, urlparse

try:
    import xbmc
    import xbmcaddon
    KODI_MODE = True
except ImportError:
    KODI_MODE = False


class InnertubeClient:
    """
    YouTube Innertube API client without authentication
    Mimics FreeTube's approach for privacy-first YouTube access
    """
    
    # API endpoints
    BASE_URL = 'https://www.youtube.com'
    API_BASE = 'https://www.youtube.com/youtubei/v1'
    
    # API Keys (from YouTube's web client - public)
    API_KEYS = {
        'web': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'mweb': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'android': 'AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w',
        'ios': 'AIzaSyB-63vPrdThhKuerbB2N_l7Kwwcxj6yUAc',
    }
    
    # Client information (mimics real browser)
    CLIENTS = {
        'web': {
            'clientName': 'WEB',
            'clientVersion': '2.20241111.01.00',
            'platform': 'DESKTOP',
            'osName': 'Windows',
            'osVersion': '10.0',
            'browserName': 'Chrome',
            'browserVersion': '131.0.0.0',
        },
        'mweb': {
            'clientName': 'MWEB',
            'clientVersion': '2.20241111.08.00',
            'platform': 'MOBILE',
            'osName': 'Android',
            'osVersion': '14',
        },
        'android': {
            'clientName': 'ANDROID',
            'clientVersion': '19.15.36',
            'androidSdkVersion': 34,
            'platform': 'MOBILE',
            'osName': 'Android',
            'osVersion': '14',
        },
        'ios': {
            'clientName': 'IOS',
            'clientVersion': '19.15.1',
            'platform': 'MOBILE',
            'osName': 'iOS',
            'osVersion': '17.5.1',
            'deviceMake': 'Apple',
            'deviceModel': 'iPhone15,2',
        },
    }
    
    def __init__(self, client_type='web', language='en', region='US', use_https=True):
        """
        Initialize Innertube client
        
        Args:
            client_type: 'web', 'mweb', 'android', or 'ios'
            language: Language code (e.g., 'en', 'ru')
            region: Region code (e.g., 'US', 'RU')
            use_https: Use HTTPS (always True for security)
        """
        self.client_type = client_type
        self.language = language
        self.region = region
        self.use_https = use_https
        
        # Session data
        self.api_key = self.API_KEYS.get(client_type, self.API_KEYS['web'])
        self.context = self._create_context()
        
        # Request session (use requests library)
        try:
            import requests
            self.session = requests.Session()
            self._setup_headers()
        except ImportError:
            raise ImportError('requests module is required')
    
    def _create_context(self):
        """
        Create API context (no authentication needed)
        This mimics FreeTube's approach: create fresh session without login
        """
        client_info = self.CLIENTS.get(self.client_type, self.CLIENTS['web']).copy()
        
        # Generate visitor data (anonymous identifier)
        visitor_data = self._generate_visitor_data()
        
        context = {
            'client': client_info,
            'request': {
                'useSsl': self.use_https,
                'internalExperimentFlags': [],
            },
            'user': {
                'lockedSafetyMode': False,
                # No authentication - key difference from official clients
            },
        }
        
        # Add language/region
        if self.language:
            context['client']['hl'] = self.language
        if self.region:
            context['client']['gl'] = self.region
        
        # Add visitor data for tracking prevention
        context['client']['visitorData'] = visitor_data
        
        return context
    
    def _generate_visitor_data(self):
        """
        Generate anonymous visitor data
        This is used instead of authentication
        """
        # Simple random string generation (11 chars base64-like)
        chars = string.ascii_letters + string.digits + '-_'
        return ''.join(random.choice(chars) for _ in range(11))
    
    def _setup_headers(self):
        """
        Setup HTTP headers to mimic FreeTube's requests
        Key headers for bypassing authentication checks
        """
        # User agent based on client type
        user_agents = {
            'web': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'mweb': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.39 Mobile Safari/537.36',
            'android': 'com.google.android.youtube/19.15.36 (Linux; U; Android 14) gzip',
            'ios': 'com.google.ios.youtube/19.15.1 (iPhone15,2; U; CPU iOS 17_5_1 like Mac OS X)',
        }
        
        headers = {
            'User-Agent': user_agents.get(self.client_type, user_agents['web']),
            'Accept-Language': f'{self.language},en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': self.BASE_URL,
            'Referer': self.BASE_URL + '/',
        }
        
        # Critical headers for non-authenticated access (from FreeTube)
        if self.client_type in ['web', 'mweb']:
            headers.update({
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'same-origin',
                'X-Youtube-Bootstrap-Logged-In': 'false',  # KEY: Tell YouTube we're not logged in
                'X-Youtube-Client-Name': '1' if self.client_type == 'web' else '2',
                'X-Youtube-Client-Version': self.CLIENTS[self.client_type]['clientVersion'],
            })
        
        self.session.headers.update(headers)
    
    def _call_api(self, endpoint, data=None, params=None):
        """
        Make API call to Innertube endpoint
        
        Args:
            endpoint: API endpoint (e.g., 'player', 'browse', 'search')
            data: POST data dictionary
            params: URL parameters
            
        Returns:
            dict: API response
        """
        url = f'{self.API_BASE}/{endpoint}'
        
        # Add API key to URL
        url_params = {'key': self.api_key}
        if params:
            url_params.update(params)
        
        # Prepare request data
        if data is None:
            data = {}
        
        # Always include context
        data['context'] = self.context
        
        try:
            # Make POST request (Innertube API uses POST for everything)
            response = self.session.post(
                url,
                params=url_params,
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Innertube API error: {str(e)}', xbmc.LOGERROR)
            raise
    
    def get_video_info(self, video_id):
        """
        Get video information without authentication
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            dict: Video information including streams
        """
        data = {
            'videoId': video_id,
            'contentCheckOk': True,
            'racyCheckOk': True,
        }
        
        # Call player endpoint
        response = self._call_api('player', data=data)
        
        return self._parse_video_info(response)
    
    def _parse_video_info(self, response):
        """
        Parse video info response
        
        Returns:
            dict: Parsed video information
        """
        video_details = response.get('videoDetails', {})
        streaming_data = response.get('streamingData', {})
        
        # Parse basic info
        info = {
            'video_id': video_details.get('videoId'),
            'title': video_details.get('title'),
            'author': video_details.get('author'),
            'channel_id': video_details.get('channelId'),
            'length_seconds': int(video_details.get('lengthSeconds', 0)),
            'is_live': video_details.get('isLiveContent', False),
            'short_description': video_details.get('shortDescription', ''),
            'view_count': int(video_details.get('viewCount', 0)),
            'thumbnails': video_details.get('thumbnail', {}).get('thumbnails', []),
        }
        
        # Parse streaming data
        formats = []
        adaptive_formats = []
        
        # Regular formats (video + audio combined)
        for fmt in streaming_data.get('formats', []):
            formats.append(self._parse_format(fmt))
        
        # Adaptive formats (separate video/audio)
        for fmt in streaming_data.get('adaptiveFormats', []):
            adaptive_formats.append(self._parse_format(fmt))
        
        info['formats'] = formats
        info['adaptive_formats'] = adaptive_formats
        
        # HLS manifest (for live streams)
        if 'hlsManifestUrl' in streaming_data:
            info['hls_manifest_url'] = streaming_data['hlsManifestUrl']
        
        # DASH manifest
        if 'dashManifestUrl' in streaming_data:
            info['dash_manifest_url'] = streaming_data['dashManifestUrl']
        
        return info
    
    def _parse_format(self, fmt):
        """Parse a single format object"""
        return {
            'itag': fmt.get('itag'),
            'url': fmt.get('url'),
            'mime_type': fmt.get('mimeType'),
            'bitrate': fmt.get('bitrate'),
            'width': fmt.get('width'),
            'height': fmt.get('height'),
            'fps': fmt.get('fps'),
            'quality': fmt.get('quality'),
            'quality_label': fmt.get('qualityLabel'),
            'audio_quality': fmt.get('audioQuality'),
            'audio_sample_rate': fmt.get('audioSampleRate'),
            'signature_cipher': fmt.get('signatureCipher'),
        }
    
    def search(self, query, continuation=None):
        """
        Search YouTube without authentication
        
        Args:
            query: Search query string
            continuation: Continuation token for pagination
            
        Returns:
            dict: Search results
        """
        if continuation:
            # Continue previous search
            data = {'continuation': continuation}
            response = self._call_api('search', data=data)
        else:
            # New search
            data = {'query': query}
            response = self._call_api('search', data=data)
        
        return self._parse_search_results(response)
    
    def _parse_search_results(self, response):
        """Parse search results"""
        results = {
            'items': [],
            'continuation': None,
        }
        
        # Extract continuation token
        continuation_items = self._find_in_dict(response, 'continuationCommand')
        if continuation_items:
            results['continuation'] = continuation_items[0].get('token')
        
        # Extract videos
        video_renderers = self._find_in_dict(response, 'videoRenderer')
        for renderer in video_renderers:
            item = self._parse_video_renderer(renderer)
            if item:
                results['items'].append(item)
        
        # Extract channels
        channel_renderers = self._find_in_dict(response, 'channelRenderer')
        for renderer in channel_renderers:
            item = self._parse_channel_renderer(renderer)
            if item:
                results['items'].append(item)
        
        # Extract playlists
        playlist_renderers = self._find_in_dict(response, 'playlistRenderer')
        for renderer in playlist_renderers:
            item = self._parse_playlist_renderer(renderer)
            if item:
                results['items'].append(item)
        
        return results
    
    def _parse_video_renderer(self, renderer):
        """Parse video renderer object"""
        try:
            video_id = renderer.get('videoId')
            if not video_id:
                return None
            
            title_runs = renderer.get('title', {}).get('runs', [])
            title = title_runs[0].get('text') if title_runs else ''
            
            return {
                'type': 'video',
                'video_id': video_id,
                'title': title,
                'author': self._get_text(renderer, 'ownerText'),
                'channel_id': self._get_navigation_endpoint(renderer, 'ownerText', 'browseId'),
                'duration': self._get_text(renderer, 'lengthText'),
                'view_count': self._get_text(renderer, 'viewCountText'),
                'published': self._get_text(renderer, 'publishedTimeText'),
                'thumbnails': renderer.get('thumbnail', {}).get('thumbnails', []),
            }
        except Exception:
            return None
    
    def _parse_channel_renderer(self, renderer):
        """Parse channel renderer object"""
        try:
            return {
                'type': 'channel',
                'channel_id': renderer.get('channelId'),
                'title': self._get_text(renderer, 'title'),
                'description': self._get_text(renderer, 'descriptionSnippet'),
                'subscriber_count': self._get_text(renderer, 'subscriberCountText'),
                'thumbnails': renderer.get('thumbnail', {}).get('thumbnails', []),
            }
        except Exception:
            return None
    
    def _parse_playlist_renderer(self, renderer):
        """Parse playlist renderer object"""
        try:
            return {
                'type': 'playlist',
                'playlist_id': renderer.get('playlistId'),
                'title': self._get_text(renderer, 'title'),
                'video_count': self._get_text(renderer, 'videoCountText'),
                'thumbnails': renderer.get('thumbnails', [{}])[0].get('thumbnails', []),
            }
        except Exception:
            return None
    
    def get_channel_info(self, channel_id):
        """Get channel information"""
        data = {'browseId': channel_id}
        response = self._call_api('browse', data=data)
        return response
    
    def get_channel_videos(self, channel_id, continuation=None):
        """Get channel videos"""
        if continuation:
            data = {'continuation': continuation}
        else:
            # Videos tab params (protobuf encoded)
            data = {
                'browseId': channel_id,
                'params': 'EgZ2aWRlb3PyBgQKAjoA',  # Videos tab
            }
        
        response = self._call_api('browse', data=data)
        return self._parse_search_results(response)
    
    def get_playlist(self, playlist_id, continuation=None):
        """Get playlist videos"""
        if continuation:
            data = {'continuation': continuation}
        else:
            data = {'browseId': f'VL{playlist_id}'}
        
        response = self._call_api('browse', data=data)
        return self._parse_search_results(response)
    
    def get_trending(self):
        """Get trending videos"""
        data = {'browseId': 'FEtrending'}
        response = self._call_api('browse', data=data)
        return self._parse_search_results(response)
    
    def get_search_suggestions(self, query):
        """Get search suggestions"""
        data = {'input': query}
        response = self._call_api('music/get_search_suggestions', data=data)
        
        suggestions = []
        for item in self._find_in_dict(response, 'searchSuggestionRenderer'):
            suggestion = self._get_text(item, 'suggestion')
            if suggestion:
                suggestions.append(suggestion)
        
        return suggestions
    
    # Helper methods
    
    def _find_in_dict(self, data, key):
        """Recursively find all occurrences of a key in nested dict/list"""
        results = []
        
        if isinstance(data, dict):
            if key in data:
                results.append(data[key])
            for value in data.values():
                results.extend(self._find_in_dict(value, key))
        elif isinstance(data, list):
            for item in data:
                results.extend(self._find_in_dict(item, key))
        
        return results
    
    def _get_text(self, data, key):
        """Extract text from renderer object"""
        try:
            text_data = data.get(key, {})
            if 'runs' in text_data:
                return ''.join([run.get('text', '') for run in text_data['runs']])
            elif 'simpleText' in text_data:
                return text_data['simpleText']
            return ''
        except Exception:
            return ''
    
    def _get_navigation_endpoint(self, data, key, endpoint_key):
        """Extract navigation endpoint from renderer"""
        try:
            text_data = data.get(key, {})
            runs = text_data.get('runs', [])
            if runs:
                endpoint = runs[0].get('navigationEndpoint', {})
                browse_endpoint = endpoint.get('browseEndpoint', {})
                return browse_endpoint.get(endpoint_key)
            return None
        except Exception:
            return None

