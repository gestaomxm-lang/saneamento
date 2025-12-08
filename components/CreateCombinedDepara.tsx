 'use client'

import { useState } from 'react'
import * as XLSX from 'xlsx'

type Row = Record<string, any>

function normalize_text(text: any) {
  if (text === null || text === undefined) return ''
  const s = String(text)
  // Normalize NFKD and remove combining diacritics
  const normalized = s.normalize('NFKD').replace(/\p{Diacritic}/gu, '').toUpperCase().trim()
  // Fallback for environments without \p{Diacritic}
  return normalized.replace(/[\u0300-\u036f]/g, '')
}

function readFile(file: File): Promise<Row[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const data = e.target?.result
        if (!data) return resolve([])
        const wb = XLSX.read(data, { type: 'array' })
        const wsName = wb.SheetNames[0]
        const ws = wb.Sheets[wsName]
        const json = XLSX.utils.sheet_to_json<Row>(ws, { defval: '' })
        resolve(json)
      } catch (err) {
        reject(err)
      }
    }
    reader.onerror = reject
    reader.readAsArrayBuffer(file)
  })
}

function downloadWorkbook(rows: Row[], filename = 'resultado_de_para.xlsx') {
  const ws = XLSX.utils.json_to_sheet(rows)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Resultado')
  XLSX.writeFile(wb, filename)
}

export default function CreateCombinedDepara() {
  const [hcmRows, setHcmRows] = useState<Row[] | null>(null)
  const [rhcRows, setRhcRows] = useState<Row[] | null>(null)
  const [status, setStatus] = useState<string>('')
  const [stats, setStats] = useState<{ total: number; matches: number; rate: number } | null>(null)

  const handleLoadHcm = async (f: File) => {
    setStatus('Lendo base_hcm...')
    const rows = await readFile(f)
    setHcmRows(rows)
    setStatus('')
  }

  const handleLoadRhc = async (f: File) => {
    setStatus('Lendo base_rhc...')
    const rows = await readFile(f)
    setRhcRows(rows)
    setStatus('')
  }

  const handleProcess = () => {
    setStats(null)
    if (!hcmRows || !rhcRows) return alert('Envie os dois arquivos: base_hcm e base_rhc')

    // Validate required columns in both
    const required = ['CÓDIGO', 'PRODUTO']
    const hcmCols = hcmRows.length > 0 ? Object.keys(hcmRows[0]) : []
    const rhcCols = rhcRows.length > 0 ? Object.keys(rhcRows[0]) : []
    const missingHcm = required.filter((c) => !hcmCols.includes(c))
    const missingRhc = required.filter((c) => !rhcCols.includes(c))
    if (missingHcm.length > 0) return alert(`Arquivo base_hcm está faltando colunas: ${missingHcm.join(', ')}`)
    if (missingRhc.length > 0) return alert(`Arquivo base_rhc está faltando colunas: ${missingRhc.join(', ')}`)

    setStatus('Normalizando e fazendo merge...')

    // Build _KEY for both
    const hcmCopy = hcmRows.map((r) => ({ ...r, _KEY: normalize_text(r['PRODUTO']) }))
    const rhcCopy = rhcRows.map((r) => ({ ...r, _KEY: normalize_text(r['PRODUTO']) }))

    // Build index for rhc by _KEY
    const rhcIndex = new Map<string, Row>()
    for (const r of rhcCopy) {
      const k = String(r['_KEY'] ?? '')
      if (!rhcIndex.has(k)) rhcIndex.set(k, r)
      // If multiple exist, we keep the first
    }

    // Build result
    const result: Row[] = []
    for (const a of hcmCopy) {
      const k = String(a['_KEY'] ?? '')
      const matched = rhcIndex.get(k)
      const out: Row = { ...a }
      if (matched) {
        out['CÓDIGO RHC'] = matched['CÓDIGO']
        out['PRODUTO RHC'] = matched['PRODUTO']
      } else {
        out['CÓDIGO RHC'] = ''
        out['PRODUTO RHC'] = ''
      }
      result.push(out)
    }

    // Compute stats
    const total = hcmCopy.length
    const matches = result.filter((r) => r['CÓDIGO RHC'] !== '' && r['CÓDIGO RHC'] !== null && r['CÓDIGO RHC'] !== undefined).length
    const rate = total === 0 ? 0 : (matches / total) * 100
    setStats({ total, matches, rate })

    // Drop _KEY before saving
    const final = result.map((r) => {
      const copy = { ...r }
      delete copy['_KEY']
      return copy
    })

    downloadWorkbook(final)
    setStatus('Pronto — download iniciado')
  }

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Create Combined Depara (igual ao script)</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium mb-2">base_hcm.xlsx</label>
          <input type="file" accept=".xls,.xlsx,.csv" onChange={(e) => { const f = e.target.files?.[0]; if (f) handleLoadHcm(f) }} />
          {hcmRows && <div className="text-sm text-gray-600 mt-2">Linhas: {hcmRows.length} — Colunas: {Object.keys(hcmRows[0] ?? {}).join(', ')}</div>}
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">base_rhc.xlsx</label>
          <input type="file" accept=".xls,.xlsx,.csv" onChange={(e) => { const f = e.target.files?.[0]; if (f) handleLoadRhc(f) }} />
          {rhcRows && <div className="text-sm text-gray-600 mt-2">Linhas: {rhcRows.length} — Colunas: {Object.keys(rhcRows[0] ?? {}).join(', ')}</div>}
        </div>
      </div>

      <div className="flex gap-3 mb-4">
        <button onClick={handleProcess} className="btn-primary">Processar e Baixar resultado_de_para.xlsx</button>
        <button onClick={() => { setHcmRows(null); setRhcRows(null); setStats(null); setStatus('') }} className="btn-secondary">Limpar</button>
      </div>

      {status && <p className="text-sm text-gray-600">{status}</p>}

      {stats && (
        <div className="mt-4 bg-gray-50 p-3 rounded">
          <p>Total HCM: <strong>{stats.total}</strong></p>
          <p>Matches encontrados: <strong>{stats.matches}</strong></p>
          <p>Taxa de match: <strong>{stats.rate.toFixed(2)}%</strong></p>
        </div>
      )}
    </div>
  )
}
