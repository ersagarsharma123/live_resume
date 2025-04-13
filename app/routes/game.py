from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.chrome.options import Options
from .fetch_data import get_data
from .state import game_state

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

class GameConfig(BaseModel):
    mobile_number: str
    password: str
    amounts: List[str]
    set_target: float
    loss: float

@router.get("/game")
async def game(request: Request):
    return templates.TemplateResponse("game.html", {"request": request})


@router.post("/api/start-game")
async def start_game(config: GameConfig, background_tasks: BackgroundTasks):
    instance = game_state.get_instance(config.mobile_number)
    
    if instance.is_running():
        raise HTTPException(status_code=400, detail=f"Game is already running for {config.mobile_number}")
    
    try:
        chrome_driver_path = r"C:\ProgramData\chocolatey\lib\chromedriver\tools\chromedriver-win64\chromedriver.exe"
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless=new") 
        
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
        wait = WebDriverWait(driver, 10)  # Initialize WebDriverWait here
        driver.get("https://damangames.bet")
        time.sleep(3)
        instance.driver = driver
        instance.start()
        instance.wait = wait  # Set the wait object in the instance
        background_tasks.add_task(instance.run_game, config)  # Pass the config to run_game     
        return {"message": "Game started successfully", "mobile_number": config.mobile_number}

    except Exception as e:
        if instance.driver:
            instance.driver.quit()
        instance.stop()
        raise HTTPException(status_code=500, detail=str(e))
class StopGameRequest(BaseModel):
    mobile_number: str

@router.post("/api/stop-game")
async def stop_game(request: StopGameRequest):
    instance = game_state.get_instance(request.mobile_number)
    try:
        if instance.driver:
            instance.driver.quit()
        instance.stop()
        return {"message": "Game stopped successfully", "mobile_number": request.mobile_number}
    except Exception as e:
        print(f"Error stopping game: {e}")
        return {"message": "Error stopping game", "error": str(e), "mobile_number": request.mobile_number}

@router.get("/api/game-status")
async def game_status():
    return game_state.get_all_instances()