# PookieClaude — Vibe Code Day 1

โปรเจคทดลอง vibe coding รวมหลายเดโมเล็ก ๆ

## ไฟล์ในโปรเจค

| ไฟล์ | คำอธิบาย |
|------|----------|
| [`lucky-colors.html`](lucky-colors.html) | ระบบเลือกสีเสื้อผ้ามงคลตามวันเกิด+วันที่ ตามโหราศาสตร์ไทย — Wizard 4 ขั้น พร้อม 4 หมวด (การงาน, การเงิน, ความรัก, เมตตา) |
| [`form.html`](form.html) | ฟอร์มลงทะเบียน (frontend) |
| [`admin.html`](admin.html) | หน้า admin ดูรายชื่อผู้ลงทะเบียน |
| [`server.js`](server.js) | Express server สำหรับระบบลงทะเบียน |
| [`server.py`](server.py) | เวอร์ชัน Python ของ server |

## วิธีใช้

### Lucky Colors (HTML เดี่ยว)
เปิดไฟล์ `lucky-colors.html` ในเบราว์เซอร์ได้เลย ไม่ต้องใช้ server

### Registration System
```bash
npm install
npm start
# เปิด http://localhost:3000/form.html
```

## Tech
- Vanilla HTML/CSS/JS (no framework)
- Node.js + Express สำหรับ backend
- Thai astrology color logic
