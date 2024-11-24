#!/usr/bin/env python3
# app for sending info from radiometr to local db

# import sys
import serial
import sqlite3
import minimalmodbus # https://pypi.org/project/minimalmodbus/

# modbus порт та десятковий адрес радіометра
instrument = minimalmodbus.Instrument('/dev/pts/1', 1, minimalmodbus.MODE_RTU)

# налаштування порта
instrument.serial.baudrate = 9600  # Baud
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 0.05  # seconds
instrument.clear_buffers_before_each_transaction = True


# Зчитування регистрів
MIS1_reg = instrument.read_registers(8704, 112, 4)
MIS2_reg = instrument.read_registers(40960, 3, 3)
MIS3_reg = instrument.read_registers(40963, 48, 3)
MIS4_reg = instrument.read_registers(16640, 33, 4)
MAD1_reg = instrument.read_registers(17152, 81, 4)
MKU1_reg = instrument.read_registers(12288, 3, 4)


# Обробка помилок порта
try:
    print(instrument.read_register(4143))
except IOError:
    print("Failed to read from instrument")


# Завантажуємо в SQL
connection = sqlite3.connect('test.db')
cursor = connection.cursor()

# Додаємо в таблицю значення регистрів

cursor.execute(
    'INSERT INTO host3_e (curent_amount_1, curent_amount_2, curent_amount_4, curent_amount_4) VALUES (?, ?, ?, ?)',
    (
        float(MIS1_reg[28]),
        float(MIS1_reg[30]),
        float(MIS1_reg[32]),
        float(MIS1_reg[34]),
    )
)

cursor.execute(
    'INSERT INTO host3_e (state_amount_1, state_amount_2, state_amount_4, state_amount_4) VALUES (?, ?, ?, ?)',
    (
        float(MIS1_reg[12]),
        float(MIS1_reg[14]),
        float(MIS1_reg[16]),
        float(MIS1_reg[18]),
    )
)

cursor.execute(
    'INSERT INTO host3_e (triger_1, triger_2, triger_3, triger_4) VALUES (?, ?, ?, ?)',
    (
        MIS1_reg[4] >> 5,
        MIS1_reg[4] >> 6,
        MIS1_reg[4] >> 7,
        MIS1_reg[4] >> 8,
    )
)


connection.commit()
connection.close()
