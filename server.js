console.log('========================================================');
console.log('  PROYEK REKAYASA API (SUB-CPMK 4) - TRAVEL EXPENSE API');
console.log('  1. Lidiya - F5512530118');
console.log('  2. Tabita Creaselia Belicia Theona - F5512520086');
console.log('  3. Muhammad Zikri Adam - F5512530117');
console.log('  4. Trista Sheryl Lambei - F5512530106');
console.log('========================================================');

const http = require('http');
const fs = require('fs/promises');
const path = require('path');
const url = require('url');

const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'data', 'expenses.json');
const PUBLIC_API_URL = 'https://open.er-api.com/v6/latest/USD';

// Target anggaran default (dalam Rupiah) untuk evaluasi batas belanja
const DEFAULT_BUDGET_LIMIT_IDR = 10000000; // Rp 10.000.000

// Cache nilai tukar mata uang (agar tetap dapat berfungsi optimal dan tahan jika jaringan kampus bermasalah)
let cachedRates = {
  USD: 1,
  IDR: 16200,
  JPY: 155,
  EUR: 0.92,
  SGD: 1.34,
  MYR: 4.70,
  GBP: 0.78,
  AUD: 1.52
};
let lastFetchedTime = null;

// ---------- Helper Respons HTTP ----------
function kirimJSON(res, statusCode, data) {
  const body = JSON.stringify(data, null, 2);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Access-Control-Allow-Origin': '*'
  });
  res.end(body);
}

function kirimError(res, statusCode, pesan, detail = null) {
  const payload = {
    sukses: false,
    status: statusCode,
    error: pesan
  };
  if (detail) payload.detail = detail;
  kirimJSON(res, statusCode, payload);
}

// ---------- Helper Request Body ----------
function bacaBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk;
    });
    req.on('end', () => {
      if (!body.trim()) return resolve(null);
      try {
        resolve(JSON.parse(body));
      } catch (err) {
        const errorJSON = new Error('Body request bukan format JSON yang valid');
        errorJSON.statusCode = 400;
        reject(errorJSON);
      }
    });
    req.on('error', reject);
  });
}

// ---------- Helper Integrasi Public API Kurs Mata Uang ----------
async function dapatkanKursTerbaru() {
  try {
    const response = await fetch(PUBLIC_API_URL, { signal: AbortSignal.timeout(4000) });
    if (response.ok) {
      const data = await response.json();
      if (data && data.rates) {
        cachedRates = data.rates;
        lastFetchedTime = new Date().toISOString();
        return { rates: cachedRates, sumber: 'live_public_api', waktu: lastFetchedTime };
      }
    }
  } catch (err) {
    console.warn('[Peringatan] Gagal memanggil Public API live, beralih ke cache data kurs.');
  }
  return { rates: cachedRates, sumber: 'cache_fallback', waktu: lastFetchedTime || 'default_rate' };
}

// Menghitung konversi nilai asing ke IDR secara presisi
function konversiKeIDR(amount, currency, rates) {
  const mataUang = currency.toUpperCase();
  const rateAsal = rates[mataUang] || 1;
  const rateIDR = rates['IDR'] || 16200;
  
  // Konversi dari mata uang asal ke USD, lalu ke IDR
  const nilaiDalamUSD = amount / rateAsal;
  const nilaiDalamIDR = Math.round(nilaiDalamUSD * rateIDR);
  const kursSatuSatuanIDR = Math.round((1 / rateAsal) * rateIDR);

  return {
    nominalIDR: nilaiDalamIDR,
    kursPerSatuanIDR: kursSatuSatuanIDR,
    formatRupiah: 'Rp ' + nilaiDalamIDR.toLocaleString('id-ID')
  };
}

// ---------- Helper Pembacaan & Penyimpanan File JSON ----------
async function bacaData() {
  try {
    const raw = await fs.readFile(DATA_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    if (err.code === 'ENOENT') {
      await simpanData([]);
      return [];
    }
    throw err;
  }
}

async function simpanData(data) {
  await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

// ---------- Helper Validasi Data Input (Defensive Programming) ----------
function validasiPayload(body, isUpdate = false) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return 'Body request wajib berupa objek JSON.';
  }

  const { title, category, amount, currency, date, notes } = body;

  if (!isUpdate || title !== undefined) {
    if (typeof title !== 'string' || title.trim() === '') {
      return 'Field "title" wajib diisi dengan teks.';
    }
  }

  const kategoriValid = ['akomodasi', 'transportasi', 'konsumsi', 'belanja', 'hiburan', 'lainnya'];
  if (!isUpdate || category !== undefined) {
    if (typeof category !== 'string' || !kategoriValid.includes(category.toLowerCase())) {
      return `Field "category" harus salah satu dari: ${kategoriValid.join(', ')}.`;
    }
  }

  if (!isUpdate || amount !== undefined) {
    if (typeof amount !== 'number' || isNaN(amount) || amount <= 0) {
      return 'Field "amount" wajib berupa angka lebih besar dari 0.';
    }
  }

  const mataUangDidukung = ['USD', 'JPY', 'EUR', 'SGD', 'MYR', 'GBP', 'AUD', 'IDR'];
  if (!isUpdate || currency !== undefined) {
    if (typeof currency !== 'string' || !mataUangDidukung.includes(currency.toUpperCase())) {
      return `Field "currency" harus salah satu dari: ${mataUangDidukung.join(', ')}.`;
    }
  }

  if (!isUpdate || date !== undefined) {
    if (typeof date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      return 'Field "date" wajib format YYYY-MM-DD (contoh: 2026-10-25).';
    }
  }

  if (notes !== undefined && typeof notes !== 'string') {
    return 'Field "notes" harus berupa teks.';
  }

  return null;
}

// ---------- Router & Request Handler ----------
const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname.replace(/\/+$/, '') || '/';
  const method = req.method.toUpperCase();
  const query = parsedUrl.query;

  try {
    // 1. ENDPOINT: GET / (Info API)
    if (pathname === '' || pathname === '/') {
      return kirimJSON(res, 200, {
        namaAplikasi: 'Travel Expense Tracker & Currency Converter RESTful API',
        kelompok: 'Kelompok 3 - Rekayasa API (Sub-CPMK 4)',
        anggota: [
          'Lidiya (F5512530118)',
          'Tabita Creaselia Belicia Theona (F5512520086)',
          'Muhammad Zikri Adam (F5512530117)',
          'Trista Sheryl Lambei (F5512530106)'
        ],
        status: 'Server Aktif Berjalan',
        daftarEndpoint: [
          'GET /expenses - Mendapatkan seluruh pengeluaran (bisa filter ?category=...&currency=...)',
          'GET /expenses/summary - Ringkasan total dalam IDR & evaluasi batas anggaran',
          'GET /expenses/:id - Mendapatkan detail satu catatan pengeluaran',
          'POST /expenses - Menambahkan catatan pengeluaran baru',
          'PUT /expenses/:id - Memperbarui catatan pengeluaran',
          'DELETE /expenses/:id - Menghapus catatan pengeluaran'
        ]
      });
    }

    // 2. ENDPOINT: GET /expenses/summary (Logika Pengolahan Data Public API + Analisis Anggaran)
    if (pathname === '/expenses/summary' && method === 'GET') {
      const dataExpenses = await bacaData();
      const kursInfo = await dapatkanKursTerbaru();
      const limitBudgetIDR = Number(query.budget) || DEFAULT_BUDGET_LIMIT_IDR;

      let totalAkumulasiIDR = 0;
      const breakdownKategori = {};

      dataExpenses.forEach((item) => {
        const hasilKonversi = konversiKeIDR(item.amount, item.currency, kursInfo.rates);
        totalAkumulasiIDR += hasilKonversi.nominalIDR;

        if (!breakdownKategori[item.category]) {
          breakdownKategori[item.category] = { totalIDR: 0, count: 0 };
        }
        breakdownKategori[item.category].totalIDR += hasilKonversi.nominalIDR;
        breakdownKategori[item.category].count += 1;
      });

      const sisaAnggaranIDR = limitBudgetIDR - totalAkumulasiIDR;
      const persentasePemakaian = Number(((totalAkumulasiIDR / limitBudgetIDR) * 100).toFixed(2));

      // Evaluasi Risiko Anggaran (Server-side Business Logic)
      let evaluasiRisiko = 'SAFE: Anggaran Masih Aman Terkendali';
      let tingkatRisiko = 'RENDAH';
      if (persentasePemakaian > 100) {
        evaluasiRisiko = 'DANGER: Pengeluaran Telah Melebihi Batas Anggaran (Over Budget)!';
        tingkatRisiko = 'TINGGI (BAHAYA)';
      } else if (persentasePemakaian >= 80) {
        evaluasiRisiko = 'WARNING: Peringatan Kritis! Lebih dari 80% Kuota Anggaran Terpakai!';
        tingkatRisiko = 'SEDANG (WASPADA)';
      }

      return kirimJSON(res, 200, {
        sukses: true,
        ringkasanAnggaran: {
          targetAnggaranIDR: limitBudgetIDR,
          formatTargetAnggaran: 'Rp ' + limitBudgetIDR.toLocaleString('id-ID'),
          totalPengeluaranIDR: totalAkumulasiIDR,
          formatTotalPengeluaran: 'Rp ' + totalAkumulasiIDR.toLocaleString('id-ID'),
          sisaAnggaranIDR: sisaAnggaranIDR,
          formatSisaAnggaran: 'Rp ' + sisaAnggaranIDR.toLocaleString('id-ID'),
          persentasePemakaian: `${persentasePemakaian}%`,
          tingkatRisiko: tingkatRisiko,
          statusEvaluasi: evaluasiRisiko
        },
        rincianKategori: breakdownKategori,
        totalCatatan: dataExpenses.length,
        metadataKurs: {
          sumberAPI: 'ExchangeRate-API (open.er-api.com)',
          statusPemanggilan: kursInfo.sumber,
          kursIDRperUSD: kursInfo.rates['IDR'],
          terakhirDiperbarui: kursInfo.waktu
        }
      });
    }

    // 3. ENDPOINT: GET & POST pada /expenses
    if (pathname === '/expenses') {
      const dataExpenses = await bacaData();
      const kursInfo = await dapatkanKursTerbaru();

      // --- GET /expenses (Dengan Pengayaan Data Public API & Filter) ---
      if (method === 'GET') {
        let hasil = dataExpenses.map((item) => {
          const konversi = konversiKeIDR(item.amount, item.currency, kursInfo.rates);
          return {
            ...item,
            pengayaanKurs: {
              nominalIDR: konversi.nominalIDR,
              formatRupiah: konversi.formatRupiah,
              kursAcuanKeIDR: `1 ${item.currency} ≈ Rp ${konversi.kursPerSatuanIDR.toLocaleString('id-ID')}`
            }
          };
        });

        // Filter kategori jika diberikan via query param (?category=akomodasi)
        if (query.category) {
          hasil = hasil.filter(
            (item) => item.category.toLowerCase() === query.category.toLowerCase()
          );
        }

        // Filter currency jika diberikan via query param (?currency=JPY)
        if (query.currency) {
          hasil = hasil.filter(
            (item) => item.currency.toUpperCase() === query.currency.toUpperCase()
          );
        }

        return kirimJSON(res, 200, {
          sukses: true,
          jumlah: hasil.length,
          data: hasil
        });
      }

      // --- POST /expenses (Tambah Data Baru & Simpan ke File fs) ---
      if (method === 'POST') {
        const body = await bacaBody(req);
        const pesanErrorValidasi = validasiPayload(body, false);

        if (pesanErrorValidasi) {
          return kirimError(res, 400, pesanErrorValidasi);
        }

        // Generate ID baru secara inkremental
        const idBaru = dataExpenses.length > 0 ? Math.max(...dataExpenses.map((d) => d.id)) + 1 : 1;

        const itemBaru = {
          id: idBaru,
          title: body.title.trim(),
          category: body.category.toLowerCase().trim(),
          amount: Number(body.amount),
          currency: body.currency.toUpperCase().trim(),
          date: body.date,
          notes: body.notes ? body.notes.trim() : ''
        };

        dataExpenses.push(itemBaru);
        await simpanData(dataExpenses);

        const konversi = konversiKeIDR(itemBaru.amount, itemBaru.currency, kursInfo.rates);

        return kirimJSON(res, 201, {
          sukses: true,
          pesan: 'Catatan pengeluaran berhasil ditambahkan.',
          data: {
            ...itemBaru,
            pengayaanKurs: {
              nominalIDR: konversi.nominalIDR,
              formatRupiah: konversi.formatRupiah,
              kursAcuanKeIDR: `1 ${itemBaru.currency} ≈ Rp ${konversi.kursPerSatuanIDR.toLocaleString('id-ID')}`
            }
          }
        });
      }

      return kirimError(res, 405, `Metode ${method} tidak diizinkan pada /expenses`);
    }

    // 4. ENDPOINT: /expenses/:id (GET detail, PUT update, DELETE)
    const matchId = pathname.match(/^\/expenses\/(\d+)$/);
    if (matchId) {
      const targetId = parseInt(matchId[1], 10);
      const dataExpenses = await bacaData();
      const itemIndex = dataExpenses.findIndex((d) => d.id === targetId);

      // --- GET /expenses/:id ---
      if (method === 'GET') {
        if (itemIndex === -1) {
          return kirimError(res, 404, `Pengeluaran dengan ID ${targetId} tidak ditemukan.`);
        }

        const kursInfo = await dapatkanKursTerbaru();
        const item = dataExpenses[itemIndex];
        const konversi = konversiKeIDR(item.amount, item.currency, kursInfo.rates);

        return kirimJSON(res, 200, {
          sukses: true,
          data: {
            ...item,
            pengayaanKurs: {
              nominalIDR: konversi.nominalIDR,
              formatRupiah: konversi.formatRupiah,
              kursAcuanKeIDR: `1 ${item.currency} ≈ Rp ${konversi.kursPerSatuanIDR.toLocaleString('id-ID')}`
            }
          }
        });
      }

      // --- PUT /expenses/:id ---
      if (method === 'PUT') {
        if (itemIndex === -1) {
          return kirimError(res, 404, `Pengeluaran dengan ID ${targetId} tidak ditemukan.`);
        }

        const body = await bacaBody(req);
        const pesanErrorValidasi = validasiPayload(body, true);
        if (pesanErrorValidasi) {
          return kirimError(res, 400, pesanErrorValidasi);
        }

        const itemLama = dataExpenses[itemIndex];
        const itemDiperbarui = {
          ...itemLama,
          ...(body.title !== undefined && { title: body.title.trim() }),
          ...(body.category !== undefined && { category: body.category.toLowerCase().trim() }),
          ...(body.amount !== undefined && { amount: Number(body.amount) }),
          ...(body.currency !== undefined && { currency: body.currency.toUpperCase().trim() }),
          ...(body.date !== undefined && { date: body.date }),
          ...(body.notes !== undefined && { notes: body.notes.trim() })
        };

        dataExpenses[itemIndex] = itemDiperbarui;
        await simpanData(dataExpenses);

        const kursInfo = await dapatkanKursTerbaru();
        const konversi = konversiKeIDR(itemDiperbarui.amount, itemDiperbarui.currency, kursInfo.rates);

        return kirimJSON(res, 200, {
          sukses: true,
          pesan: `Pengeluaran dengan ID ${targetId} berhasil diperbarui.`,
          data: {
            ...itemDiperbarui,
            pengayaanKurs: {
              nominalIDR: konversi.nominalIDR,
              formatRupiah: konversi.formatRupiah
            }
          }
        });
      }

      // --- DELETE /expenses/:id ---
      if (method === 'DELETE') {
        if (itemIndex === -1) {
          return kirimError(res, 404, `Pengeluaran dengan ID ${targetId} tidak ditemukan.`);
        }

        const itemDihapus = dataExpenses.splice(itemIndex, 1)[0];
        await simpanData(dataExpenses);

        return kirimJSON(res, 200, {
          sukses: true,
          pesan: `Pengeluaran dengan ID ${targetId} ("${itemDihapus.title}") berhasil dihapus.`,
          idDihapus: targetId
        });
      }

      return kirimError(res, 405, `Metode ${method} tidak diizinkan pada /expenses/${targetId}`);
    }

    // Jika endpoint tidak ditemukan (404)
    kirimError(res, 404, `Endpoint ${method} ${pathname} tidak ditemukan.`);
  } catch (error) {
    console.error('Server Internal Error:', error);
    if (error.statusCode === 400) {
      return kirimError(res, 400, error.message);
    }
    kirimError(res, 500, 'Terjadi kesalahan internal pada server.', error.message);
  }
});

server.listen(PORT, () => {
  console.log(`Server aktif berjalan di http://localhost:${PORT}`);
  console.log(`Tekan Ctrl + C untuk mematikan server.`);
});
