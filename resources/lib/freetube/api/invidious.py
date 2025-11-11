# -*- coding: utf-8 -*-
"""
    Invidious API Client - Fallback Backend
    
    Uses public Invidious instances as privacy-preserving proxy
    Based on FreeTube's Invidious integration
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import json
import random

try:
    from urllib.parse import urlencode, quote
except ImportError:
    from urllib import urlencode, quote

try:
    import xbmc
    KODI_MODE = True
except ImportError:
    KODI_MODE = False


class InvidiousClient:
    """
    Invidious API client for fallback functionality
    Uses public Invidious instances as alternative to direct YouTube access
    """
    
    # Default public Invidious instances (from FreeTube's list)
    DEFAULT_INSTANCES = [
        'https://inv.nadeko.net',
        'https://invidious.private.coffee',
        'https://yt.artemislena.eu',
        'https://invidious.lunar.icu',
        'https://inv.tux.pizza',
        'https://invidious.perennialte.ch',
        'https://yt.drgnz.club',
        'https://invidious.asir.dev',
        'https://iv.ggtyler.dev',
        'https://invidious.io.lol',
    ]
    
    def __init__(self, instance_url=None, random_instance=True):
        """
        Initialize Invidious client
        
        Args:
            instance_url: Specific Invidious instance URL (optional)
            random_instance: Use random instance from list if no URL provided
        """
        if instance_url:
            self.instance_url = instance_url.rstrip('/')
        elif random_instance:
            self.instance_url = random.choice(self.DEFAULT_INSTANCES)
        else:
            self.instance_url = self.DEFAULT_INSTANCES[0]
        
        # Request session
        try:
            import requests
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            })
        except ImportError:
            raise ImportError('requests module is required')
    
    def _call_api(self, endpoint, params=None):
        """
        Make API call to Invidious instance
        
        Args:
            endpoint: API endpoint (e.g., 'videos/{id}', 'search')
            params: URL parameters
            
        Returns:
            dict: API response
        """
        url = f'{self.instance_url}/api/v1/{endpoint}'
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            if KODI_MODE:
                xbmc.log(f'[FreeTube] Invidious API error: {str(e)}', xbmc.LOGERROR)
            raise
    
    def get_video_info(self, video_id):
        """
        Get video information from Invidious
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            dict: Video information
        """
        response = self._call_api(f'videos/{video_id}')
        return self._parse_video_info(response)
    
    def _parse_video_info(self, data):
        """Parse Invidious video info to standard format"""
        info = {
            'video_id': data.get('videoId'),
            'title': data.get('title'),
            'author': data.get('author'),
            'channel_id': data.get('authorId'),
            'length_seconds': data.get('lengthSeconds', 0),
            'is_live': data.get('liveNow', False),
            'short_description': data.get('description', ''),
            'view_count': data.get('viewCount', 0),
            'published': data.get('published', 0),
            'thumbnails': data.get('videoThumbnails', []),
        }
        
        # Parse formats
        formats = []
        adaptive_formats = []
        
        for fmt in data.get('formatStreams', []):
            formats.append({
                'itag': fmt.get('itag'),
                'url': self._get_proxied_url(fmt.get('url')),
                'mime_type': f"{fmt.get('type')}/{fmt.get('container')}",
                'quality': fmt.get('quality'),
                'quality_label': fmt.get('qualityLabel'),
                'fps': fmt.get('fps'),
                'bitrate': fmt.get('bitrate'),
                'width': fmt.get('size', '').split('x')[0] if 'x' in fmt.get('size', '') else None,
                'height': fmt.get('size', '').split('x')[1] if 'x' in fmt.get('size', '') else None,
            })
        
        for fmt in data.get('adaptiveFormats', []):
            adaptive_formats.append({
                'itag': fmt.get('itag'),
                'url': self._get_proxied_url(fmt.get('url')),
                'mime_type': f"{fmt.get('type')}/{fmt.get('container')}",
                'quality': fmt.get('quality'),
                'quality_label': fmt.get('qualityLabel'),
                'fps': fmt.get('fps'),
                'bitrate': fmt.get('bitrate'),
                'audio_quality': fmt.get('audioQuality'),
                'audio_sample_rate': fmt.get('audioSampleRate'),
                'width': fmt.get('size', '').split('x')[0] if 'x' in fmt.get('size', '') else None,
                'height': fmt.get('size', '').split('x')[1] if 'x' in fmt.get('size', '') else None,
            })
        
        info['formats'] = formats
        info['adaptive_formats'] = adaptive_formats
        
        # HLS manifest for live streams
        if data.get('hlsUrl'):
            info['hls_manifest_url'] = self._get_proxied_url(data['hlsUrl'])
        
        # DASH manifest
        if data.get('dashUrl'):
            info['dash_manifest_url'] = self._get_proxied_url(data['dashUrl'])
        
        return info
    
    def _get_proxied_url(self, url):
        """
        Get proxied URL through Invidious
        
        Args:
            url: Original URL
            
        Returns:
            str: Proxied URL
        """
        if not url:
            return url
        
        # If URL is already proxied, return as is
        if url.startswith(self.instance_url):
            return url
        
        # Proxy through Invidious
        from urllib.parse import urlparse
        parsed = urlparse(url)
        
        # Add host parameter for Invidious proxy
        if 'googlevideo.com' in parsed.netloc:
            # YouTube video servers need special handling
            return url.replace(parsed.scheme + '://' + parsed.netloc, self.instance_url)
        
        return url
    
    def search(self, query, page=1, sort_by='relevance', date='', duration='', type='all'):
        """
        Search on Invidious
        
        Args:
            query: Search query
            page: Page number (1-indexed)
            sort_by: 'relevance', 'rating', 'upload_date', 'view_count'
            date: '', 'hour', 'today', 'week', 'month', 'year'
            duration: '', 'short', 'medium', 'long'
            type: 'all', 'video', 'channel', 'playlist'
            
        Returns:
            dict: Search results
        """
        params = {
            'q': query,
            'page': page,
            'sort_by': sort_by,
        }
        
        if date:
            params['date'] = date
        if duration:
            params['duration'] = duration
        if type != 'all':
            params['type'] = type
        
        response = self._call_api('search', params=params)
        return self._parse_search_results(response)
    
    def _parse_search_results(self, data):
        """Parse Invidious search results"""
        results = {
            'items': [],
            'continuation': None,
        }
        
        for item in data:
            item_type = item.get('type')
            
            if item_type == 'video':
                results['items'].append({
                    'type': 'video',
                    'video_id': item.get('videoId'),
                    'title': item.get('title'),
                    'author': item.get('author'),
                    'channel_id': item.get('authorId'),
                    'duration': item.get('lengthSeconds'),
                    'view_count': item.get('viewCount'),
                    'published': item.get('publishedText'),
                    'thumbnails': item.get('videoThumbnails', []),
                    'live': item.get('liveNow', False),
                })
            
            elif item_type == 'channel':
                results['items'].append({
                    'type': 'channel',
                    'channel_id': item.get('authorId'),
                    'title': item.get('author'),
                    'description': item.get('description'),
                    'subscriber_count': item.get('subCount'),
                    'thumbnails': item.get('authorThumbnails', []),
                })
            
            elif item_type == 'playlist':
                results['items'].append({
                    'type': 'playlist',
                    'playlist_id': item.get('playlistId'),
                    'title': item.get('title'),
                    'video_count': item.get('videoCount'),
                    'author': item.get('author'),
                    'channel_id': item.get('authorId'),
                    'thumbnails': item.get('videos', [{}])[0].get('videoThumbnails', []) if item.get('videos') else [],
                })
        
        return results
    
    def get_channel_info(self, channel_id):
        """
        Get channel information
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            dict: Channel information
        """
        response = self._call_api(f'channels/{channel_id}')
        
        return {
            'channel_id': response.get('authorId'),
            'title': response.get('author'),
            'description': response.get('description'),
            'subscriber_count': response.get('subCount'),
            'total_views': response.get('totalViews'),
            'joined': response.get('joined'),
            'thumbnails': response.get('authorThumbnails', []),
            'banner': response.get('authorBanners', []),
            'tabs': response.get('tabs', []),
        }
    
    def get_channel_videos(self, channel_id, sort_by='newest', continuation=None):
        """
        Get channel videos
        
        Args:
            channel_id: YouTube channel ID
            sort_by: 'newest', 'oldest', 'popular'
            continuation: Continuation token for pagination
            
        Returns:
            dict: Channel videos
        """
        params = {'sort_by': sort_by}
        
        if continuation:
            params['continuation'] = continuation
        
        response = self._call_api(f'channels/{channel_id}/videos', params=params)
        
        results = {
            'items': [],
            'continuation': response.get('continuation'),
        }
        
        for video in response.get('videos', []):
            results['items'].append({
                'type': 'video',
                'video_id': video.get('videoId'),
                'title': video.get('title'),
                'duration': video.get('lengthSeconds'),
                'view_count': video.get('viewCount'),
                'published': video.get('publishedText'),
                'thumbnails': video.get('videoThumbnails', []),
                'live': video.get('liveNow', False),
            })
        
        return results
    
    def get_playlist(self, playlist_id, page=1):
        """
        Get playlist videos
        
        Args:
            playlist_id: YouTube playlist ID
            page: Page number
            
        Returns:
            dict: Playlist videos
        """
        params = {'page': page}
        response = self._call_api(f'playlists/{playlist_id}', params=params)
        
        results = {
            'title': response.get('title'),
            'author': response.get('author'),
            'channel_id': response.get('authorId'),
            'video_count': response.get('videoCount'),
            'items': [],
        }
        
        for video in response.get('videos', []):
            results['items'].append({
                'type': 'video',
                'video_id': video.get('videoId'),
                'title': video.get('title'),
                'duration': video.get('lengthSeconds'),
                'thumbnails': video.get('videoThumbnails', []),
            })
        
        return results
    
    def get_trending(self, type='default', region='US'):
        """
        Get trending videos
        
        Args:
            type: 'default', 'music', 'gaming', 'movies'
            region: Region code (e.g., 'US', 'RU')
            
        Returns:
            dict: Trending videos
        """
        params = {}
        
        if type != 'default':
            params['type'] = type
        if region:
            params['region'] = region
        
        response = self._call_api('trending', params=params)
        
        results = {'items': []}
        
        for video in response:
            results['items'].append({
                'type': 'video',
                'video_id': video.get('videoId'),
                'title': video.get('title'),
                'author': video.get('author'),
                'channel_id': video.get('authorId'),
                'duration': video.get('lengthSeconds'),
                'view_count': video.get('viewCount'),
                'published': video.get('publishedText'),
                'thumbnails': video.get('videoThumbnails', []),
            })
        
        return results
    
    def get_search_suggestions(self, query):
        """
        Get search suggestions
        
        Args:
            query: Partial search query
            
        Returns:
            list: List of suggestions
        """
        try:
            params = {'q': query}
            response = self._call_api('search/suggestions', params=params)
            return response.get('suggestions', [])
        except Exception:
            return []
    
    def test_instance(self):
        """
        Test if Invidious instance is working
        
        Returns:
            bool: True if instance is working
        """
        try:
            response = self._call_api('stats')
            return 'version' in response
        except Exception:
            return False
    
    @classmethod
    def find_working_instance(cls, timeout=5):
        """
        Find a working Invidious instance
        
        Args:
            timeout: Timeout for each instance test
            
        Returns:
            InvidiousClient or None: Working client or None
        """
        import requests
        
        # Shuffle instances for load balancing
        instances = cls.DEFAULT_INSTANCES.copy()
        random.shuffle(instances)
        
        for instance_url in instances:
            try:
                # Quick test
                response = requests.get(
                    f'{instance_url}/api/v1/stats',
                    timeout=timeout
                )
                if response.status_code == 200:
                    if KODI_MODE:
                        xbmc.log(f'[FreeTube] Found working Invidious instance: {instance_url}', xbmc.LOGINFO)
                    return cls(instance_url=instance_url)
            except Exception:
                continue
        
        return None

