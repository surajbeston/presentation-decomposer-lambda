import requests
import asyncio
import aiohttp
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def send_request(session, request_id):
    url = "https://xs83txxuwl.execute-api.ap-south-1.amazonaws.com/prod/"
    data = {
        "presentation": "https://pub-7c765f3726084c52bcd5d180d51f1255.r2.dev/Your%20big%20idea.pptx"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    start_time = time.time()
    logger.info(f"Starting request {request_id}")
    
    try:
        async with session.post(url, json=data, headers=headers) as response:
            elapsed = time.time() - start_time
            if response.status == 200:
                logger.info(f"Request {request_id} successful - Status: {response.status} - Time: {elapsed:.2f}s")
                return await response.text()
            else:
                logger.error(f"Request {request_id} failed - Status: {response.status} - Time: {elapsed:.2f}s")
                return None
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Request {request_id} error: {str(e)} - Time: {elapsed:.2f}s")
        return None

async def main():
    start_time = time.time()
    logger.info("Starting main execution")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(5):
            tasks.append(send_request(session, i+1))
        
        logger.info("Sending concurrent requests")
        responses = await asyncio.gather(*tasks)
        
        successful = len([r for r in responses if r is not None])
        failed = len([r for r in responses if r is None])
        
        total_time = time.time() - start_time
        logger.info(f"Execution completed - Total time: {total_time:.2f}s")
        logger.info(f"Successful requests: {successful}, Failed requests: {failed}")

if __name__ == "__main__":
    asyncio.run(main())
