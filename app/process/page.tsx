import FileMerge from '@/components/FileMerge'
import Navbar from '@/components/Navbar'

export const metadata = {
  title: 'Processar Arquivos',
}

export default function ProcessPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-5xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 gradient-text">Upload e Gerar Resultado</h1>
        <p className="mb-6 text-gray-600">Envie os dois arquivos (A e B), selecione as colunas-chave e clique em processar para baixar o Excel resultante.</p>
        <FileMerge />
      </main>
    </div>
  )
}
