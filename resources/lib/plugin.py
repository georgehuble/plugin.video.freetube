# -*- coding: utf-8 -*-
"""
    FreeTube for Kodi - Main Entry Point
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import sys

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

import xbmc
import xbmcaddon
import xbmcplugin

from freetube.provider import FreeTubeProvider


def main():
    """Main plugin entry point"""
    try:
        # Get addon info
        addon = xbmcaddon.Addon()
        addon_handle = int(sys.argv[1])
        addon_url = sys.argv[0]
        
        # Parse parameters
        params = parse_qs(sys.argv[2][1:]) if len(sys.argv) > 2 else {}
        
        xbmc.log('[FreeTube] Plugin started', xbmc.LOGINFO)
        xbmc.log(f'[FreeTube] Params: {params}', xbmc.LOGDEBUG)
        
        # Initialize provider
        provider = FreeTubeProvider(addon_handle, addon_url)
        
        # Route request
        provider.route(params)
        
    except Exception as e:
        xbmc.log(f'[FreeTube] Fatal error: {str(e)}', xbmc.LOGERROR)
        import traceback
        xbmc.log(f'[FreeTube] Traceback: {traceback.format_exc()}', xbmc.LOGERROR)
        
        # Show error to user
        import xbmcgui
        xbmcgui.Dialog().notification(
            'FreeTube Error',
            str(e),
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )


if __name__ == '__main__':
    main()

