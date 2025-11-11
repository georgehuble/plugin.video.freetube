# -*- coding: utf-8 -*-
"""
    FreeTube Provider - Main Plugin Logic
    
    Handles all plugin functionality without Google authentication
    Based on FreeTube application architecture
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import sys

try:
    from urllib.parse import urlencode, parse_qs
except ImportError:
    from urllib import urlencode
    from urlparse import parse_qs

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

from .api import InnertubeClient, InvidiousClient
from .storage import Database, SubscriptionsManager, HistoryManager, ProfilesManager, PlaylistsManager


class FreeTubeProvider:
    """Main provider for FreeTube Kodi plugin"""
    
    def __init__(self, addon_handle, addon_url):
        """
        Initialize provider
        
        Args:
            addon_handle: Kodi addon handle
            addon_url: Kodi addon URL
        """
        self.handle = addon_handle
        self.url = addon_url
        self.addon = xbmcaddon.Addon()
        self.addon_id = self.addon.getAddonInfo('id')
        
        # Initialize database and managers
        self.db = Database()
        self.subscriptions = SubscriptionsManager(self.db)
        self.history = HistoryManager(self.db)
        self.profiles = ProfilesManager(self.db)
        self.playlists = PlaylistsManager(self.db)
        
        # Get current profile
        self.current_profile = self.profiles.get_default_profile()
        if not self.current_profile:
            # Create default profile if none exists
            profile_id = self.profiles.create_profile('Default Profile', is_default=True)
            self.current_profile = self.profiles.get_profile(profile_id)
        
        # Initialize API clients
        self._init_api_clients()
    
    def _init_api_clients(self):
        """Initialize API clients based on settings"""
        # Get API backend preference
        api_backend = self.addon.getSetting('api_backend') or 'local'
        enable_fallback = self.addon.getSetting('enable_api_fallback') == 'true'
        
        # Language and region
        language = self.addon.getSetting('content_language') or 'en'
        region = self.addon.getSetting('content_region') or 'US'
        
        try:
            if api_backend == 'invidious':
                # Use Invidious as primary
                instance_url = self.addon.getSetting('invidious_instance')
                if instance_url:
                    self.api_client = InvidiousClient(instance_url=instance_url)
                else:
                    self.api_client = InvidiousClient(random_instance=True)
                
                # Innertube as fallback
                if enable_fallback:
                    self.fallback_client = InnertubeClient('web', language, region)
            else:
                # Use Local Innertube as primary
                client_type = self.addon.getSetting('innertube_client') or 'web'
                self.api_client = InnertubeClient(client_type, language, region)
                
                # Invidious as fallback
                if enable_fallback:
                    self.fallback_client = InvidiousClient(random_instance=True)
        
        except Exception as e:
            xbmc.log(f'[FreeTube] API client init error: {str(e)}', xbmc.LOGERROR)
            # Fallback to basic Innertube client
            self.api_client = InnertubeClient('web', language, region)
            self.fallback_client = None
    
    def build_url(self, params):
        """
        Build plugin URL
        
        Args:
            params: URL parameters dict
            
        Returns:
            str: Plugin URL
        """
        return f'{self.url}?{urlencode(params)}'
    
    def add_directory_item(self, title, url_params, icon='DefaultFolder.png', fanart=None,
                          context_menu=None, is_folder=True, info_labels=None):
        """
        Add directory item to Kodi
        
        Args:
            title: Item title
            url_params: URL parameters dict
            icon: Icon path
            fanart: Fanart path
            context_menu: Context menu items
            is_folder: Is this a folder
            info_labels: Video info labels
        """
        url = self.build_url(url_params)
        list_item = xbmcgui.ListItem(label=title)
        
        # Set info
        if info_labels:
            list_item.setInfo('video', info_labels)
        
        # Set art
        list_item.setArt({
            'icon': icon,
            'thumb': icon,
            'fanart': fanart or self.addon.getAddonInfo('fanart')
        })
        
        # Set context menu
        if context_menu:
            list_item.addContextMenuItems(context_menu)
        
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, is_folder)
    
    def add_video_item(self, video):
        """
        Add video item to Kodi
        
        Args:
            video: Video data dict
        """
        title = video.get('title', 'Unknown')
        video_id = video.get('video_id')
        
        # Build URL
        url = self.build_url({'action': 'play', 'video_id': video_id})
        
        # Create list item
        list_item = xbmcgui.ListItem(label=title)
        list_item.setProperty('IsPlayable', 'true')
        
        # Set video info
        info_labels = {
            'title': title,
            'plot': video.get('short_description', ''),
            'duration': video.get('length_seconds', 0),
            'aired': video.get('published', ''),
        }
        
        if video.get('author'):
            info_labels['studio'] = video['author']
        
        if video.get('view_count'):
            info_labels['playcount'] = video['view_count']
        
        list_item.setInfo('video', info_labels)
        
        # Set thumbnail
        thumbnails = video.get('thumbnails', [])
        if thumbnails:
            thumb = thumbnails[-1].get('url') if isinstance(thumbnails[-1], dict) else thumbnails[-1]
            list_item.setArt({'thumb': thumb, 'icon': thumb})
        
        # Context menu
        context_menu = [
            ('Queue', f'Action(Queue)'),
            ('Add to Playlist', f'RunPlugin({self.build_url({"action": "add_to_playlist", "video_id": video_id})})'),
        ]
        
        # Subscribe/Unsubscribe option
        if video.get('channel_id'):
            if self.subscriptions.is_subscribed(self.current_profile['profile_id'], video['channel_id']):
                context_menu.append((
                    'Unsubscribe',
                    f'RunPlugin({self.build_url({"action": "unsubscribe", "channel_id": video["channel_id"]})})'
                ))
            else:
                context_menu.append((
                    'Subscribe',
                    f'RunPlugin({self.build_url({"action": "subscribe", "channel_id": video["channel_id"], "channel_name": video.get("author", "")})})'
                ))
        
        list_item.addContextMenuItems(context_menu)
        
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, False)
    
    def show_main_menu(self):
        """Show main menu"""
        xbmcplugin.setPluginCategory(self.handle, 'FreeTube')
        xbmcplugin.setContent(self.handle, 'videos')
        
        # Subscriptions
        self.add_directory_item(
            'Subscriptions',
            {'action': 'subscriptions'},
            icon='DefaultUser.png'
        )
        
        # Trending
        self.add_directory_item(
            'Trending',
            {'action': 'trending'},
            icon='DefaultTVShows.png'
        )
        
        # Search
        self.add_directory_item(
            'Search',
            {'action': 'search'},
            icon='DefaultAddonsSearch.png'
        )
        
        # Watch History
        self.add_directory_item(
            'Watch History',
            {'action': 'history'},
            icon='DefaultRecentlyAddedEpisodes.png'
        )
        
        # Playlists
        self.add_directory_item(
            'Playlists',
            {'action': 'playlists'},
            icon='DefaultPlaylist.png'
        )
        
        # Profiles
        profile_name = self.current_profile['name']
        self.add_directory_item(
            f'Profiles ({profile_name})',
            {'action': 'profiles'},
            icon='DefaultActor.png'
        )
        
        # Settings
        self.add_directory_item(
            'Settings',
            {'action': 'settings'},
            icon='DefaultAddonService.png'
        )
        
        xbmcplugin.endOfDirectory(self.handle)
    
    def show_subscriptions(self):
        """Show subscriptions feed"""
        xbmcplugin.setPluginCategory(self.handle, 'Subscriptions')
        xbmcplugin.setContent(self.handle, 'videos')
        
        # Get subscriptions
        profile_id = self.current_profile['profile_id']
        subs = self.subscriptions.get_subscriptions(profile_id)
        
        if not subs:
            xbmcgui.Dialog().notification(
                'FreeTube',
                'No subscriptions yet. Subscribe to channels!',
                xbmcgui.NOTIFICATION_INFO
            )
            xbmcplugin.endOfDirectory(self.handle)
            return
        
        # Add "All Subscriptions" view
        self.add_directory_item(
            'All Subscriptions Feed',
            {'action': 'subscriptions_feed'},
            icon='DefaultTVShows.png'
        )
        
        # Show channels
        for sub in subs:
            context_menu = [
                ('Unsubscribe', f'RunPlugin({self.build_url({"action": "unsubscribe", "channel_id": sub["channel_id"]})})')
            ]
            
            self.add_directory_item(
                sub['channel_name'],
                {'action': 'channel', 'channel_id': sub['channel_id']},
                icon=sub.get('channel_thumbnail', 'DefaultActor.png'),
                context_menu=context_menu
            )
        
        xbmcplugin.endOfDirectory(self.handle)
    
    def show_subscriptions_feed(self):
        """Show videos from all subscribed channels"""
        xbmcplugin.setPluginCategory(self.handle, 'Subscriptions Feed')
        xbmcplugin.setContent(self.handle, 'videos')
        
        profile_id = self.current_profile['profile_id']
        subs = self.subscriptions.get_subscriptions(profile_id)
        
        if not subs:
            xbmcplugin.endOfDirectory(self.handle)
            return
        
        # Get videos from each channel (limit to prevent slowdown)
        all_videos = []
        max_channels = 20  # Limit to prevent long load times
        
        progress = xbmcgui.DialogProgress()
        progress.create('FreeTube', 'Loading subscription feed...')
        
        for idx, sub in enumerate(subs[:max_channels]):
            if progress.iscanceled():
                break
            
            progress.update(int((idx / len(subs[:max_channels])) * 100), f'Loading {sub["channel_name"]}...')
            
            try:
                result = self.api_client.get_channel_videos(sub['channel_id'])
                videos = result.get('items', [])[:5]  # Latest 5 videos per channel
                all_videos.extend(videos)
            except Exception:
                continue
        
        progress.close()
        
        # Sort by published date (if available)
        # For now, just show all videos
        for video in all_videos[:50]:  # Limit to 50 videos
            self.add_video_item(video)
        
        xbmcplugin.endOfDirectory(self.handle)
    
    def show_trending(self):
        """Show trending videos"""
        xbmcplugin.setPluginCategory(self.handle, 'Trending')
        xbmcplugin.setContent(self.handle, 'videos')
        
        try:
            result = self.api_client.get_trending()
            videos = result.get('items', [])
            
            for video in videos:
                self.add_video_item(video)
        
        except Exception as e:
            xbmc.log(f'[FreeTube] Trending error: {str(e)}', xbmc.LOGERROR)
            xbmcgui.Dialog().notification('FreeTube', 'Error loading trending', xbmcgui.NOTIFICATION_ERROR)
        
        xbmcplugin.endOfDirectory(self.handle)
    
    def search_videos(self, query=None):
        """Search for videos"""
        if not query:
            # Show search dialog
            keyboard = xbmcgui.Dialog().input('Search YouTube', type=xbmcgui.INPUT_ALPHANUM)
            if not keyboard:
                xbmcplugin.endOfDirectory(self.handle)
                return
            query = keyboard
        
        xbmcplugin.setPluginCategory(self.handle, f'Search: {query}')
        xbmcplugin.setContent(self.handle, 'videos')
        
        try:
            result = self.api_client.search(query)
            items = result.get('items', [])
            
            for item in items:
                if item.get('type') == 'video':
                    self.add_video_item(item)
                elif item.get('type') == 'channel':
                    self.add_directory_item(
                        item['title'],
                        {'action': 'channel', 'channel_id': item['channel_id']},
                        icon=item.get('thumbnails', [{}])[0].get('url') if item.get('thumbnails') else 'DefaultActor.png'
                    )
        
        except Exception as e:
            xbmc.log(f'[FreeTube] Search error: {str(e)}', xbmc.LOGERROR)
            xbmcgui.Dialog().notification('FreeTube', 'Search error', xbmcgui.NOTIFICATION_ERROR)
        
        xbmcplugin.endOfDirectory(self.handle)
    
    def play_video(self, video_id):
        """
        Play video
        
        Args:
            video_id: YouTube video ID
        """
        try:
            # Get video info
            video_info = self.api_client.get_video_info(video_id)
            
            # Choose format (prefer adaptive formats with highest quality)
            formats = video_info.get('adaptive_formats', []) + video_info.get('formats', [])
            
            if not formats:
                xbmcgui.Dialog().notification('FreeTube', 'No playable streams found', xbmcgui.NOTIFICATION_ERROR)
                return
            
            # Sort by quality (height) and select best
            video_formats = [f for f in formats if f.get('height')]
            if video_formats:
                video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
                best_format = video_formats[0]
                stream_url = best_format.get('url')
            else:
                # Fallback to first available format
                stream_url = formats[0].get('url')
            
            if not stream_url:
                xbmcgui.Dialog().notification('FreeTube', 'No playable URL found', xbmcgui.NOTIFICATION_ERROR)
                return
            
            # Create playable item
            play_item = xbmcgui.ListItem(path=stream_url)
            play_item.setInfo('video', {
                'title': video_info.get('title'),
                'duration': video_info.get('length_seconds', 0),
                'plot': video_info.get('short_description', '')
            })
            
            # Set resolved URL
            xbmcplugin.setResolvedUrl(self.handle, True, play_item)
            
            # Add to history
            if self.addon.getSetting('enable_watch_history') == 'true':
                self.history.add_to_history(
                    self.current_profile['profile_id'],
                    video_id,
                    video_info.get('title', ''),
                    video_info.get('author'),
                    video_info.get('channel_id'),
                    video_info.get('length_seconds'),
                    video_info.get('thumbnails', [{}])[0].get('url') if video_info.get('thumbnails') else None
                )
        
        except Exception as e:
            xbmc.log(f'[FreeTube] Playback error: {str(e)}', xbmc.LOGERROR)
            xbmcgui.Dialog().notification('FreeTube', 'Playback error', xbmcgui.NOTIFICATION_ERROR)
            xbmcplugin.setResolvedUrl(self.handle, False, xbmcgui.ListItem())
    
    def route(self, params):
        """
        Route request to appropriate handler
        
        Args:
            params: URL parameters dict
        """
        action = params.get('action', ['main_menu'])[0]
        
        if action == 'main_menu':
            self.show_main_menu()
        elif action == 'subscriptions':
            self.show_subscriptions()
        elif action == 'subscriptions_feed':
            self.show_subscriptions_feed()
        elif action == 'trending':
            self.show_trending()
        elif action == 'search':
            query = params.get('query', [None])[0]
            self.search_videos(query)
        elif action == 'play':
            video_id = params.get('video_id', [None])[0]
            if video_id:
                self.play_video(video_id)
        else:
            self.show_main_menu()

