import Navbar from '@/components/Navbar'
import { BarChartComponent, LineChartComponent, PieChartComponent } from '@/components/Charts'

export default function Relatorios() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <Navbar />

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold gradient-text mb-12">Relatórios</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="glass-effect p-8 card-hover">
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Relatório Mensal</h2>
            <BarChartComponent />
          </div>

          <div className="glass-effect p-8 card-hover">
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Análise de Crescimento</h2>
            <LineChartComponent />
          </div>

          <div className="glass-effect p-8 card-hover">
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Distribuição de Status</h2>
            <PieChartComponent />
          </div>

          <div className="glass-effect p-8 card-hover">
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Resumo Executivo</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-navy-50 rounded-lg">
                <span className="font-medium">Total de Projetos</span>
                <span className="text-2xl font-bold text-navy-600">228</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-teal-50 rounded-lg">
                <span className="font-medium">Projetos Ativos</span>
                <span className="text-2xl font-bold text-teal-600">72</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-amber-50 rounded-lg">
                <span className="font-medium">Pendentes</span>
                <span className="text-2xl font-bold text-amber-600">24</span>
              </div>
              <button className="btn-primary w-full mt-6">Exportar Relatório</button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
