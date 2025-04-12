import threading
from threading import Event
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from typing import Dict, Optional
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Event
import time
import random
import re
from .fetch_data import get_data

class GameInstance:
    def __init__(self, mobile_number):
        self.mobile_number = mobile_number
        self.driver = None
        self.status = "stopped"
        self.target = 0
        self.amounts = []
        self.loss = 0
        self.current_balance = 0
        self.desired_target = 0  # Add this line
        

    def start(self):
        self.status = "running"

    def stop(self):
        self.status = "stopped"
        if self.driver:
            self.driver.quit()

    def is_running(self):
        return self.status == "running"

    def update_balance(self, balance):
        self.current_balance = balance

    def update_target(self, target):
        self.target = target
    
    

    def run_game(self, config):
        try:
            wait = self.wait
            
            # XPaths
            xpaths = {
                "login_btn": '//*[@id="app"]/div[2]/div[1]/div/div/div[3]/div/div[1]',
                "mobile_input": '//*[@id="app"]/div[2]/div[4]/div[1]/div/div[1]/div[2]/input',
                "password_input": '//*[@id="app"]/div[2]/div[4]/div[1]/div/div[2]/div[2]/input',
                "login_submit": '//*[@id="app"]/div[2]/div[4]/div[1]/div/div[4]/button[1]',
                "confirm_prompt": '//*[@id="app"]/div[2]/div[12]/div[2]/button/div/span',
                "promotion": '//*[@id="app"]/div[6]/div[2]/div[2]',
                "receive": '//*[@id="app"]/div[6]/div[1]/div/div/div[3]',
                "wingo_btn": '//*[@id="app"]/div[2]/div[4]/div[2]/div/div[1]/div[2]/div[1]',
                "balance": '//*[@id="app"]/div[2]/div[2]/div/div[1]',
                "big": '//*[@id="app"]/div[2]/div[6]/div[5]/div[1]',
                "small": '//*[@id="app"]/div[2]/div[6]/div[5]/div[2]',
                "bet_input": '//*[@id="van-field-1-input"]',
                "confirm_bet": '//*[@id="app"]/div[2]/div[6]/div[7]/div/div[3]/div[2]',
                "win_loss_cut": '//*[@id="app"]/div[2]/div[10]/div/div[5]',
                "announcement": '//*[@id="app"]/div[2]/div[12]/div[2]/button/div/span'
            }

            # Utility functions
            def click_element(xpath):
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
                    return True
                except:
                    return False

            def enter_text(xpath, text):
                try:
                    input_field = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    input_field.click()
                    input_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
                    input_field.send_keys(text)
                    return True
                except:
                    return False

            # Login Process
            try:
                click_element(xpaths["login_btn"])
                enter_text(xpaths["mobile_input"], config.mobile_number)
                enter_text(xpaths["password_input"], config.password)
                click_element(xpaths["login_submit"])
                time.sleep(1)

                click_element(xpaths["confirm_prompt"])
                time.sleep(1)
                click_element(xpaths["promotion"])
                time.sleep(1)
                click_element(xpaths["announcement"])
                time.sleep(1)
                click_element(xpaths["receive"])
                time.sleep(1)
                click_element(xpaths["wingo_btn"])
                time.sleep(2)

                # Fetch Balance
                balance_text = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["balance"]))).text
                balance_numbers = re.findall(r'\d+', balance_text)
                balance_amount = int(balance_numbers[0])
                self.update_balance(balance_amount)

                # Initialize game state
                self.desired_target = config.set_target
                self.target = config.set_target
                self.amounts = config.amounts
                self.loss = config.loss

                # Betting Function
                def place_bet(outcome, amount):
                    click_element(xpaths["big"] if outcome == 'b' else xpaths["small"])
                    enter_text(xpaths["bet_input"], amount)
                    click_element(xpaths["confirm_bet"])

                # Betting Loop
                random_sb, n, target, bet_amount = None, 0, 0, config.amounts[0]
                print('Starting betting loop...')

                while self.is_running() and target <= config.set_target and target >= config.loss:
                    if time.strftime("%S") in ["00", "30"]:
                        print(f'🎯 Target: {round(target, 2)}')
                        time.sleep(5)
                        
                        click_element(xpaths["win_loss_cut"])
                        if click_element(xpaths["balance"]):
                            last_sb = get_data()

                            if random_sb and random_sb != last_sb:
                                target -= float(bet_amount)
                                n += 1
                                bet_amount = config.amounts[n % len(config.amounts)]
                            elif random_sb == last_sb:
                                target += float(bet_amount) * 0.96
                                n, bet_amount = 0, config.amounts[0]

                            random_sb = random.choice(['s', 'b'])
                            place_bet(random_sb, bet_amount)
                            self.update_target(target)

                        time.sleep(1)

                    time.sleep(0.1)

                print("✅ Betting automation completed.")
                self.stop()

            except Exception as e:
                print(f"Error in betting loop: {e}")
                self.stop()
                raise

        except Exception as e:
            print(f"Error in game setup: {e}")
            self.stop()
            raise

class GameState:
    def __init__(self):
        self._instances: Dict[str, GameInstance] = {}
        self._lock = threading.Lock()
    
class GameState:
    def __init__(self):
        self._instances: Dict[str, GameInstance] = {}
        self._lock = threading.Lock()

    def get_instance(self, mobile_number: str) -> GameInstance:
        with self._lock:
            if mobile_number not in self._instances:
                self._instances[mobile_number] = GameInstance(mobile_number)
            return self._instances[mobile_number]

    def get_all_instances(self):
        with self._lock:
            return {
                mobile: {
                    "status": instance.status,
                    "target": instance.target,
                    "current_balance": instance.current_balance,
                    "amounts": instance.amounts,
                    "loss": instance.loss,
                    "desired_target": instance.desired_target  # Add this line
                }
                for mobile, instance in self._instances.items()
                if instance.is_running()
            }

    def remove_instance(self, mobile_number: str):
        with self._lock:
            if mobile_number in self._instances:
                del self._instances[mobile_number]

game_state = GameState()  # This is the correct initialization