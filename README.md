# HSNscrapper

A python web scraping script crafted to automate data extraction from the [HSN](https://www.hsnstore.com/) shopping cart. If you want to receive alerts, you can join this [Telegram channel](https://t.me/hsnscrapper) where the price of the products is checked daily. This is what the alerts channel looks like.
![image](https://github.com/addreeh/HSNscrapper/assets/74270582/ef747766-abb5-407f-b965-e12aa470874b)



## Installation
To use the script you need to have installed Firefox and Python.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

This script is ready to work and store data in a MongoDB database. If you want to use the same system, you will need to install [MongoDB](https://www.mongodb.com/docs/manual/installation/). If you only want to display the current prices of the products, you can use NoDB script.


## Usage
The command to use Python will depend on the operating system; typically, in Ubuntu, *python3* is used, and in Windows, *python*. However, it will all depend on your Python installation on the system.

To run the script with the MongoDB database.
```bash
python3 hsn.py
```

To run the script without the MongoDB database.
```bash
python3 hsnNoDB.py
```

## Customize It
In the script, only two products are considered, which are the ones added to the cart, the [EVOWHEY PROTEIN 2.0 2KG](https://www.hsnstore.com/marcas/sport-series/evowhey-protein-2-0) and the [EVOCASEIN 2.0 (MICELLAR CASEIN + DIGEZYME) 2KG](https://www.hsnstore.com/marcas/sport-series/evocasein-2-0-caseina-micelar-digezyme). If you want the script to include more products, you will need to add them to your shopping cart and insert a new product into the script.

As you can see, each product must have specific information.
![image](https://github.com/addreeh/HSNscrapper/assets/74270582/a29e9c35-7ab9-45d4-8dd3-8d2b85139c90)

To obtain these data, you will need to access the browser's developer tool (F12).
![image](https://github.com/addreeh/HSNscrapper/assets/74270582/e6bb66ce-49e6-48c6-acb1-3d293780eead)

Once you have obtained the data, you simply need to insert a new product into the script.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
