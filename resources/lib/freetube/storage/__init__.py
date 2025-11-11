# -*- coding: utf-8 -*-
"""
    FreeTube Storage Module
    
    Local database for subscriptions, history, profiles, and playlists
    No cloud sync, no authentication - all data stored locally
"""

from __future__ import absolute_import, division, unicode_literals

from .database import Database
from .subscriptions import SubscriptionsManager
from .history import HistoryManager
from .profiles import ProfilesManager
from .playlists import PlaylistsManager

__all__ = [
    'Database',
    'SubscriptionsManager',
    'HistoryManager',
    'ProfilesManager',
    'PlaylistsManager',
]

