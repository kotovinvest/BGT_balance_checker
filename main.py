import json
import pandas as pd
import logging
from web3 import Web3

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Установка подключения к RPC
RPC_URL = "https://bartio.rpc.berachain.com"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Проверка подключения
if not web3.is_connected():
    logger.error("Не удалось подключиться к RPC.")
    exit()
logger.info("Успешно подключено к RPC.")

# Адрес токена
TOKEN_ADDRESS = "0xbDa130737BDd9618301681329bF2e46A016ff9Ad"

# Загрузка ABI контракта
with open('abi.json') as abi_file:
    abi = json.load(abi_file)

# Создание контракта
token_contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=abi)
logger.info("Контракт токена успешно создан.")

# Функция для получения суммы токена на кошельках
def get_token_balances(wallets):
    balances = {}
    for wallet in wallets:
        checksum_address = web3.to_checksum_address(wallet)  # Преобразуем в контрольный адрес
        balance = token_contract.functions.balanceOf(checksum_address).call()
        # Преобразуем в удобный формат с округлением до 2 знаков после запятой
        balances[wallet] = round(web3.from_wei(balance, 'ether'), 2)  
        logger.info(f"Адрес: {wallet}, Баланс: {balances[wallet]:.2f} токенов")  # Логирование баланса
    return balances

# Чтение кошельков из файла
with open('wallets.txt') as f:
    wallets = [line.strip() for line in f if line.strip()]

# Получение и вывод балансов
balances = get_token_balances(wallets)

# Запись результатов в DataFrame и в Excel
df = pd.DataFrame(list(balances.items()), columns=['Адрес', 'Баланс'])
output_file = 'token_balances.xlsx'
df.to_excel(output_file, index=False)

logger.info(f"Результаты записаны в файл: {output_file}")
