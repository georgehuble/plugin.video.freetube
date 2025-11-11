# -*- coding: utf-8 -*-
"""
    FreeTube for Kodi - Background Service
    
    Handles background tasks:
    - Subscription feed updates
    - Periodic data cleanup
    - API health checks
    
    Copyright (C) 2025 FreeTube Kodi Team
    
    SPDX-License-Identifier: AGPL-3.0-or-later
"""

from __future__ import absolute_import, division, unicode_literals

import time

import xbmc
import xbmcaddon

from freetube.storage import Database
from freetube.api import InnertubeClient, InvidiousClient


class FreeTubeService:
    """Background service for FreeTube"""
    
    def __init__(self):
        """Initialize service"""
        self.addon = xbmcaddon.Addon()
        self.monitor = xbmc.Monitor()
        self.db = Database()
        
        xbmc.log('[FreeTube Service] Started', xbmc.LOGINFO)
    
    def check_api_health(self):
        """Check if API is working, switch to fallback if needed"""
        try:
            api_backend = self.addon.getSetting('api_backend') or 'local'
            
            if api_backend == 'local':
                # Test Innertube API
                client = InnertubeClient('web')
                # Try to get trending as health check
                client.get_trending()
                xbmc.log('[FreeTube Service] Innertube API healthy', xbmc.LOGDEBUG)
            
            elif api_backend == 'invidious':
                # Test Invidious instance
                instance_url = self.addon.getSetting('invidious_instance')
                if instance_url:
                    client = InvidiousClient(instance_url=instance_url)
                    if not client.test_instance():
                        xbmc.log('[FreeTube Service] Invidious instance unhealthy, finding new one', xbmc.LOGWARNING)
                        # Find working instance
                        new_client = InvidiousClient.find_working_instance()
                        if new_client:
                            self.addon.setSetting('invidious_instance', new_client.instance_url)
                            xbmc.log(f'[FreeTube Service] Switched to: {new_client.instance_url}', xbmc.LOGINFO)
        
        except Exception as e:
            xbmc.log(f'[FreeTube Service] API health check error: {str(e)}', xbmc.LOGERROR)
    
    def cleanup_old_data(self):
        """Clean up old data based on settings"""
        try:
            # Check if auto-cleanup is enabled
            enable_cleanup = self.addon.getSetting('enable_auto_cleanup') == 'true'
            if not enable_cleanup:
                return
            
            # Get cleanup settings
            history_days = int(self.addon.getSetting('history_cleanup_days') or '90')
            search_days = int(self.addon.getSetting('search_cleanup_days') or '30')
            
            # Calculate cutoff timestamps
            now = int(time.time())
            history_cutoff = now - (history_days * 86400)
            search_cutoff = now - (search_days * 86400)
            
            # Clean history
            self.db.execute('DELETE FROM history WHERE watched_at < ?', (history_cutoff,))
            
            # Clean search history
            self.db.execute('DELETE FROM search_history WHERE searched_at < ?', (search_cutoff,))
            
            xbmc.log('[FreeTube Service] Data cleanup completed', xbmc.LOGINFO)
        
        except Exception as e:
            xbmc.log(f'[FreeTube Service] Cleanup error: {str(e)}', xbmc.LOGERROR)
    
    def run(self):
        """Main service loop"""
        # Initial delay
        if self.monitor.waitForAbort(10):
            return
        
        # Initial health check
        self.check_api_health()
        
        # Service loop
        last_health_check = 0
        last_cleanup = 0
        health_check_interval = 3600  # 1 hour
        cleanup_interval = 86400  # 24 hours
        
        while not self.monitor.abortRequested():
            current_time = time.time()
            
            # Periodic health check
            if current_time - last_health_check > health_check_interval:
                self.check_api_health()
                last_health_check = current_time
            
            # Periodic cleanup
            if current_time - last_cleanup > cleanup_interval:
                self.cleanup_old_data()
                last_cleanup = current_time
            
            # Sleep for 60 seconds (check abort every second)
            if self.monitor.waitForAbort(60):
                break
        
        xbmc.log('[FreeTube Service] Stopped', xbmc.LOGINFO)


def main():
    """Service entry point"""
    service = FreeTubeService()
    service.run()


if __name__ == '__main__':
    main()

