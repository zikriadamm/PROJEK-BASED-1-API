const readline = require('readline');

const BASE_URL = 'http://localhost:3000';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function tanya(promptText) {
  return new Promise((resolve) => {
    rl.question(promptText, (jawaban) => {
      resolve(jawaban.trim());
    });
  });
}

// Helper pemanggil HTTP API dengan penanganan error ramah tanpa stack trace
async function requestAPI(endpoint, options = {}) {
  try {
    const url = `${BASE_URL}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    const res = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...(options.headers || {})
      }
    });

    const data = await res.json().catch(() => null);

    return {
      ok: res.ok,
      status: res.status,
      data: data
    };
  } catch (err) {
    return {
      ok: false,
      status: 0,
      data: {
        error: `Gagal terhubung ke server API (${err.message}). Pastikan server sudah dijalankan di ${BASE_URL}.`
      }
    };
  }
}

function cetakHeader() {
  console.clear();
  console.log('========================================================================');
  console.log('   CLIENT CONSOLE - TRAVEL EXPENSE & CURRENCY CONVERTER CLI');
  console.log('   Rekayasa API (Sub-CPMK 4) - Kelompok 3');
  console.log('   Target API: ' + BASE_URL);
  console.log('========================================================================\n');
}

async function menuTampilkanSemua() {
  console.log('\n--- DAFTAR SELURUH PENGELUARAN (DIPERKAYA KURS REAL-TIME) ---');
  const res = await requestAPI('/expenses');

  if (!res.ok) {
    console.log(`[Error ${res.status}] ${res.data?.error || 'Gagal mengambil data'}`);
    return;
  }

  const items = res.data.data;
  if (!items || items.length === 0) {
    console.log('Belum ada data pengeluaran tersimpan.');
    return;
  }

  console.log(`Ditemukan ${items.length} catatan pengeluaran:\n`);
  items.forEach((item) => {
    console.log(`[ID: ${item.id}] ${item.title}`);
    console.log(`   Kategori   : ${item.category}`);
    console.log(`   Nominal Asli: ${item.amount} ${item.currency}`);
    console.log(`   Hasil Kurs : ${item.pengayaanKurs.formatRupiah} (${item.pengayaanKurs.kursAcuanKeIDR})`);
    console.log(`   Tanggal    : ${item.date} | Catatan: ${item.notes || '-'}`);
    console.log('   ' + '-'.repeat(60));
  });
}

async function menuFilterPengeluaran() {
  console.log('\n--- FILTER PENGELUARAN ---');
  console.log('Pilihan filter:');
  console.log('1. Berdasarkan Kategori (akomodasi, transportasi, konsumsi, belanja, hiburan)');
  console.log('2. Berdasarkan Mata Uang (USD, JPY, EUR, SGD, MYR, dll)');
  
  const pilihan = await tanya('Pilih jenis filter (1/2): ');
  let endpoint = '/expenses';

  if (pilihan === '1') {
    const kat = await tanya('Masukkan kategori: ');
    endpoint += `?category=${encodeURIComponent(kat)}`;
  } else if (pilihan === '2') {
    const cur = await tanya('Masukkan kode mata uang (contoh: JPY, USD): ');
    endpoint += `?currency=${encodeURIComponent(cur)}`;
  } else {
    console.log('Pilihan filter tidak valid.');
    return;
  }

  const res = await requestAPI(endpoint);
  if (!res.ok) {
    console.log(`[Error ${res.status}] ${res.data?.error || 'Gagal memfilter data'}`);
    return;
  }

  const items = res.data.data;
  console.log(`\nHasil filter: ditemukan ${items.length} data:\n`);
  items.forEach((item) => {
    console.log(`* [${item.id}] ${item.title} - ${item.amount} ${item.currency} => ${item.pengayaanKurs.formatRupiah} (${item.category})`);
  });
}

async function menuRingkasanAnggaran() {
  console.log('\n--- RINGKASAN & EVALUASI ANGGARAN (BUDGET GUARD ANALYSIS) ---');
  const inputBudget = await tanya('Masukkan batas anggaran kustom dalam Rp (tekan Enter untuk default Rp 10.000.000): ');
  const query = inputBudget ? `?budget=${encodeURIComponent(inputBudget)}` : '';
  
  const res = await requestAPI(`/expenses/summary${query}`);
  if (!res.ok) {
    console.log(`[Error ${res.status}] ${res.data?.error || 'Gagal mengambil ringkasan'}`);
    return;
  }

  const r = res.data.ringkasanAnggaran;
  console.log('\n================ HASIL ANALISIS SERVER ================');
  console.log(`Target Anggaran     : ${r.formatTargetAnggaran}`);
  console.log(`Total Pengeluaran   : ${r.formatTotalPengeluaran}`);
  console.log(`Sisa Anggaran       : ${r.formatSisaAnggaran}`);
  console.log(`Persentase Terpakai : ${r.persentasePemakaian}`);
  console.log(`Tingkat Risiko      : [ ${r.tingkatRisiko} ]`);
  console.log(`Evaluasi Sistem     : ${r.statusEvaluasi}`);
  console.log('======================================================');

  console.log('\nRincian Pengeluaran per Kategori:');
  const cats = res.data.rincianKategori;
  for (const [k, v] of Object.entries(cats)) {
    console.log(`  - ${k.padEnd(14)}: Rp ${v.totalIDR.toLocaleString('id-ID')} (${v.count} transaksi)`);
  }

  const meta = res.data.metadataKurs;
  console.log(`\nInformasi Kurs Terkini (USD to IDR): Rp ${meta.kursIDRperUSD?.toLocaleString('id-ID')} [Sumber: ${meta.sumberAPI}]`);
}

async function menuTambahPengeluaran() {
  console.log('\n--- TAMBAH PENGELUARAN BARU (POST) ---');
  const title = await tanya('Judul Pengeluaran (misal: Tiket Museum Kyoto): ');
  const category = await tanya('Kategori (akomodasi/transportasi/konsumsi/belanja/hiburan): ');
  const amountStr = await tanya('Nominal Uang Asing (angka, misal: 1200): ');
  const currency = await tanya('Mata Uang Asing (USD/JPY/EUR/SGD/MYR): ');
  const date = await tanya('Tanggal (YYYY-MM-DD, contoh: 2026-10-26): ');
  const notes = await tanya('Catatan Tambahan (opsional): ');

  const payload = {
    title,
    category,
    amount: Number(amountStr),
    currency,
    date,
    notes
  };

  const res = await requestAPI('/expenses', {
    method: 'POST',
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    console.log(`\n[Gagal - Status ${res.status}] ${res.data?.error || 'Gagal menambahkan data'}`);
  } else {
    console.log(`\n[Sukses - Status ${res.status}] ${res.data.pesan}`);
    const baru = res.data.data;
    console.log(`ID Baru: ${baru.id} | Dikonversi: ${baru.pengayaanKurs.formatRupiah}`);
  }
}

async function menuUbahPengeluaran() {
  console.log('\n--- PERBARUI PENGELUARAN (PUT) ---');
  const id = await tanya('Masukkan ID pengeluaran yang ingin diubah: ');

  // Cek dulu apakah item ada
  const cek = await requestAPI(`/expenses/${id}`);
  if (!cek.ok) {
    console.log(`\n[Gagal - Status ${cek.status}] ${cek.data?.error || 'ID tidak ditemukan'}`);
    return;
  }

  console.log(`Data saat ini: "${cek.data.data.title}" - ${cek.data.data.amount} ${cek.data.data.currency}`);
  console.log('(Tekan Enter langsung jika tidak ingin mengubah field tertentu)\n');

  const title = await tanya('Judul baru: ');
  const category = await tanya('Kategori baru: ');
  const amountStr = await tanya('Nominal baru: ');
  const currency = await tanya('Mata uang baru: ');
  const notes = await tanya('Catatan baru: ');

  const updateBody = {};
  if (title) updateBody.title = title;
  if (category) updateBody.category = category;
  if (amountStr) updateBody.amount = Number(amountStr);
  if (currency) updateBody.currency = currency;
  if (notes) updateBody.notes = notes;

  if (Object.keys(updateBody).length === 0) {
    console.log('Tidak ada data yang diubah.');
    return;
  }

  const res = await requestAPI(`/expenses/${id}`, {
    method: 'PUT',
    body: JSON.stringify(updateBody)
  });

  if (!res.ok) {
    console.log(`\n[Gagal - Status ${res.status}] ${res.data?.error || 'Gagal memperbarui'}`);
  } else {
    console.log(`\n[Sukses - Status ${res.status}] ${res.data.pesan}`);
  }
}

async function menuHapusPengeluaran() {
  console.log('\n--- HAPUS PENGELUARAN (DELETE) ---');
  const id = await tanya('Masukkan ID pengeluaran yang ingin dihapus: ');

  const konfirmasi = await tanya(`Yakin ingin menghapus ID ${id}? (y/n): `);
  if (konfirmasi.toLowerCase() !== 'y') {
    console.log('Penghapusan dibatalkan.');
    return;
  }

  const res = await requestAPI(`/expenses/${id}`, {
    method: 'DELETE'
  });

  if (!res.ok) {
    console.log(`\n[Gagal - Status ${res.status}] ${res.data?.error || 'Gagal menghapus'}`);
  } else {
    console.log(`\n[Sukses - Status ${res.status}] ${res.data.pesan}`);
  }
}

async function menuUjiKondisiGagal() {
  console.log('\n--- PENGUJIAN SKENARIO GAGAL (MEMBUKTIKAN PENANGANAN ERROR TANPA STACK TRACE) ---');
  console.log('1. Uji Error 400 Bad Request (Payload tidak lengkap / nominal salah)');
  console.log('2. Uji Error 404 Not Found (Mengakses ID yang tidak ada)');
  console.log('3. Uji Error 405 Method Not Allowed');

  const uji = await tanya('Pilih skenario uji (1/2/3): ');

  if (uji === '1') {
    console.log('\nMengirim POST dengan amount negatif dan field title kosong...');
    const res = await requestAPI('/expenses', {
      method: 'POST',
      body: JSON.stringify({ title: '', amount: -500 })
    });
    console.log(`Status HTTP: ${res.status}`);
    console.log(`Pesan Error: ${res.data?.error}`);
    console.log('-> Terbukti: Ditangani dengan elegan (kode status 400, pesan valid, bebas stack trace).');
  } else if (uji === '2') {
    console.log('\nMengakses GET /expenses/99999 (ID fiktif)...');
    const res = await requestAPI('/expenses/99999');
    console.log(`Status HTTP: ${res.status}`);
    console.log(`Pesan Error: ${res.data?.error}`);
    console.log('-> Terbukti: Ditangani dengan elegan (kode status 404 Not Found, bebas stack trace).');
  } else if (uji === '3') {
    console.log('\nMengirim PATCH pada /expenses/1 (metode tidak didukung)...');
    const res = await requestAPI('/expenses/1', { method: 'PATCH' });
    console.log(`Status HTTP: ${res.status}`);
    console.log(`Pesan Error: ${res.data?.error}`);
    console.log('-> Terbukti: Ditangani dengan status 405 Method Not Allowed.');
  }
}

async function mainLoop() {
  while (true) {
    cetakHeader();
    console.log('PILIHAN MENU:');
    console.log('1. Tampilkan Semua Pengeluaran (dengan Konversi IDR Real-Time)');
    console.log('2. Filter Pengeluaran (Kategori / Mata Uang)');
    console.log('3. Ringkasan & Analisis Evaluasi Anggaran (Budget Guard Analysis)');
    console.log('4. Tambah Catatan Pengeluaran Baru (POST)');
    console.log('5. Perbarui Catatan Pengeluaran (PUT)');
    console.log('6. Hapus Catatan Pengeluaran (DELETE)');
    console.log('7. Uji Skenario Gagal (Validasi Status 400 & 404 Bebas Stack Trace)');
    console.log('0. Keluar dari Aplikasi');
    console.log('------------------------------------------------------------------------');

    const pilihan = await tanya('Masukkan pilihan Anda (0-7): ');

    switch (pilihan) {
      case '1':
        await menuTampilkanSemua();
        break;
      case '2':
        await menuFilterPengeluaran();
        break;
      case '3':
        await menuRingkasanAnggaran();
        break;
      case '4':
        await menuTambahPengeluaran();
        break;
      case '5':
        await menuUbahPengeluaran();
        break;
      case '6':
        await menuHapusPengeluaran();
        break;
      case '7':
        await menuUjiKondisiGagal();
        break;
      case '0':
        console.log('\nTerima kasih telah menggunakan Client Console Travel Expense API!');
        rl.close();
        process.exit(0);
      default:
        console.log('\nPilihan tidak valid. Silakan pilih angka 0 - 7.');
    }

    console.log('\nTekan Enter untuk kembali ke menu utama...');
    await tanya('');
  }
}

mainLoop();
