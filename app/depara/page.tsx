import Navbar from '@/components/Navbar'
import CreateCombinedDepara from '@/components/CreateCombinedDepara'

export const metadata = {
  title: 'Create Combined Depara',
}

export default function DeparaPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-5xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 gradient-text">Criar arquivo de De-Para</h1>
        <p className="mb-6 text-gray-600">Baseado no script `create_combined_depara.py`. Envie `base_hcm` e `base_rhc` e baixe `resultado_de_para.xlsx`.</p>
        <CreateCombinedDepara />
      </main>
    </div>
  )
}
