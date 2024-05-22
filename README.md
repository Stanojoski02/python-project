# **Tech Gear Inventory Module**

## **Overview**

The `tech_gear_inventory` module is designed for "Tech Gear Inc.," a fictional company that sells electronic devices and accessories. This module streamlines inventory management by integrating with existing Odoo modules and incorporating functionality to parse product data from an Excel file.

## **Features**

- **Product Category Management**: Create and manage product categories.
- **Product Template Extension**: Extend the existing `product.template` model to include a category field.
- **Excel File Import**: Parse and import product data from an Excel file.
- **Automated Inventory Update**: Synchronize data from the parsed Excel file to the Odoo database.

## **Requirements**

- Odoo 16.0+ (Enterprise)
- pandas library for handling Excel files
- base64 library for file decoding

## **Installation**

1. **Unzip the module file**:
   - Unzip `tech_gear_inventory.zip` to your Odoo addons directory. You should have a directory structure like `/path/to/your/odoo/addons/tech_gear_inventory`.

2. **Navigate to the Odoo Addons Directory**:
   ```bash
   cd /path/to/your/odoo/addons
3. **Update Odoo Configuration**:
   Add the module directory to the `addons_path` in your Odoo configuration file (`odoo.conf`):
   ```bash
   addons_path = /path/to/your/odoo/addons, /path/to/your/odoo/custom_addons
4. **Restart Odoo**:
   ```bash
   sudo service odoo restart
5. **Install the Module**:
   - Navigate to the Odoo web interface.
   - Go to `Apps`.
   - Click on the menu icon to update the app list.
   - Search for `Tech Gear Inventory`.
   - Click `Install`.

## **Usage**

### **Import Products from Excel**

1. **Navigate to Tech Gear Module**:
   - Go to `Tech Gear Inventory > Tech Gear`.
   - 
![Screenshot from 2024-05-22 16-21-50.png](..%2F..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20from%202024-05-22%2016-21-50.png)
2. **Upload and Import Products**:
   - Click on the `Import Products` button.
   - Upload the Excel file (`products_data.xlsx`).
   - Click `Import Products`.
   
![Screenshot from 2024-05-22 16-27-11.png](..%2F..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20from%202024-05-22%2016-27-11.png)

3 **Upload and Import Products from Inventory**:
   - Click on the `Import Products` button.
   - Upload the Excel file (`products_data.xlsx`).
   - Click `Import Products`.


