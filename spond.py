#!/usr/bin/env python3

import asyncio
import aiohttp
from datetime import datetime, timedelta

class Spond():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.apiurl = "https://spond.com/api/2.1/"
        self.clientsession = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar())
        self.cookie = None
        self.groups = None
        self.events = None


    async def login(self):
        url = self.apiurl + "login"
        data = { 'email': self.username, 'password': self.password }
        async with self.clientsession.post(url, json=data) as r:
            self.cookie = r.cookies['auth']

    async def getGroups(self):
        if not self.cookie:
            await self.login()
        url = self.apiurl + "groups/"
        async with self.clientsession.get(url) as r:
            self.groups = await r.json()
            return self.groups

    async def getGroup(self, uid):
        if not self.cookie:
            await self.login()

    async def getPerson(self, uid):
        if not self.cookie:
            await self.login()
        if not self.groups:
            await self.getGroups()
        for group in self.groups:
            for member in group['members']:
                if member['id'] == uid:
                    return member
                p = member.get('profile')
                if p:
                    if p['id'] == uid:
                        return member
                if 'guardians' in member:
                    for guardian in member['guardians']:
                        if guardian['id'] == uid:
                            return guardian

    async def getMessages(self):
        if not self.cookie:
            await self.login()
        url = self.apiurl + "chats/?max=10"
        async with self.clientsession.get(url) as r:
            return await r.json()


    async def getEvents(self, end_time = None):
        if not self.cookie:
            await self.login()
        if not end_time:
            end_time = datetime.now() - timedelta(days=14)
            url = self.apiurl + "sponds/?max=100&minEndTimestamp={}&order=asc&scheduled=true".format(end_time.strftime("%Y-%m-%dT00:00:00.000Z"))
            async with self.clientsession.get(url) as r:
                self.events = await r.json()
                return self.events

    async def getEventsBetween(self, start_time, end_time):
        if not self.cookie:
            await self.login()

        url = self.apiurl + "sponds/?max=100&minEndTimestamp={}&maxEndTimestamp={}&order=asc&scheduled=true".format(start_time, end_time)
        async with self.clientsession.get(url) as r:
            self.events = await r.json()
            return self.events

    async def getEvent(self, uid):
        if not self.cookie:
            await self.login()
        if not self.events:
            await self.getEvents()
        for event in self.events:
            if event['id'] == uid:
                return event
