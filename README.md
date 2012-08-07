iStockFinancial
===============

sina stock and financial statistical tools.

It includes client and server, client provide tools to download industry and stock information to sqlite3 database.
server provide Web access interface.

The development is based on python 2.6.1 and urllib3 V1.4

client step
===============
1. please install python 2.6.1
2. wget -O urllib3-V1.4.zip https://github.com/shazow/urllib3/zipball/1.4
3. unzip urllib3-V1.4.zip
4. cd shazow-urllib3-1ffd99e
4. sudo python setup.py install
5. cd ../client
6. python main.py .

as step 6, client will download year 1989~2011 stock financial information and save to current directory.
you also can indicate a year as parameter, such as 'python main.py . 2011'
