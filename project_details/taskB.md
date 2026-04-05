## index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SneakerVault - Admin Dashboard</title>
</head>
<body>
  <header>
    <h1>SneakerVault</h1>
    <h2>Admin Dashboard</h2>
    <nav>
      <a href="index.html">Dashboard</a> |
      <a href="add_sneaker.html">Add Sneaker</a> |
      <a href="add_inventory.html">Add Inventory</a> |
      <a href="supplier_management.html">Supplier Management</a> |
      <a href="record_sale.html">Record Sale</a> |
      <a href="customer_management.html">Customer Management</a> |
      <a href="inventory_search.html">Inventory Search</a> |
      <a href="reports.html">Reports</a>
    </nav>
    <hr />
  </header>

  <main>
    <section>
      <h3>Key Metrics</h3>
      <p>Total Inventory Count: [Query result will appear here later]</p>
      <p>Number of Items Sold: [Query result will appear here later]</p>
      <p>Total Revenue: [Query result will appear here later]</p>
      <p>Total Profit: [Query result will appear here later]</p>
      <p><strong>Note:</strong> Metrics will be populated from database queries in a later phase.</p>
    </section>

    <section>
      <h3>Recent Sales (Preview)</h3>
      <table border="1" cellpadding="8" cellspacing="0">
        <thead>
          <tr>
            <th>Item ID</th>
            <th>Customer ID</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="2">Query results will be displayed here after database integration.</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</body>
</html>
```

## add_sneaker.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SneakerVault - Add Sneaker</title>
</head>
<body>
  <header>
    <h1>SneakerVault</h1>
    <h2>Add Sneaker</h2>
    <nav>
      <a href="index.html">Dashboard</a> |
      <a href="add_sneaker.html">Add Sneaker</a> |
      <a href="add_inventory.html">Add Inventory</a> |
      <a href="supplier_management.html">Supplier Management</a> |
      <a href="record_sale.html">Record Sale</a> |
      <a href="customer_management.html">Customer Management</a> |
      <a href="inventory_search.html">Inventory Search</a> |
      <a href="reports.html">Reports</a>
    </nav>
    <hr />
  </header>

  <main>
    <form action="#" method="post">
      <label for="sneakerId">Sneaker ID:</label><br />
      <input type="number" min="1" id="sneakerId" name="sneakerId" required /><br /><br />

      <label for="brand">Brand:</label><br />
      <input type="text" id="brand" name="brand" required /><br /><br />

      <label for="model">Model:</label><br />
      <input type="text" id="model" name="model" required /><br /><br />

      <label for="colorway">Colorway:</label><br />
      <input type="text" id="colorway" name="colorway" /><br /><br />

      <label for="releaseDate">Release Date:</label><br />
      <input type="date" id="releaseDate" name="releaseDate" /><br /><br />

      <button type="submit">Add Sneaker</button>
      <button type="reset">Clear</button>
    </form>

    <p><strong>Note:</strong> Form submission will be connected to the database in a later phase.</p>
  </main>
</body>
</html>
```

## add_inventory.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SneakerVault - Add Inventory</title>
</head>
<body>
  <header>
    <h1>SneakerVault</h1>
    <h2>Add Inventory Item</h2>
    <nav>
      <a href="index.html">Dashboard</a> |
      <a href="add_sneaker.html">Add Sneaker</a> |
      <a href="add_inventory.html">Add Inventory</a> |
      <a href="supplier_management.html">Supplier Management</a> |
      <a href="record_sale.html">Record Sale</a> |
      <a href="customer_management.html">Customer Management</a> |
      <a href="inventory_search.html">Inventory Search</a> |
      <a href="reports.html">Reports</a>
    </nav>
    <hr />
  </header>

  <main>
    <form action="#" method="post">
      <label for="itemId">Item ID:</label><br />
      <input type="number" min="1" id="itemId" name="itemId" required /><br /><br />

      <label for="sneakerId">Sneaker ID:</label><br />
      <input type="number" min="1" id="sneakerId" name="sneakerId" required /><br /><br />

      <label for="size">Size:</label><br />
      <input type="number" step="0.5" id="size" name="size" required /><br /><br />

      <label for="condition">Condition:</label><br />
      <input type="text" id="condition" name="condition" required /><br /><br />

      <label for="purchasePrice">Purchase Price:</label><br />
      <input type="number" step="0.01" id="purchasePrice" name="purchasePrice" required /><br /><br />

      <label for="purchaseDate">Purchase Date:</label><br />
      <input type="date" id="purchaseDate" name="purchaseDate" required /><br /><br />

      <label for="supplierId">Supplier ID:</label><br />
      <input type="number" min="1" id="supplierId" name="supplierId" required /><br /><br />

      <label for="status">Status:</label><br />
      <select id="status" name="status" required>
        <option value="Available">Available</option>
        <option value="Reserved">Reserved</option>
        <option value="Sold">Sold</option>
      </select><br /><br />

      <button type="submit">Add Inventory Item</button>
      <button type="reset">Clear</button>
    </form>

    <p><strong>Note:</strong> Database insert and supplier lookup will be implemented later.</p>
  </main>
</body>
</html>
```

## supplier_management.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SneakerVault - Supplier Management</title>
</head>
<body>
  <header>
    <h1>SneakerVault</h1>
    <h2>Supplier Management</h2>
    <nav>
      <a href="index.html">Dashboard</a> |
      <a href="add_sneaker.html">Add Sneaker</a> |
      <a href="add_inventory.html">Add Inventory</a> |
      <a href="supplier_management.html">Supplier Management</a> |
      <a href="record_sale.html">Record Sale</a> |
      <a href="customer_management.html">Customer Management</a> |
      <a href="inventory_search.html">Inventory Search</a> |
      <a href="reports.html">Reports</a>
    </nav>
    <hr />
  </header>

  <main>
    <section>
      <h3>Add / Edit Supplier</h3>
      <form action="#" method="post">
        <label for="supplierId">Supplier ID:</label><br />
        <input type="number" min="1" id="supplierId" name="supplierId" required /><br /><br />

        <label for="name">Name:</label><br />
        <input type="text" id="name" name="name" required /><br /><br />

        <label for="type">Type:</label><br />
        <input type="text" id="type" name="type" /><br /><br />

        <label for="contactInfo">Contact Info:</label><br />
        <input type="text" id="contactInfo" name="contactInfo" /><br /><br />

        <button type="submit">Save Supplier</button>
        <button type="reset">Clear</button>
      </form>
    </section>

    <hr />

    <section>
      <h3>Search Suppliers</h3>
      <form action="#" method="get">
        <label for="searchName">Name:</label>
        <input type="text" id="searchName" name="searchName" />

        <label for="searchType">Type:</label>
        <input type="text" id="searchType" name="searchType" />

        <button type="submit">Search</button>
      </form>

      <table border="1" cellpadding="8" cellspacing="0">
        <thead>
          <tr>
            <th>Supplier ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Contact Info</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="4">Search results will be displayed here after database integration.</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</body>
</html>
```

## record_sale.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SneakerVault - Record Sale</title>
</head>
<body>
  <header>
    <h1>SneakerVault</h1>
    <h2>Add Sale</h2>
    <nav>
      <a href="index.html">Dashboard</a> |
      <a href="add_sneaker.html">Add Sneaker</a> |
      <a href="add_inventory.html">Add Inventory</a> |
      <a href="supplier_management.html">Supplier Management</a> |
      <a href="record_sale.html">Record Sale</a> |
      <a href="customer_management.html">Customer Management</a> |
      <a href="inventory_search.html">Inventory Search</a> |
      <a href="reports.html">Reports</a>
    </nav>
    <hr />
  </header>

  <main>
    <form action="#" method="post">
      <label for="saleId">Sale ID:</label><br />
      <input type="number" min="1" id="saleId" name="saleId" required /><br /><br />

      <label for="itemId">Item ID:</label><br />
      <input type="number" min="1" id="itemId" name="itemId" required /><br /><br />

      <label for="customerId">Customer ID:</label><br />
      <input type="number" min="1" id="customerId" name="customerId" required /><br /><br />

      <label for="salePrice">Sale Price:</label><br />
      <input type="number" step="0.01" id="salePrice" name="salePrice" required /><br /><br />

      <label for="saleDate">Sale Date:</label><br />
      <input type="date" id="saleDate" name="saleDate" required /><br /><br />

      <label for="platform">Platform:</label><br />
      <select id="platform" name="platform" required>
        <option value="">Select platform</option>
        <option value="StockX">StockX</option>
        <option value="GOAT">GOAT</option>
        <option value="eBay">eBay</option>
        <option value="Local">Local</option>
      </select><br /><br />

      <button type="submit">Record Sale</button>
      <button type="reset">Clear</button>
    </form>

    <p><strong>Note:</strong> In a later phase, this form will insert into Sale and update Inventory status when needed.</p>
  </main>
</body>
</html>
```

## customer_management.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SneakerVault - Customer Management</title>
</head>
<body>
  <header>
    <h1>SneakerVault</h1>
    <h2>Customer Management</h2>
    <nav>
      <a href="index.html">Dashboard</a> |
      <a href="add_sneaker.html">Add Sneaker</a> |
      <a href="add_inventory.html">Add Inventory</a> |
      <a href="supplier_management.html">Supplier Management</a> |
      <a href="record_sale.html">Record Sale</a> |
      <a href="customer_management.html">Customer Management</a> |
      <a href="inventory_search.html">Inventory Search</a> |
      <a href="reports.html">Reports</a>
    </nav>
    <hr />
  </header>

  <main>
    <section>
      <h3>Add / Edit Customer</h3>
      <form action="#" method="post">
        <label for="customerId">Customer ID:</label><br />
        <input type="number" min="1" id="customerId" name="customerId" required /><br /><br />

        <label for="firstName">First Name:</label><br />
        <input type="text" id="firstName" name="firstName" required /><br /><br />

        <label for="lastName">Last Name:</label><br />
        <input type="text" id="lastName" name="lastName" required /><br /><br />

        <label for="email">Email:</label><br />
        <input type="email" id="email" name="email" /><br /><br />

        <label for="phone">Phone:</label><br />
        <input type="tel" id="phone" name="phone" /><br /><br />

        <button type="submit">Save Customer</button>
        <button type="reset">Clear</button>
      </form>
    </section>

    <hr />

    <section>
      <h3>Search Customers</h3>
      <form action="#" method="get">
        <label for="searchName">Name:</label>
        <input type="text" id="searchName" name="searchName" />

        <label for="searchEmail">Email:</label>
        <input type="text" id="searchEmail" name="searchEmail" />

        <button type="submit">Search</button>
      </form>

      <table border="1" cellpadding="8" cellspacing="0">
        <thead>
          <tr>
            <th>Customer ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Phone</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="5">Search results will be displayed here after database integration.</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</body>
</html>
```

## inventory_search.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SneakerVault - Inventory Search</title>
</head>
<body>
  <header>
    <h1>SneakerVault</h1>
    <h2>Inventory Search</h2>
    <nav>
      <a href="index.html">Dashboard</a> |
      <a href="add_sneaker.html">Add Sneaker</a> |
      <a href="add_inventory.html">Add Inventory</a> |
      <a href="supplier_management.html">Supplier Management</a> |
      <a href="record_sale.html">Record Sale</a> |
      <a href="customer_management.html">Customer Management</a> |
      <a href="inventory_search.html">Inventory Search</a> |
      <a href="reports.html">Reports</a>
    </nav>
    <hr />
  </header>

  <main>
    <form action="#" method="get">
      <label for="brand">Brand:</label>
      <input type="text" id="brand" name="brand" />

      <label for="size">Size:</label>
      <input type="number" step="0.5" id="size" name="size" />

      <label for="status">Status:</label>
      <select id="status" name="status">
        <option value="">Any</option>
        <option value="Available">Available</option>
        <option value="Sold">Sold</option>
        <option value="Reserved">Reserved</option>
      </select>

      <button type="submit">Search</button>
    </form>

    <h3>Search Results</h3>
    <table border="1" cellpadding="8" cellspacing="0">
      <thead>
        <tr>
          <th>Item ID</th>
          <th>Sneaker ID</th>
          <th>Brand</th>
          <th>Model</th>
          <th>Size</th>
          <th>Condition</th>
          <th>Purchase Price</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td colspan="8">Filtered inventory results will be displayed here after database integration.</td>
        </tr>
      </tbody>
    </table>
  </main>
</body>
</html>
```

## reports.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SneakerVault - Reports</title>
</head>
<body>
  <header>
    <h1>SneakerVault</h1>
    <h2>Reports</h2>
    <nav>
      <a href="index.html">Dashboard</a> |
      <a href="add_sneaker.html">Add Sneaker</a> |
      <a href="add_inventory.html">Add Inventory</a> |
      <a href="supplier_management.html">Supplier Management</a> |
      <a href="record_sale.html">Record Sale</a> |
      <a href="customer_management.html">Customer Management</a> |
      <a href="inventory_search.html">Inventory Search</a> |
      <a href="reports.html">Reports</a>
    </nav>
    <hr />
  </header>

  <main>
    <section>
      <h3>Monthly Profit</h3>
      <table border="1" cellpadding="8" cellspacing="0">
        <thead>
          <tr>
            <th>Month</th>
            <th>Total Revenue</th>
            <th>Total Cost</th>
            <th>Profit</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="4">Report output will be populated from SQL query results later.</td>
          </tr>
        </tbody>
      </table>
    </section>

    <hr />

    <section>
      <h3>Total Sales by Platform</h3>
      <table border="1" cellpadding="8" cellspacing="0">
        <thead>
          <tr>
            <th>Platform</th>
            <th>Number of Sales</th>
            <th>Total Revenue</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="3">Report output will be populated from SQL query results later.</td>
          </tr>
        </tbody>
      </table>
    </section>

    <hr />

    <section>
      <h3>Most Profitable Sneaker Models</h3>
      <table border="1" cellpadding="8" cellspacing="0">
        <thead>
          <tr>
            <th>Sneaker ID</th>
            <th>Brand</th>
            <th>Model</th>
            <th>Total Profit</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="4">Report output will be populated from SQL query results later.</td>
          </tr>
        </tbody>
      </table>
    </section>

    <p><strong>Note:</strong> These report tables are placeholders and will be dynamically filled after database connectivity is added.</p>
  </main>
</body>
</html>
```
