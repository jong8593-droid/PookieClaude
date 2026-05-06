const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'data.json');

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

function readData() {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
}

function writeData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

// POST /api/register — บันทึกผู้ลงทะเบียน
app.post('/api/register', (req, res) => {
  const { name, email, phone } = req.body;

  if (!name || !email || !phone) {
    return res.status(400).json({ error: 'กรุณากรอกข้อมูลให้ครบถ้วน' });
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    return res.status(400).json({ error: 'รูปแบบอีเมลไม่ถูกต้อง' });
  }

  const phoneDigits = phone.replace(/[-\s]/g, '');
  if (!/^\d{10}$/.test(phoneDigits)) {
    return res.status(400).json({ error: 'เบอร์โทรต้องมี 10 หลัก' });
  }

  const records = readData();

  const duplicate = records.find(r => r.email === email.toLowerCase());
  if (duplicate) {
    return res.status(409).json({ error: 'อีเมลนี้ลงทะเบียนไปแล้ว' });
  }

  const newRecord = {
    id: Date.now(),
    name: name.trim(),
    email: email.trim().toLowerCase(),
    phone: phone.trim(),
    registeredAt: new Date().toISOString()
  };

  records.push(newRecord);
  writeData(records);

  res.status(201).json({ message: 'ลงทะเบียนสำเร็จ', data: newRecord });
});

// GET /api/registrations — ดึงรายชื่อทั้งหมด
app.get('/api/registrations', (req, res) => {
  const records = readData();
  res.json({ total: records.length, data: records });
});

// DELETE /api/registrations/:id — ลบรายการ
app.delete('/api/registrations/:id', (req, res) => {
  const id = parseInt(req.params.id);
  let records = readData();
  const before = records.length;
  records = records.filter(r => r.id !== id);

  if (records.length === before) {
    return res.status(404).json({ error: 'ไม่พบรายการ' });
  }

  writeData(records);
  res.json({ message: 'ลบเรียบร้อยแล้ว' });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
  console.log(`Admin dashboard: http://localhost:${PORT}/admin.html`);
  console.log(`Registration form: http://localhost:${PORT}/form.html`);
});
