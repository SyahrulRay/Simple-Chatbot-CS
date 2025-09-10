PRAGMA foreign_keys = ON;

-- User 
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT
);


CREATE TABLE IF NOT EXISTS conversations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Pesan
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id INTEGER NOT NULL,
  role TEXT CHECK(role IN ('user','assistant','system')) NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- Produk
CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  features TEXT,     -- bullet/JSON string ringkas fitur
  warranty_policy TEXT
);

CREATE TABLE IF NOT EXISTS orders (
  id TEXT PRIMARY KEY,
  user_id INTEGER,
  product_id TEXT,
  status TEXT,       
  last_update DATETIME,
  courier TEXT,
  tracking_number TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert Users
INSERT OR IGNORE INTO users(id, name) VALUES 
 (1,'Syahrul'),
 (2,'Ujang');

-- Insert Products
INSERT OR IGNORE INTO products(id,name,features,warranty_policy) VALUES
 ('P001','Headset X','- ANC\n- 40h battery\n- BT 5.3','Garansi 1 tahun, klaim via invoice + video unboxing.'),
 ('P002','Keyboard Y','- Hot-swappable\n- RGB\n- Gasket mount','Garansi 1 tahun, kerusakan pabrik saja.'),
 ('P003','Mouse Z','- Wireless\n- 16000 DPI\n- RGB Lighting','Garansi 6 bulan, claim dengan invoice.'),
 ('P004','Monitor A','- 27 inch 144Hz\n- IPS Panel\n- 1ms response','Garansi 2 tahun, klaim ke service center resmi.'),
 ('P005','Laptop B','- Intel i7\n- 16GB RAM\n- 512GB SSD','Garansi 1 tahun, tidak termasuk kerusakan akibat cairan.');

-- Syahrul's Order (user_id = 1)
INSERT OR IGNORE INTO orders(id,user_id,product_id,status,last_update,courier,tracking_number) VALUES
 ('ORD123',1,'P001','dikirim',datetime('now','-1 day'),'JNE','JNE12345678'),
 ('ORD124',1,'P002','diproses',datetime('now','-2 day'),'SiCepat','SCP98765432'),
 ('ORD125',1,'P005','selesai',datetime('now','-10 day'),'J&T','JNT55566677');

-- ujang's Order (user_id = 2)
INSERT OR IGNORE INTO orders(id,user_id,product_id,status,last_update,courier,tracking_number) VALUES
 ('ORD200',2,'P003','dikirim',datetime('now','-3 day'),'Pos Indonesia','POS11223344'),
 ('ORD201',2,'P004','diproses',datetime('now','-1 day'),'JNE','JNE88990011'),
 ('ORD202',2,'P001','selesai',datetime('now','-5 day'),'TIKI','TIKI44556677');