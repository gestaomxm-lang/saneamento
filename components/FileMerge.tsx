'use client'

import { useState } from 'react'
import * as XLSX from 'xlsx'

type Row = Record<string, any>

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

function downloadWorkbook(rows: Row[], filename = 'resultado.xlsx') {
  const ws = XLSX.utils.json_to_sheet(rows)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Resultado')
  XLSX.writeFile(wb, filename)
}

export default function FileMerge() {
  // file objects are not stored; we only read their content into dataA/dataB
  const [dataA, setDataA] = useState<Row[] | null>(null)
  const [dataB, setDataB] = useState<Row[] | null>(null)
  const [keyA, setKeyA] = useState<string>('')
  const [keyB, setKeyB] = useState<string>('')
  const [status, setStatus] = useState<string>('')

  const handleLoadA = async (f: File) => {
    setStatus('Lendo arquivo A...')
    const rows = await readFile(f)
    setDataA(rows)
    setStatus('')
  }
  const handleLoadB = async (f: File) => {
    setStatus('Lendo arquivo B...')
    const rows = await readFile(f)
    setDataB(rows)
    setStatus('')
  }

  const handleProcess = () => {
    if (!dataA || !dataB) return alert('Envie os dois arquivos primeiro')
    if (!keyA || !keyB) return alert('Selecione as colunas-chave em ambos os arquivos')

    setStatus('Processando...')

    // Build index for B
    const bIndex = new Map<string, Row[]>()
    for (const row of dataB) {
      const k = String(row[keyB] ?? '')
      if (!bIndex.has(k)) bIndex.set(k, [])
      bIndex.get(k)!.push(row)
    }

    const result: Row[] = []
    const bCols = dataB.length > 0 ? Object.keys(dataB[0]) : []
    const aCols = dataA.length > 0 ? Object.keys(dataA[0]) : []

    for (const aRow of dataA) {
      const k = String(aRow[keyA] ?? '')
      const matches = bIndex.get(k)
      if (matches && matches.length > 0) {
        for (const bRow of matches) {
          const out: Row = {}
          for (const c of aCols) out[`A_${c}`] = aRow[c]
          for (const c of bCols) out[`B_${c}`] = bRow[c]
          result.push(out)
        }
      } else {
        const out: Row = {}
        for (const c of aCols) out[`A_${c}`] = aRow[c]
        for (const c of bCols) out[`B_${c}`] = ''
        result.push(out)
      }
    }

    downloadWorkbook(result)
    setStatus('Pronto — download iniciado')
  }

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Processar Arquivos</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium mb-2">Arquivo A</label>
          <input
            type="file"
            accept=".xls,.xlsx,.csv"
            onChange={(e) => {
              const f = e.target.files?.[0]
              if (f) handleLoadA(f)
            }}
            className="mb-2"
          />
          {dataA && (
            <div className="text-sm text-gray-600">
              Colunas: {Object.keys(dataA[0] ?? {}).join(', ')}
            </div>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Arquivo B</label>
          <input
            type="file"
            accept=".xls,.xlsx,.csv"
            onChange={(e) => {
              const f = e.target.files?.[0]
              if (f) handleLoadB(f)
            }}
            className="mb-2"
          />
          {dataB && (
            <div className="text-sm text-gray-600">Colunas: {Object.keys(dataB[0] ?? {}).join(', ')}</div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium mb-2">Chave A</label>
          <select
            value={keyA}
            onChange={(e) => setKeyA(e.target.value)}
            className="w-full px-3 py-2 border rounded"
          >
            <option value="">-- selecione --</option>
            {dataA && Object.keys(dataA[0]).map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Chave B</label>
          <select
            value={keyB}
            onChange={(e) => setKeyB(e.target.value)}
            className="w-full px-3 py-2 border rounded"
          >
            <option value="">-- selecione --</option>
            {dataB && Object.keys(dataB[0]).map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex gap-3">
        <button onClick={handleProcess} className="btn-primary">Processar e Baixar</button>
        <button onClick={() => { setDataA(null); setDataB(null); setKeyA(''); setKeyB(''); setStatus('') }} className="btn-secondary">Limpar</button>
      </div>

      {status && <p className="mt-4 text-sm text-gray-600">{status}</p>}
    </div>
  )
}
